import flet as ft
from db_config import get_connection, gestionar_usuario, listar_usuarios_con_roles, eliminar_usuario

def users_view(page: ft.Page):
    # --- 1. Estilizado del Formulario (Lado Izquierdo) ---
    user_input = ft.TextField(
        label="Nombre de Usuario", 
        width=300, 
        prefix_icon=ft.Icons.PERSON,
        border_radius=12,
        bgcolor=ft.colors.BLACK12
    )
    
    pass_input = ft.TextField(
        label="Contraseña", 
        width=300, 
        password=True, 
        can_reveal_password=True, 
        prefix_icon=ft.Icons.LOCK,
        border_radius=12,
        bgcolor=ft.colors.BLACK12
    )
    
    rol_dropdown = ft.Dropdown(
        label="Nivel de Privilegios", 
        width=300,
        prefix_icon=ft.Icons.SHIELD,
        border_radius=12,
        bgcolor=ft.colors.BLACK12,
        options=[
            ft.dropdown.Option("Acceso Total (Admin)"),
            ft.dropdown.Option("Solo Respaldos"),
            ft.dropdown.Option("Solo Lectura"),
        ]
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

    # --- 2. Estilizado de la Tabla (Lado Derecho) ---
    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Usuario", weight="bold")),
            ft.DataColumn(ft.Text("Rol Asignado", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        rows=[],
        border=ft.border.all(1, ft.colors.WHITE10),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.WHITE10),
        heading_row_color=ft.colors.BLACK26,
    )

    table_holder = ft.Column([users_table], scroll=ft.ScrollMode.AUTO, height=350)

    # --- 3. Lógica de Negocio ---
    def refrescar_lista():
        users_table.rows.clear()
        datos = listar_usuarios_con_roles()
        for u in datos:
            es_admin = u["rol"] == "Acceso Total"
            # Destacamos visualmente a los administradores
            color_rol = ft.colors.BLUE_400 if es_admin else ft.colors.WHITE70
            
            users_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(u["user"], weight="bold" if es_admin else "normal")),
                    ft.DataCell(ft.Text(u["rol"], color=color_rol)),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.colors.RED_400 if not es_admin else ft.colors.WHITE10,
                            disabled=es_admin, # Protegemos al admin
                            tooltip="Revocar Acceso" if not es_admin else "Protegido por el sistema",
                            on_click=lambda _, usr=u["user"], hst=u["host"]: borrar_click(usr, hst)
                        )
                    ),
                ])
            )
        page.update()

    def borrar_click(usuario, host):
        exito, msg = eliminar_usuario(usuario, host) 
        if exito:
            mostrar_mensaje(f"✅ {msg}", ft.colors.GREEN_400)
            refrescar_lista()
        else:
            mostrar_mensaje(f"❌ Error: {msg}", ft.colors.RED_400)

    def crear_click(e):
        if not user_input.value or not pass_input.value or not rol_dropdown.value:
            mostrar_mensaje("⚠️ Completa todos los campos para continuar.", ft.colors.ORANGE)
            return

        mostrar_mensaje("⏳ Configurando permisos en el servidor...", ft.colors.BLUE_200)
        conn = get_connection()
        exito, msg = gestionar_usuario(conn, user_input.value, pass_input.value, rol_dropdown.value)
        conn.close()
        
        if exito:
            mostrar_mensaje(f"✅ {msg}", ft.colors.GREEN_400)
            user_input.value = ""
            pass_input.value = ""
            rol_dropdown.value = None
            refrescar_lista()
        else:
            mostrar_mensaje(f"❌ Error: {msg}", ft.colors.RED_400)

    # Carga inicial
    refrescar_lista()

    # --- 4. Construcción de la UI ---
    return ft.Column([
        # Cabecera
        ft.Row([
            ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, size=40, color=ft.colors.CYAN_400),
            ft.Column([
                ft.Text("Gestión de Usuarios", size=28, weight="bold"),
                ft.Text("Administración de credenciales y roles de acceso", color=ft.colors.WHITE70),
            ], spacing=0)
        ]),
        
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),

        # Layout dividido (Izquierda: Crear / Derecha: Lista)
        ft.Row([
            # Panel Izquierdo (Crear Usuario)
            ft.Card(
                content=ft.Container(
                    padding=25,
                    content=ft.Column([
                        ft.Text("Nuevo Acceso", size=18, weight="bold"),
                        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                        user_input, 
                        pass_input, 
                        rol_dropdown,
                        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Crear Usuario", 
                            icon=ft.Icons.PERSON_ADD_ROUNDED,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.CYAN_700,
                                color=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=crear_click
                        ),
                        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                        status_container
                    ], spacing=10)
                ),
                elevation=3,
            ),
            
            # Panel Derecho (Lista de Usuarios) - Con expand=True para que tome el resto del espacio
            ft.Card(
                content=ft.Container(
                    padding=25,
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Directorio Activo", size=18, weight="bold"),
                            ft.IconButton(
                                icon=ft.Icons.REFRESH_ROUNDED, 
                                icon_color=ft.colors.CYAN_400,
                                tooltip="Actualizar lista",
                                on_click=lambda _: refrescar_lista()
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                        
                        ft.Container(
                            content=table_holder, 
                            bgcolor=ft.colors.BLACK12, 
                            padding=10, 
                            border_radius=10,
                            expand=True
                        ),
                    ])
                ),
                elevation=3,
                expand=True
            )
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
    ], expand=True, spacing=10)