import flet as ft
from db_config import validar_login
import time

def login_view(page: ft.Page, on_login_success):
    # --- Componentes del Formulario ---
    user_input = ft.TextField(
        label="Usuario de MariaDB", 
        prefix_icon=ft.Icons.PERSON,
        border_radius=12,
        bgcolor=ft.colors.BLACK12,
        width=320
    )
    
    pass_input = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        border_radius=12,
        bgcolor=ft.colors.BLACK12,
        width=320,
        on_submit=lambda _: validar_credenciales(None) # Permite dar Enter para entrar
    )
    
    # Contenedor para mensajes de error
    error_text = ft.Text("", color=ft.colors.RED_400, size=13, weight="bold")
    error_container = ft.Container(content=error_text, visible=False)
    
    # Botón de acceso
    btn_login = ft.ElevatedButton(
        "Conectar al Servidor", 
        icon=ft.Icons.LOGIN_ROUNDED,
        width=320,
        height=45,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    def validar_credenciales(e):
        if not user_input.value or not pass_input.value:
            error_text.value = "⚠️ Ingresa usuario y contraseña."
            error_container.visible = True
            page.update()
            return

        btn_login.text = "Validando en servidor..."
        btn_login.disabled = True
        page.update()
        
        # 🔌 AQUÍ ESTÁ LA MAGIA: Llamamos a MariaDB de verdad
        exito, rol_detectado, msg = validar_login(user_input.value, pass_input.value)
        
        if exito:
            # Login Exitoso! Entramos con el rol que MariaDB nos dio
            on_login_success(rol_detectado, user_input.value)
        else:
            # Login Fallido
            error_text.value = msg
            error_container.visible = True
            btn_login.text = "Conectar al Servidor"
            btn_login.disabled = False
            page.update()

    btn_login.on_click = validar_credenciales

    # --- Diseño Final (Tarjeta Centrada) ---
    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Card(
            elevation=10,
            color=ft.colors.BLACK26,
            content=ft.Container(
                padding=40,
                content=ft.Column([
                    ft.Icon(ft.Icons.STORAGE_ROUNDED, size=70, color=ft.colors.BLUE_400),
                    ft.Text("Mstar Admin Panel", size=26, weight="bold"),
                    ft.Text("Ingresa tus credenciales del servidor", color=ft.colors.WHITE70, size=14),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    user_input,
                    pass_input,
                    error_container,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    btn_login
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
                )
            )
        )
    )