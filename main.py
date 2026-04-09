import flet as ft
from views.view_backup import backup_view
from views.view_csv import csv_view
from views.view_sql import sql_view
from views.view_charts import charts_view
from views.view_users import users_view
from views.view_dashboard import dashboard_view

# Estadísticas de la sesión
stats = {"exitosas": 0, "fallidas": 0}

def main(page: ft.Page):
    # --- Configuración de la Ventana ---
    page.title = "MariaDB Admin Panel"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1100
    page.window.height = 750
    page.padding = 0  # Quitamos el padding global para que el menú pegue al borde

    # --- APPBAR (La barra superior pro) ---
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.STORAGE_ROUNDED, color=ft.colors.BLUE_400, size=28),
        leading_width=60,
        title=ft.Text("MariaDB Server Manager", size=20, weight="bold"),
        center_title=False,
        bgcolor=ft.colors.BLACK26, # Mismo color que el menú lateral
        actions=[
            # Indicador de "Servidor en línea"
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, color=ft.colors.GREEN_400, size=12),
                    ft.Text("Localhost (root)", color=ft.colors.WHITE70, size=13, weight="w500")
                ]),
                padding=ft.padding.only(right=20)
            )
        ]
    )

    # --- ÁREA DE CONTENIDO ---
    # Usamos una columna interna para cambiar las vistas
    content_column = ft.Column(expand=True)
    
    # Y la metemos en un contenedor para darle márgenes bonitos
    content_area = ft.Container(
        content=content_column,
        expand=True,
        padding=20 # Esto evita que las tarjetas se peguen a la pantalla
    )

    def nav_change(e):
        index = e.control.selected_index
        content_column.controls.clear()
        
        if index == 0:
            content_column.controls.append(dashboard_view(page))
        elif index == 1:
            content_column.controls.append(backup_view(page))
        elif index == 2:
            content_column.controls.append(csv_view(page))
        elif index == 3:
            content_column.controls.append(charts_view(page, stats))
        elif index == 4:
            content_column.controls.append(sql_view(page, stats))
        elif index == 5:
            content_column.controls.append(users_view(page))
        page.update()

    # --- MENÚ LATERAL ---
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.colors.BLACK26, # Fondo oscuro elegante
        min_width=100,
        group_alignment=-0.95, # Empuja los íconos hacia la parte superior
        destinations=[
            # Agregamos la animación de ícono vacío (OUTLINED) a ícono lleno al seleccionar
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.Icons.SAVE_OUTLINED, selected_icon=ft.Icons.SAVE, label="Respaldos"),
            ft.NavigationRailDestination(icon=ft.Icons.DATA_OBJECT_OUTLINED, selected_icon=ft.Icons.DATA_OBJECT, label="CSV"),
            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART_OUTLINED, selected_icon=ft.Icons.BAR_CHART, label="Rendimiento"),
            ft.NavigationRailDestination(icon=ft.Icons.TERMINAL_OUTLINED, selected_icon=ft.Icons.TERMINAL, label="Consola SQL"),
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE_OUTLINED, selected_icon=ft.Icons.PEOPLE, label="Usuarios"),
        ],
        on_change=nav_change,
    )

    # Carga inicial (Llamamos a la primera vista)
    content_column.controls.append(dashboard_view(page))

    # Ensamblaje final de la página
    page.add(
        ft.Row(
            [
                sidebar, 
                ft.VerticalDivider(width=1, color=ft.colors.WHITE10), # Línea divisoria súper sutil
                content_area
            ],
            expand=True,
            spacing=0 # Sin espacio extra, el padding ya lo da el content_area
        )
    )

if __name__ == "__main__":
    ft.app(target=main)