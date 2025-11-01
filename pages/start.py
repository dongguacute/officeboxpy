import flet as ft
import flet_pages
import time
from flet_pages.router import PageMeta
from flet_pages.i18n import t

def get_start_content(ui: flet_pages.pages):
    # Get current theme mode for dynamic styling
    is_dark = ui.the_page.theme_mode == ft.ThemeMode.DARK

    def toggle_theme(e):
        ui.the_page.theme_mode = ft.ThemeMode.DARK if ui.the_page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        ui.the_page.update()

    co = ft.Container(
        content=ft.Column(
            [
                # Logo
                ft.Container(
                    content=ft.Image(
                        src="public/logo.png",
                        width=150,
                        height=150,
                        border_radius=75,  # 圆角
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    margin=ft.margin.only(bottom=20),
                ),
                ft.Text("OfficeBoxPy", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(t("hello") + " " + t("world"), size=18, color="#666666" if not is_dark else "#CCCCCC"),
                ft.Container(height=30),  # Spacer
                ft.ElevatedButton(t("switch_to_start"), on_click=lambda e: ui.change_page_by_label("about")),
                ft.ElevatedButton(t("settings"), on_click=lambda e: ui.change_page_by_label("settings")),
                ft.ElevatedButton(t("theme_settings"), on_click=lambda e: ui.change_page_by_label("theme_settings")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.alignment.center,
        bgcolor="#FFFFFF" if not is_dark else "#1E1E1E",
        padding=ft.padding.all(30),
    )
    return co

page = PageMeta(
    label="start",
    func=get_start_content,
    title=lambda: t("start"),
)