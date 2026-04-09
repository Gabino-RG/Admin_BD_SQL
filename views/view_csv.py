import flet as ft
import csv
from db_config import get_connection, obtener_bases_datos, obtener_tablas

def csv_view(page: ft.Page):
    # --- 1. Estilizado de Componentes ---
    db_dropdown = ft.Dropdown(
        label="1. Selecciona la Base de Datos",
        hint_text="Base de datos...",
        width=350,
        border_radius=12,
        bgcolor=ft.colors.BLACK12,
        prefix_icon=ft.Icons.STORAGE,
        options=[ft.dropdown.Option(db) for db in obtener_bases_datos()]
    )
    
    tabla_dropdown = ft.Dropdown(
        label="2. Selecciona la Tabla",
        hint_text="Tabla origen/destino...",
        width=350,
        border_radius=12,
        bgcolor=ft.colors.BLACK12,
        prefix_icon=ft.Icons.TABLE_CHART,
        disabled=True
    )

    # Texto de estado mejorado dentro de un contenedor
    status_text = ft.Text("", size=14, weight="w500")
    status_container = ft.Container(
        content=status_text,
        padding=10,
        border_radius=10,
        visible=False
    )

    def mostrar_mensaje(texto, color):
        status_text.value = texto
        status_text.color = color
        status_container.bgcolor = ft.colors.with_opacity(0.1, color)
        status_container.visible = True
        page.update()

    # --- 2. Lógica de Eventos ---
    def on_db_change(e):
        tablas = obtener_tablas(db_dropdown.value)
        tabla_dropdown.options = [ft.dropdown.Option(t) for t in tablas]
        tabla_dropdown.disabled = False
        # Limpiamos la selección anterior si la hubiera
        tabla_dropdown.value = None
        tabla_dropdown.update()

    db_dropdown.on_change = on_db_change

    # --- Lógica de EXPORTAR ---
    def on_export_result(e: ft.FilePickerResultEvent):
        if e.path:
            if not db_dropdown.value or not tabla_dropdown.value:
                mostrar_mensaje("⚠️ Selecciona una BD y una Tabla primero.", ft.colors.ORANGE)
                return
            
            try:
                mostrar_mensaje("⏳ Generando archivo CSV...", ft.colors.BLUE_200)
                conn = get_connection(db_dropdown.value)
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {tabla_dropdown.value}")
                
                columnas = [i[0] for i in cursor.description]
                filas = cursor.fetchall()

                with open(e.path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(columnas)
                    writer.writerows(filas)
                
                conn.close()
                mostrar_mensaje("✅ Datos exportados con éxito a CSV.", ft.colors.GREEN_400)
            except Exception as err:
                mostrar_mensaje(f"❌ Error al exportar: {str(err)}", ft.colors.RED_400)

    # --- Lógica de IMPORTAR ---
    def on_import_result(e: ft.FilePickerResultEvent):
        if e.files:
            if not db_dropdown.value or not tabla_dropdown.value:
                mostrar_mensaje("⚠️ Selecciona una BD y una Tabla destino.", ft.colors.ORANGE)
                return

            try:
                mostrar_mensaje("🚀 Importando datos a la tabla...", ft.colors.BLUE_200)
                conn = get_connection(db_dropdown.value)
                cursor = conn.cursor()
                
                with open(e.files[0].path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    columnas = next(reader)
                    
                    placeholder = ", ".join(["%s"] * len(columnas))
                    cols_str = ", ".join(columnas)
                    query = f"INSERT INTO {tabla_dropdown.value} ({cols_str}) VALUES ({placeholder})"
                    
                    cursor.executemany(query, list(reader))
                    conn.commit()
                
                conn.close()
                mostrar_mensaje("✅ Datos importados correctamente.", ft.colors.GREEN_400)
            except Exception as err:
                mostrar_mensaje(f"❌ Error al importar: {str(err)}", ft.colors.RED_400)

    # Validadores para los botones
    def trigger_export(e):
        if not tabla_dropdown.value:
            mostrar_mensaje("⚠️ Selecciona una tabla para exportar.", ft.colors.ORANGE)
            return
        picker_export.save_file(file_name=f"{tabla_dropdown.value}.csv")

    def trigger_import(e):
        if not tabla_dropdown.value:
            mostrar_mensaje("⚠️ Selecciona una tabla para importar.", ft.colors.ORANGE)
            return
        picker_import.pick_files(allowed_extensions=["csv"])

    picker_export = ft.FilePicker(on_result=on_export_result)
    picker_import = ft.FilePicker(on_result=on_import_result)
    page.overlay.extend([picker_export, picker_import])

    # --- 3. Construcción de la UI ---
    return ft.Column([
        # Cabecera
        ft.Row([
            ft.Icon(ft.Icons.DATA_OBJECT, size=40, color=ft.colors.TEAL_400),
            ft.Column([
                ft.Text("Migración de Datos CSV", size=28, weight="bold"),
                ft.Text("Transfiere información entre MariaDB y archivos planos", color=ft.colors.WHITE70),
            ], spacing=0)
        ]),
        
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),

        # Cuerpo Principal (Tarjeta)
        ft.Card(
            content=ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Parámetros de Transferencia", size=18, weight="bold"),
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    
                    ft.Row([db_dropdown, tabla_dropdown], spacing=20),
                    
                    ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            "Exportar a CSV", 
                            icon=ft.Icons.FILE_DOWNLOAD,
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.GREEN_700,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=trigger_export
                        ),
                        ft.ElevatedButton(
                            "Importar desde CSV", 
                            icon=ft.Icons.FILE_UPLOAD,
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.BLUE_700,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=trigger_import
                        ),
                    ], spacing=15),
                    
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
                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.colors.YELLOW_400, size=20),
                ft.Text(
                    "Al importar, asegúrate de que el CSV tenga las mismas columnas que la tabla destino.",
                    size=12, color=ft.colors.WHITE70
                )
            ])
        )
    ], spacing=10, expand=True)