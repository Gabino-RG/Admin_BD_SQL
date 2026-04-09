import flet as ft
from db_config import get_connection, obtener_bases_datos

def sql_view(page: ft.Page, stats):
    # --- 1. Estilizado de Componentes ---
    db_dropdown = ft.Dropdown(
        label="Base de Datos", 
        width=300,
        border_radius=12,
        bgcolor=ft.colors.BLACK12,
        prefix_icon=ft.Icons.STORAGE,
        options=[ft.dropdown.Option(db) for db in obtener_bases_datos()]
    )
    
    # Estilo "Terminal" para el input de SQL
    sql_input = ft.TextField(
        label="Editor de Consultas SQL",
        multiline=True,
        min_lines=5,
        max_lines=8,
        hint_text="Ejemplo: SELECT * FROM tabla LIMIT 10;",
        text_size=15,
        border_radius=12,
        bgcolor=ft.colors.BLACK26, # Fondo oscuro tipo terminal
        border_color=ft.colors.BLUE_700,
        focused_border_color=ft.colors.BLUE_400,
        text_style=ft.TextStyle(font_family="Consolas") # Letra tipo código
    )
    
    # Tabla con diseño limpio
    result_table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Resultado", weight="bold"))],
        rows=[],
        border=ft.border.all(1, ft.colors.WHITE10),
        vertical_lines=ft.border.BorderSide(1, ft.colors.WHITE10),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.WHITE10),
        heading_row_color=ft.colors.BLACK26,
    )

    # Sistema de Mensajes Pro
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

    # --- 2. Lógica de Ejecución ---
    def ejecutar_sql(e):
        if not db_dropdown.value or not sql_input.value:
            mostrar_mensaje("⚠️ Selecciona una BD y escribe una consulta.", ft.colors.ORANGE)
            return

        try:
            mostrar_mensaje("⏳ Ejecutando consulta...", ft.colors.BLUE_200)
            conn = get_connection(db_dropdown.value)
            cursor = conn.cursor()
            cursor.execute(sql_input.value)

            if cursor.description:
                # Es un SELECT o similar que devuelve datos
                result_table.columns = [
                    ft.DataColumn(ft.Text(col[0].upper(), weight="bold", color=ft.colors.BLUE_200)) 
                    for col in cursor.description
                ]
                filas = cursor.fetchall()
                result_table.rows = [
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(valor))) for valor in fila]) 
                    for fila in filas
                ]
                mostrar_mensaje(f"✅ Consulta exitosa. Se recuperaron {len(filas)} filas.", ft.colors.GREEN_400)
            else:
                # Es un INSERT/UPDATE/DELETE
                conn.commit()
                result_table.columns = [ft.DataColumn(ft.Text("Resultado de Operación", color=ft.colors.BLUE_200))]
                result_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(f"✅ Filas afectadas: {cursor.rowcount}"))])]
                mostrar_mensaje("✅ Comando ejecutado correctamente.", ft.colors.GREEN_400)
            
            stats["exitosas"] += 1 
            cursor.close()
            conn.close()
        except Exception as err:
            stats["fallidas"] += 1 
            mostrar_mensaje(f"❌ Error de Sintaxis o Servidor: {str(err)}", ft.colors.RED_400)
        
        page.update()

    # --- 3. Construcción de la UI ---
    return ft.Column([
        # Cabecera
        ft.Row([
            ft.Icon(ft.Icons.TERMINAL_ROUNDED, size=40, color=ft.colors.PURPLE_400),
            ft.Column([
                ft.Text("Consola SQL Interactiva", size=28, weight="bold"),
                ft.Text("Ejecuta consultas DDL y DML directamente en el servidor", color=ft.colors.WHITE70),
            ], spacing=0)
        ]),
        
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),

        # Panel de Comandos
        ft.Card(
            content=ft.Container(
                padding=25,
                content=ft.Column([
                    ft.Row([
                        db_dropdown,
                        ft.ElevatedButton(
                            "Ejecutar Query", 
                            icon=ft.Icons.PLAY_ARROW_ROUNDED, 
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.PURPLE_700,
                                color=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=ejecutar_sql
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    sql_input,
                    
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    status_container
                ], spacing=10)
            ),
            elevation=5
        ),

        # Panel de Resultados
        ft.Text("Resultados de la Consulta:", weight="bold", size=16),
        ft.Container(
            # TRUCO: Doble scroll para que puedas mover la tabla arriba/abajo y derecha/izquierda
            content=ft.Column([
                ft.Row([result_table], scroll=ft.ScrollMode.ADAPTIVE)
            ], scroll=ft.ScrollMode.ADAPTIVE),
            bgcolor=ft.colors.BLACK12, 
            padding=10, 
            border_radius=10, 
            border=ft.border.all(1, ft.colors.WHITE10),
            expand=True # Para que ocupe el resto de la pantalla
        )
    ], spacing=15, expand=True)