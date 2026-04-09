import mariadb
import os

# --- CONFIGURACIÓN CORE ---
def get_connection(db_name=None):
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    try:
        config = {"user": "root", "password": "Mstar", "host": db_host, "port": 3306}
        if db_name: config["database"] = db_name
        return mariadb.connect(**config)
    except mariadb.Error as e:
        print(f"Error de conexión: {e}"); return None

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
    # Esta la dejamos casi igual por seguridad de los permisos
    try:
        cursor = admin_conn.cursor()
        cursor.execute(f"CREATE USER '{usuario}'@'%' IDENTIFIED BY '{password}'")
        privs = {
            "Acceso Total (Admin)": "ALL PRIVILEGES ON *.* TO '{u}'@'%' WITH GRANT OPTION",
            "Solo Respaldos": "GRANT SELECT, RELOAD, LOCK TABLES, REPLICATION CLIENT, SHOW VIEW, PROCESS, EVENT, TRIGGER ON *.* TO '{u}'@'%'",
            "Solo Lectura": "GRANT SELECT ON *.* TO '{u}'@'%'"
        }
        cursor.execute(privs[rol].format(u=usuario))
        cursor.execute("FLUSH PRIVILEGES")
        return True, f"✅ Usuario '{usuario}' creado."
    except Exception as e: return False, f"❌ Error: {e}"

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