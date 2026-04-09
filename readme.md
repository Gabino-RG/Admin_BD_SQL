# 📊 MariaDB Admin Panel

### *Gestor Integral de Bases de Datos MariaDB*

Una herramienta visual, moderna y poderosa para administrar servidores **MariaDB**, construida con **Python** y **Flet**. Diseñada para transformar tareas complejas en acciones simples con una interfaz limpia e interactiva.

---

## 🚀 Características Principales

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

## 🖥️ Vista Previa

> ✨ Aquí puedes agregar capturas de tu dashboard, gráficas o consola SQL para mostrar el potencial visual de la herramienta.

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

**Gabino**
🎓 8vo Cuatrimestre - UTSJR

---

## 🌟 Filosofía del Proyecto

Este panel no solo administra bases de datos.
Convierte datos en decisiones, procesos en clics y complejidad en claridad.

---

🚀 *Listo para ejecutar. Listo para escalar. Listo para impresionar.*
