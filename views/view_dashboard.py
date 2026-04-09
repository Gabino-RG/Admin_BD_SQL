import flet as ft
from db_config import obtener_info_servidor

def dashboard_view(page: ft.Page):
    # Obtenemos la información real del servidor
    info = obtener_info_servidor()

    # Función auxiliar para crear tarjetas de estado
    def crear_tarjeta_info(titulo, valor, icono, color_accent):
        return ft.Container(
            content=ft.Column([
                ft.Icon(name=icono, color=color_accent, size=30),
                ft.Text(titulo, size=14, color=ft.colors.WHITE70, weight="w400"),
                ft.Text(valor, size=30, weight="bold", color=ft.colors.WHITE),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment="center"),
            width=250,
            height=160,
            # TRUCO: Gradiente sutil y bordes bien redondeados
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.WHITE10, ft.colors.BLACK12],
            ),
            border=ft.border.all(1, ft.colors.WHITE10),
            border_radius=20,
            padding=20,
            # TRUCO: Sombra para dar profundidad
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
            ),
        )

    # Creamos las tres tarjetas
    tarjeta_version = crear_tarjeta_info(
        "Versión de MariaDB", 
        info["version"].split("-")[0], # Limpiamos un poco el texto
        ft.icons.STORAGE, 
        ft.colors.BLUE_300
    )
    tarjeta_uptime = crear_tarjeta_info(
        "Tiempo de Actividad", 
        info["uptime"], 
        ft.icons.TIMER, 
        ft.colors.GREEN_300
    )
    tarjeta_dbs = crear_tarjeta_info(
        "Total de Bases de Datos", 
        str(info["dbs"]), 
        ft.icons.DATA_EXPLORATION, 
        ft.colors.AMBER_300
    )

    # El layout de la vista
    return ft.Column([
        # Bienvenida
        ft.Container(
            content=ft.Column([
                ft.Text("Bienvenido al Panel de Control", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Gestor Integral de Bases de Datos MariaDB", size=18, color=ft.colors.WHITE70),
            ], spacing=5),
            margin=ft.margin.only(bottom=20)
        ),
        
        ft.Divider(),
        
        # Resumen del Servidor
        ft.Text("Estado del Servidor de Base de Datos:", size=20, weight="bold"),
        ft.Row([
            tarjeta_version,
            tarjeta_uptime,
            tarjeta_dbs,
        ], spacing=25, alignment=ft.MainAxisAlignment.START),
        
        ft.Divider(),
        
        # Consejos rápidos
        ft.Container(
            content=ft.Column([
                ft.Text("Guía Rápida:", weight="bold", size=18),
                ft.Text("• Pestaña 'Respaldos': Para exportar e importar SQL.", color=ft.colors.WHITE70),
                ft.Text("• Pestaña 'CSV': Para mover datos de/hacia archivos planos.", color=ft.colors.WHITE70),
                ft.Text("• Pestaña 'Rendimiento': Visualiza el uso de disco de tus tablas.", color=ft.colors.WHITE70),
            ], spacing=10),
            bgcolor=ft.colors.BLACK12,
            padding=20,
            border_radius=10,
            margin=ft.margin.only(top=20),
            expand=True
        )
    ], spacing=20, expand=True)