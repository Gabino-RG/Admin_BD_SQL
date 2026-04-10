import flet as ft
from views.view_login import login_view # <--- IMPORTAMOS EL LOGIN
from views.view_backup import backup_view
from views.view_csv import csv_view
from views.view_sql import sql_view
from views.view_charts import charts_view
from views.view_users import users_view
from views.view_dashboard import dashboard_view

stats = {"exitosas": 0, "fallidas": 0}

def main(page: ft.Page):
    # --- Configuración Base ---
    page.title = "Mstar - MariaDB Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1100
    page.window.height = 750
    page.padding = 0

    # =========================================================================
    # FUNCIÓN PRINCIPAL: SE EJECUTA SOLO SI EL LOGIN ES EXITOSO
    # =========================================================================
    def cargar_interfaz_principal(rol_usuario, nombre_usuario):
        page.controls.clear() # Borramos la pantalla de login
        
        # --- Lógica de filtrado de Menú según el Rol ---
        destinos_menu = [
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Inicio"),
        ]
        
        # Administrador: Ve todo
        if rol_usuario == "Acceso Total (Admin)":
            destinos_menu.extend([
                ft.NavigationRailDestination(icon=ft.Icons.SAVE_OUTLINED, selected_icon=ft.Icons.SAVE, label="Respaldos"),
                ft.NavigationRailDestination(icon=ft.Icons.DATA_OBJECT_OUTLINED, selected_icon=ft.Icons.DATA_OBJECT, label="CSV"),
                ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART_OUTLINED, selected_icon=ft.Icons.BAR_CHART, label="Rendimiento"),
                ft.NavigationRailDestination(icon=ft.Icons.TERMINAL_OUTLINED, selected_icon=ft.Icons.TERMINAL, label="Consola SQL"),
                ft.NavigationRailDestination(icon=ft.Icons.PEOPLE_OUTLINED, selected_icon=ft.Icons.PEOPLE, label="Usuarios"),
            ])
            vistas_disponibles = [dashboard_view, backup_view, csv_view, charts_view, sql_view, users_view]
            
        # Respaldo: Solo BDs y CSV
        elif rol_usuario == "Solo Respaldos":
            destinos_menu.extend([
                ft.NavigationRailDestination(icon=ft.Icons.SAVE_OUTLINED, selected_icon=ft.Icons.SAVE, label="Respaldos"),
                ft.NavigationRailDestination(icon=ft.Icons.DATA_OBJECT_OUTLINED, selected_icon=ft.Icons.DATA_OBJECT, label="CSV"),
            ])
            vistas_disponibles = [dashboard_view, backup_view, csv_view]
            
        # Lectura: Solo gráficas
        elif rol_usuario == "Solo Lectura":
            destinos_menu.extend([
                ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART_OUTLINED, selected_icon=ft.Icons.BAR_CHART, label="Rendimiento"),
            ])
            vistas_disponibles = [dashboard_view, charts_view]

        # --- AppBar Dinámico ---
        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.STORAGE_ROUNDED, color=ft.colors.BLUE_400, size=28),
            leading_width=60,
            title=ft.Text("Mstar System", size=20, weight="bold"),
            bgcolor=ft.colors.BLACK26,
            actions=[
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, color=ft.colors.GREEN_400, size=12),
                        ft.Text(f"{nombre_usuario} ({rol_usuario})", color=ft.colors.WHITE70, size=13, weight="w500"),
                        # Botón para cerrar sesión
                        ft.IconButton(ft.Icons.LOGOUT, icon_color=ft.colors.RED_400, tooltip="Cerrar Sesión", on_click=cerrar_sesion)
                    ]),
                    padding=ft.padding.only(right=20)
                )
            ]
        )

        content_column = ft.Column(expand=True)
        content_area = ft.Container(content=content_column, expand=True, padding=20)

        # Controlador de navegación
        def nav_change(e):
            index = e.control.selected_index
            content_column.controls.clear()
            
            # Llamamos a la vista correspondiente de nuestra lista dinámica
            vista_seleccionada = vistas_disponibles[index]
            
            # Le pasamos stats si la vista lo requiere (charts o sql)
            if vista_seleccionada in [charts_view, sql_view]:
                content_column.controls.append(vista_seleccionada(page, stats))
            else:
                content_column.controls.append(vista_seleccionada(page))
                
            page.update()

        sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            bgcolor=ft.colors.BLACK26,
            min_width=100,
            group_alignment=-0.95,
            destinations=destinos_menu,
            on_change=nav_change,
        )

        content_column.controls.append(dashboard_view(page))
        page.add(ft.Row([sidebar, ft.VerticalDivider(width=1, color=ft.colors.WHITE10), content_area], expand=True, spacing=0))
        page.update()

    # --- Función para Cerrar Sesión ---
    def cerrar_sesion(e):
        page.appbar = None # Quitamos la barra de arriba
        page.controls.clear()
        page.add(login_view(page, cargar_interfaz_principal))
        page.update()


    page.add(login_view(page, cargar_interfaz_principal))

if __name__ == "__main__":
    ft.app(target=main)