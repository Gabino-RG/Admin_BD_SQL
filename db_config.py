import mariadb
import os

CURRENT_DB_USER = ""
CURRENT_DB_PASS = ""

# --- CONFIGURACIÓN CORE ---
def get_connection(db_name=None):
    global CURRENT_DB_USER, CURRENT_DB_PASS
    db_host = "127.0.0.1" 
    try:
        config = {
            "user": CURRENT_DB_USER if CURRENT_DB_USER else "root",
            "password": CURRENT_DB_PASS, 
            "host": db_host,
            "port": 3306
        }
        if db_name:
            config["database"] = db_name
        return mariadb.connect(**config)
    except mariadb.Error as e:
        print(f"Error de conexión: {e}")
        return None

# --- Validacion de login ---
def validar_login(usuario, password):
    global CURRENT_DB_USER, CURRENT_DB_PASS
    # 1. Limpieza anti-inyección básica por si acaso
    u_limpio = usuario.replace("'", "").replace('"', '').replace(";", "").strip()
    try:
        # 2. Intentamos conectar directo al motor con esas credenciales
        conn = mariadb.connect(
            user=u_limpio,
            password=password,
            host="127.0.0.1",
            port=3306
        )
        # 3. Si conectó, le preguntamos a MariaDB qué permisos tiene este usuario
        cursor = conn.cursor()
        cursor.execute("SHOW GRANTS FOR CURRENT_USER;")
        grants = cursor.fetchall()
        # Convertimos todo a texto mayúscula para buscar palabras clave
        grants_str = " ".join([g[0].upper() for g in grants])
        # 4. Clasificamos el Rol según sus permisos reales
        if "ALL PRIVILEGES" in grants_str or "GRANT ALL" in grants_str:
            rol = "Acceso Total (Admin)"
        elif "RELOAD" in grants_str or "LOCK TABLES" in grants_str:
            rol = "Solo Respaldos"
        elif "SELECT" in grants_str:
            rol = "Solo Lectura"
        else:
            rol = "Solo Lectura" # Fallback por seguridad
        conn.close()
        # 5. Guardamos en la memoria global para que la app lo use
        CURRENT_DB_USER = u_limpio
        CURRENT_DB_PASS = password
        
        return True, rol, "✅ Acceso concedido"
        
    except mariadb.Error as e:
        # Si MariaDB lo rechaza (mala contraseña o no existe)
        return False, None, "❌ Credenciales incorrectas o acceso denegado"

# --- HELPERS (Para no repetir código) ---
def fetch_query(query, db=None):
    """Ejecuta una consulta y devuelve los resultados."""
    conn = get_connection(db)
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res

def run_action(query):
    """Para INSERT, UPDATE, DELETE, DROP, etc."""
    conn = get_connection()
    if not conn: return False, "Error de conexión"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True, "Operación exitosa"
    except Exception as e:
        return False, str(e)

# --- FUNCIONES DE LA APP ---

def obtener_bases_datos():
    res = fetch_query("SHOW DATABASES")
    omitir = ('information_schema', 'performance_schema', 'mysql', 'sys')
    return [r[0] for r in res if r[0] not in omitir]

def obtener_tablas(db_name):
    res = fetch_query("SHOW TABLES", db=db_name)
    return [r[0] for r in res]

def obtener_tamano_tablas(db_name):
    query = f"""
        SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) 
        FROM information_schema.TABLES WHERE table_schema = '{db_name}'
        ORDER BY (data_length + index_length) DESC LIMIT 10
    """
    return fetch_query(query)

def gestionar_usuario(admin_conn, usuario, password, rol):
    # 🛡️ SANITIZACIÓN ANTI-INYECCIÓN (Limpiamos comillas y puntos y comas)
    u_limpio = usuario.replace("'", "").replace('"', '').replace(";", "").strip()
    p_limpia = password.replace("'", "").replace('"', '').replace(";", "").strip()

    try:
        cursor = admin_conn.cursor()
        # 1. Creamos el usuario usando las variables limpias
        cursor.execute(f"CREATE USER '{u_limpio}'@'%' IDENTIFIED BY '{p_limpia}'")
        # 2. Definimos los privilegios (¡Ya con el GRANT corregido para el Admin!)
        privs = {
            "Acceso Total (Admin)": "GRANT ALL PRIVILEGES ON *.* TO '{u}'@'%' WITH GRANT OPTION",
            "Solo Respaldos": "GRANT SELECT, RELOAD, LOCK TABLES, REPLICATION CLIENT, SHOW VIEW, PROCESS, EVENT, TRIGGER ON *.* TO '{u}'@'%'",
            "Solo Lectura": "GRANT SELECT ON *.* TO '{u}'@'%'"
        }
        # 3. Asignamos los permisos y refrescamos
        cursor.execute(privs[rol].format(u=u_limpio))
        cursor.execute("FLUSH PRIVILEGES")
        return True, f"✅ Usuario '{u_limpio}' creado exitosamente."
    except Exception as e: 
        return False, f"❌ Error al crear usuario: {e}"
    
def listar_usuarios_con_roles():
    raw_users = fetch_query("SELECT User, Host FROM mysql.user WHERE User NOT IN ('mariadb.sys', 'root', 'mysql', 'PUBLIC', '')")
    conn = get_connection()
    procesados = []
    if conn:
        cursor = conn.cursor()
        for u, h in raw_users:
            try:
                cursor.execute(f"SHOW GRANTS FOR '{u}'@'{h}'")
                grants = str(cursor.fetchall())
                rol = "Acceso Total" if "ALL PRIVILEGES" in grants else "Solo Respaldos" if "LOCK TABLES" in grants else "Solo Lectura" if "SELECT" in grants else "Personalizado"
                procesados.append({"user": u, "host": h, "rol": rol})
            except: continue
        conn.close()
    return procesados

def eliminar_usuario(u, h):
    return run_action(f"DROP USER '{u}'@'{h}'")

def obtener_info_servidor():
    try:
        # 1. Obtenemos la versión
        v_raw = fetch_query("SELECT @@version")
        v = v_raw[0][0] if v_raw else "Desconocida"

        # 2. Obtenemos el Uptime en SEGUNDOS (este nunca falla)
        up_raw = fetch_query("SHOW GLOBAL STATUS LIKE 'Uptime'")
        if up_raw:
            segundos = int(up_raw[0][1])
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            uptime_final = f"{horas}h {minutos}m"
        else:
            uptime_final = "0h 0m"

        # 3. Conteo de Bases de Datos
        db_raw = fetch_query("SELECT COUNT(*) FROM information_schema.SCHEMATA")
        db_count = db_raw[0][0] if db_raw else 0

        return {"version": v, "uptime": uptime_final, "dbs": db_count}
    except Exception as e:
        print(f"Error en dashboard: {e}")
        return {"version": "Error", "uptime": "0s", "dbs": 0}