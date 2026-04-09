import flet as ft
import plotly.graph_objects as go
from flet.plotly_chart import PlotlyChart 
from db_config import obtener_bases_datos, obtener_tamano_tablas

def charts_view(page: ft.Page, stats):
    # --- 1. Estilizado de las Tarjetas de Métricas ---
    def crear_metrica(titulo, valor, icono, color_base):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icono, color=color_base, size=35),
                ft.Column([
                    ft.Text(titulo, size=12, color=ft.colors.WHITE70, weight="w400"),
                    ft.Text(str(valor), size=28, weight="bold", color=ft.colors.WHITE),
                ], spacing=0)
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.colors.WHITE10,
            padding=20,
            border_radius=15,
            expand=True,
            border=ft.border.all(1, ft.colors.with_opacity(0.1, color_base)),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.05, color_base))
        )

    # --- 2. Selectores Estilizados ---
    db_dropdown = ft.Dropdown(
        label="Base de Datos a analizar",
        width=350,
        border_radius=12,
        bgcolor=ft.colors.BLACK12,
        prefix_icon=ft.Icons.ANALYTICS_OUTLINED,
        options=[ft.dropdown.Option(db) for db in obtener_bases_datos()]
    )

    chart_container = ft.Column(expand=True, horizontal_alignment="center")

    # --- 3. Lógica de la Gráfica (Refinada y Compacta) ---
    def generar_grafica(e):
        if not db_dropdown.value:
            return
        
        datos = obtener_tamano_tablas(db_dropdown.value)
        chart_container.controls.clear()

        if not datos:
            chart_container.controls.append(
                ft.Container(
                    content=ft.Text("⚠️ No se encontraron tablas con datos en esta BD.", color="orange"),
                    padding=50
                )
            )
        else:
            nombres = [d[0] for d in datos]
            tamanos = [d[1] for d in datos]

            fig = go.Figure(
                data=[go.Bar(
                    x=nombres, 
                    y=tamanos,
                    marker=dict(
                        color=tamanos,
                        colorscale='Viridis',
                        line=dict(color='#FFFFFF', width=0.5)
                    ),
                    text=tamanos,
                    texttemplate='%{text} MB',
                    textposition='outside',
                )]
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=30, b=80), # Margen inferior ajustado para los nombres
                height=210, # Altura fija estricta para Plotly
                autosize=True,
                xaxis=dict(
                    showgrid=False,
                    tickangle=45,
                    tickfont=dict(size=10) # Letra pequeña para que no empuje todo
                ),
                yaxis=dict(title="Tamaño (MB)", showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            )

            chart_container.controls.append(
                ft.Container(
                    content=PlotlyChart(fig, expand=False), # Quitamos el expand aquí
                    alignment=ft.alignment.center,
                )
            )
        page.update()

    # --- 4. Construcción de la Interfaz ---
    return ft.Column([
        # Encabezado
        ft.Row([
            ft.Icon(ft.Icons.BAR_CHART_ROUNDED, size=40, color=ft.colors.AMBER_400),
            ft.Column([
                ft.Text("Monitor de Rendimiento", size=28, weight="bold"),
                ft.Text("Análisis de consultas y almacenamiento", color=ft.colors.WHITE70),
            ], spacing=0)
        ]),
        
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        
        # Tarjetas de Actividad
        ft.Row([
            crear_metrica("CONSULTAS EXITOSAS", stats["exitosas"], ft.Icons.CHECK_CIRCLE_OUTLINE, ft.colors.GREEN_400),
            crear_metrica("ERRORES DETECTADOS", stats["fallidas"], ft.Icons.ERROR_OUTLINE, ft.colors.RED_400),
        ], spacing=20),
        
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        
        # Panel de Control de Gráfica
        ft.Card(
            content=ft.Container(
                padding=15, # Padding reducido para dar más espacio
                content=ft.Column([
                    ft.Text("Distribución de Almacenamiento", size=16, weight="bold"),
                    ft.Row([
                        db_dropdown,
                        ft.ElevatedButton(
                            "Generar Reporte", 
                            icon=ft.Icons.PLAY_ARROW_ROUNDED,
                            on_click=generar_grafica,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.BLUE_700,
                                color=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        )
                    ], spacing=20),
                    
                    ft.Divider(height=10, color=ft.colors.WHITE10),
                    
                    # Contenedor de la gráfica (Tamaño Controlado en Flet)
                    ft.Container(
                        content=chart_container,
                        height=220, # Altura fija para que la gráfica no se desborde
                        alignment=ft.alignment.center,
                    )
                ])
            ),
            elevation=2
        )
    ], spacing=10, expand=True)