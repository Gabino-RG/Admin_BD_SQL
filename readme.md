# 📊 Mstar - MariaDB Admin Panel

### *Gestor Integral de Bases de Datos MariaDB*

Mstar es una herramienta visual, moderna y poderosa para administrar servidores **MariaDB**, construida con **Python** y **Flet**. Diseñada para transformar tareas complejas en acciones simples con una interfaz limpia e interactiva.

---

## 🚀 Características Principales

## 🛡️ Seguridad y Control de Acceso (RBAC)

A diferencia de los administradores de bases de datos convencionales, **Mstar** implementa un modelo de **Control de Acceso Basado en Roles (RBAC)** vinculado directamente al motor de MariaDB.

### ¿Cómo funciona el RBAC en Mstar?
El sistema no utiliza una tabla de usuarios interna; en su lugar, utiliza los **Privilegios Nativos de MariaDB** (`GRANT` / `REVOKE`). Al iniciar sesión, el sistema analiza dinámicamente los permisos del usuario mediante `SHOW GRANTS` y muta la interfaz de usuario:

1.  **Acceso Total (Admin):** Visualización de todas las bases de datos, gestión completa de usuarios (creación/borrado) y gestión de respaldos.
2.  **Solo Respaldos:** Acceso restringido únicamente a la generación de archivos `.sql` (Dump).
3.  **Solo Lectura:** Interfaz limitada exclusivamente a la visualización de métricas de rendimiento y gráficas de datos.

---

## 🚀 Guía de Inicio Rápido

### Requisitos Previos
* Tener instalado y activo un servidor **MariaDB** (o MySQL a través de XAMPP/WAMP) en el puerto `3306`.
* Contar con un usuario con privilegios administrativos para la configuración inicial.

### Primera Conexión (Modo Maestro)
Para configurar tus primeros usuarios y ver el potencial completo de la herramienta, inicia sesión de la siguiente manera:
1.  **Usuario:** `root`
2.  **Contraseña:** *(La contraseña que configuraste en tu instalación local de MariaDB/XAMPP. Si usas XAMPP por defecto, déjala en blanco).*
3.  **Servidor:** `127.0.0.1`

### 🏠 Dashboard Inteligente

Monitorea en tiempo real el estado de tu servidor:

* Versión de MariaDB
* Tiempo activo (Uptime)
* Número total de bases de datos

### 💾 Gestión de Respaldos

* Exporta bases de datos a archivos `.sql`
* Importa respaldos fácilmente
* Integración directa con `mysqldump` y `mysql`

### 📄 Herramientas CSV

* Importación masiva de datos desde CSV
* Exportación de tablas a archivos planos
* Ideal para migraciones y análisis externo

### 📈 Monitor de Rendimiento

* Visualiza el uso de almacenamiento por tabla
* Gráficas interactivas con **Plotly**
* Identifica rápidamente cuellos de botella

### 💻 Consola SQL Integrada

* Ejecuta consultas DDL y DML
* Registro de operaciones exitosas y fallidas
* Experiencia tipo terminal dentro de la app

### 👥 Gestión de Usuarios

* Crear y eliminar usuarios
* Asignar roles:

  * Admin
  * Solo lectura
  * Respaldos

---

## 🛠️ Stack Tecnológico

| Tecnología          | Descripción                          |
| ------------------- | ------------------------------------ |
| 🐍 Python 3.11+     | Lenguaje principal                   |
| 🎨 Flet             | Interfaz gráfica basada en Flutter   |
| 🗄️ MariaDB / MySQL | Sistema de base de datos             |
| 📊 Plotly           | Visualización de datos               |
| 📦 Librerías        | mariadb, pandas, kaleido, subprocess |

---

## 📦 Instalación y Configuración

Se recomienda el uso de un entorno virtual para mantener las dependencias aisladas y evitar conflictos.

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv venv
```

### 3️⃣ Activar entorno virtual

**Windows:**

```bash
.\venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5️⃣ Ejecutar la aplicación

```bash
python main.py
```

---

## 💡 Nota sobre MariaDB

Para que las funciones de respaldo e importación funcionen correctamente:

* MariaDB debe estar instalado en el sistema
* La carpeta `bin` de MariaDB debe estar en el **PATH** del sistema

Esto asegura que comandos como `mysqldump` y `mysql` funcionen correctamente desde la aplicación.

---

## 📂 Estructura del Proyecto

```text
├── main.py
├── db_config.py
├── requirements.txt
└── views/
    ├── view_dashboard.py
    ├── view_backup.py
    ├── view_csv.py
    ├── view_charts.py
    ├── view_sql.py
    └── view_users.py
```

---

## 👨‍💻 Autor

**Gabino Reyes**
🎓 8vo Cuatrimestre - UTSJR

---

## 🌟 Filosofía del Proyecto

Este panel no solo administra bases de datos.
Convierte datos en decisiones, procesos en clics y complejidad en claridad.

---

🚀 *Listo para ejecutar. Listo para escalar. Listo para impresionar.*
