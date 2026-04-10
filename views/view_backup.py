import flet as ft
import subprocess
import db_config
from db_config import obtener_bases_datos

def backup_view(page: ft.Page):
    usuario_actual = db_config.CURRENT_DB_USER
    pass_actual = db_config.CURRENT_DB_PASS

    # --- 1. Estilizado de Componentes ---
    lista_dbs = obtener_bases_datos()
    
    db_dropdown = ft.Dropdown(
        label="Base de Datos a procesar",
        hint_text="Selecciona una BD...",
        width=400,
        border_radius=15,
        bgcolor=ft.colors.BLACK12,
        focused_border_color=ft.colors.BLUE_400,
        prefix_icon=ft.Icons.STORAGE,
        options=[ft.dropdown.Option(db) for db in lista_dbs],
    )

    # Texto de estado mejorado dentro de un contenedor
    status_text = ft.Text("", size=14, weight="w500")
    status_container = ft.Container(
        content=status_text,
        padding=10,
        border_radius=10,
        visible=False # Se oculta hasta que haya mensajes
    )

    # --- Lógica de Mensajes (Para que el diseño brille) ---
    def mostrar_mensaje(texto, color):
        status_text.value = texto
        status_text.color = color
        status_container.bgcolor = ft.colors.with_opacity(0.1, color)
        status_container.visible = True
        page.update()

    # --- Lógica de Backup ---
    def on_backup_result(e: ft.FilePickerResultEvent):
        if e.path:
            db_seleccionada = db_dropdown.value
            if not db_seleccionada:
                mostrar_mensaje("⚠️ ¡Selecciona una BD primero!", ft.colors.ORANGE)
                return

            try:
                mostrar_mensaje(f"⏳ Procesando respaldo de {db_seleccionada}...", ft.colors.BLUE_200)
                cmd = f'mysqldump -u {usuario_actual} -p{pass_actual} {db_seleccionada} > "{e.path}"'
                subprocess.run(cmd, shell=True, check=True)
                mostrar_mensaje("✅ Respaldo generado con éxito.", ft.colors.GREEN_400)
            except Exception as err:
                mostrar_mensaje(f"❌ Error: {str(err)}", ft.colors.RED_400)

    # --- Lógica de Restore ---
    def on_restore_result(e: ft.FilePickerResultEvent):
        if e.files:
            db_seleccionada = db_dropdown.value
            if not db_seleccionada:
                mostrar_mensaje("⚠️ Selecciona la BD destino", ft.colors.ORANGE)
                return

            try:
                mostrar_mensaje("🚀 Restaurando base de datos...", ft.colors.BLUE_200)
                cmd = f'mysql -u {usuario_actual} -p{pass_actual} {db_seleccionada} < "{e.files[0].path}"'
                subprocess.run(cmd, shell=True, check=True)
                mostrar_mensaje("✅ Importación completada correctamente.", ft.colors.GREEN_400)
            except Exception as err:
                mostrar_mensaje(f"❌ Error: {str(err)}", ft.colors.RED_400)

    file_picker_save = ft.FilePicker(on_result=on_backup_result)
    file_picker_open = ft.FilePicker(on_result=on_restore_result)
    page.overlay.extend([file_picker_save, file_picker_open])

    # --- 2. Construcción de la UI ---
    return ft.Column([
        # Cabecera
        ft.Row([
            ft.Icon(ft.Icons.SETTINGS_BACKUP_RESTORE, size=40, color=ft.colors.BLUE_400),
            ft.Column([
                ft.Text("Gestión de Respaldos", size=28, weight="bold"),
                ft.Text("Mantenimiento y recuperación del servidor SQL", color=ft.colors.WHITE70),
            ], spacing=0)
        ], alignment=ft.MainAxisAlignment.START),
        
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),

        # Cuerpo Principal (Tarjeta)
        ft.Card(
            content=ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Configuración de Tarea", size=18, weight="bold"),
                    ft.Text("Selecciona el origen y la acción a realizar:", color=ft.colors.WHITE70, size=14),
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    
                    db_dropdown,
                    
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            "Exportar SQL", 
                            icon=ft.Icons.SAVE_ALT,
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.GREEN_700,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=lambda _: file_picker_save.save_file(file_name=f"respaldo.sql")
                        ),
                        ft.ElevatedButton(
                            "Importar SQL", 
                            icon=ft.Icons.UPLOAD_FILE_ROUNDED,
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.BLUE_700,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=lambda _: file_picker_open.pick_files(allowed_extensions=["sql"])
                        ),
                    ], alignment=ft.MainAxisAlignment.START, spacing=15),
                    
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    status_container
                ], spacing=10)
            ),
            elevation=5
        ),

        # Nota informativa
        ft.Container(
            padding=20,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
            border_radius=15,
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.colors.BLUE_200, size=20),
                ft.Text(
                    "Los respaldos incluyen estructuras y datos. Asegúrate de tener permisos de escritura.",
                    size=12, color=ft.colors.WHITE70
                )
            ])
        )
    ], spacing=10, expand=True)