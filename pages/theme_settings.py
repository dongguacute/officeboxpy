import flet as ft
import flet_pages
import sys
import os
import json
from flet_pages.router import PageMeta
from flet_pages.i18n import t, I18n

def get_theme_settings_content(ui: flet_pages.pages):
    # Get current theme mode for dynamic styling
    is_dark = ui.the_page.theme_mode == ft.ThemeMode.DARK

    def toggle_theme(e):
        ui.the_page.theme_mode = ft.ThemeMode.DARK if ui.the_page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        ui.the_page.update()
        # Re-render the page to apply theme changes
        ui.update_pages()
    def open_color_picker(e):
        nonlocal current_primary_color
        selected_color = current_primary_color
        selected_index = -1

        # 声明 color_picker_dialog 为 nonlocal，以便在内部函数中修改
        color_picker_dialog_instance = None

        def select_color(color, index):
            nonlocal selected_color, selected_index, color_buttons
            selected_color = color
            old_selected = selected_index
            selected_index = index

            if old_selected >= 0:
                color_buttons[old_selected].border = None
            color_buttons[selected_index].border = ft.border.all(3, "white")
            ui.the_page.update()

        def cancel_selection():
            nonlocal color_picker_dialog_instance
            if color_picker_dialog_instance:
                ui.the_page.close(color_picker_dialog_instance)
                ui.the_page.update()

        def save_color():
            nonlocal color_picker_dialog_instance
            if selected_color != current_primary_color:
                change_primary_color(selected_color)
            if color_picker_dialog_instance:
                ui.the_page.close(color_picker_dialog_instance)

            # 重啟整個應用以應用主題更改
            import subprocess
            import sys

            # 關閉對話框
            if color_picker_dialog_instance:
                ui.the_page.close(color_picker_dialog_instance)

            # 重新啟動應用
            subprocess.Popen([sys.executable] + sys.argv)

            # 關閉當前頁面/應用
            ui.the_page.window.destroy() if hasattr(ui.the_page, 'window') and hasattr(ui.the_page.window, 'destroy') else ui.the_page.update()

        color_options = [
            "#1976D2", "#4CAF50", "#FF9800", "#F44336", "#9C27B0",
            "#00BCD4", "#8BC34A", "#FFC107", "#FF5722", "#673AB7"
        ]

        color_buttons = []
        for i, color in enumerate(color_options):
            is_selected = color == current_primary_color
            if is_selected:
                selected_index = i
                selected_color = color

            color_buttons.append(
                ft.Container(
                    width=40,
                    height=40,
                    bgcolor=color,
                    border_radius=20,
                    border=ft.border.all(3, "white") if is_selected else None,
                    on_click=lambda e, c=color, idx=i: select_color(c, idx),
                    ink=True,
                )
            )

        color_picker_dialog_instance = ft.AlertDialog( # 使用新的变量名
            modal=True,
            title=ft.Text(t("theme_color")),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(t("select_color"), size=14),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(color_buttons[:5], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row(color_buttons[5:], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                                ],
                                spacing=15,
                            ),
                            padding=ft.padding.all(10),
                        ),
                    ],
                    spacing=15,
                    tight=True,
                ),
                width=350,
                height=180,
            ),
            actions=[
                ft.TextButton(t("cancel"), on_click=lambda e: cancel_selection()),
                ft.ElevatedButton(t("save"), on_click=lambda e: save_color()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        ui.the_page.open(color_picker_dialog_instance) # 使用新的变量名

    def change_primary_color(color):
        # 保存主色调到配置文件
        import json
        import os
        config_path = "./.config/ui_config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        config = {"primary_color": color}
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f)

        # 应用新颜色到主题
        ui.the_page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=color))
        ui.the_page.update()
        ui.update_pages()

    # 获取当前UI颜色设置
    ui_config_path = "./.config/ui_config.json"
    current_primary_color = "#1976D2"  # 默认蓝色
    if os.path.exists(ui_config_path):
        try:
            with open(ui_config_path, 'r', encoding='utf-8') as f:
                ui_config = json.load(f)
                current_primary_color = ui_config.get("primary_color", "#1976D2")
        except:
            pass

    co = ft.Container(
        content=ft.Column(
            [
                # Header
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon("palette", size=32, color="#000000" if not is_dark else "#FFFFFF"),
                            ft.Text(t("theme_settings"), size=28, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    margin=ft.margin.only(bottom=30),
                ),

                # Dark/Light Mode Section
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon("brightness_6", size=24, color="#000000" if not is_dark else "#FFFFFF"),
                                        ft.Text(t("dark_light_mode"), size=18, weight=ft.FontWeight.W_600),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=10,
                                ),
                                margin=ft.margin.only(bottom=15),
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(t("theme_switch"), size=16),
                                        ft.Switch(
                                            value=ui.the_page.theme_mode == ft.ThemeMode.DARK,
                                            on_change=toggle_theme,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                border=ft.border.all(1, "#E0E0E0" if not is_dark else "#404040"),
                                border_radius=12,
                                bgcolor="#F8F9FA" if not is_dark else "#2D2D2D",
                            ),
                        ],
                        spacing=0,
                    ),
                    margin=ft.margin.only(bottom=25),
                ),

                # Theme Color Section
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon("color_lens", size=24, color="#000000" if not is_dark else "#FFFFFF"),
                                        ft.Text(t("theme_color"), size=18, weight=ft.FontWeight.W_600),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=10,
                                ),
                                margin=ft.margin.only(bottom=15),
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(t("primary_color"), size=14, weight=ft.FontWeight.W_500),
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.Container(
                                                        width=60,
                                                        height=40,
                                                        bgcolor=current_primary_color,
                                                        border_radius=8,
                                                        border=ft.border.all(2, "#CCCCCC"),
                                                    ),
                                                    ft.ElevatedButton(
                                                        content=ft.Row(
                                                            [
                                                                ft.Icon("edit", size=18),
                                                                ft.Text(t("change"), size=14),
                                                            ],
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            spacing=6,
                                                        ),
                                                        on_click=lambda e: open_color_picker(e),
                                                        style=ft.ButtonStyle(
                                                            shape=ft.RoundedRectangleBorder(radius=8),
                                                        ),
                                                        height=40,
                                                    ),
                                                ],
                                                spacing=15,
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            padding=ft.padding.symmetric(horizontal=15, vertical=10),
                                            border_radius=12,
                                            bgcolor="#F8F9FA" if not is_dark else "#2D2D2D",
                                        ),
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                padding=ft.padding.all(20),
                                border=ft.border.all(1, "#E0E0E0" if not is_dark else "#404040"),
                                border_radius=15,
                                bgcolor="#FFFFFF" if not is_dark else "#2D2D2D",
                            ),
                        ],
                        spacing=0,
                    ),
                    margin=ft.margin.only(bottom=30),
                ),

                # Warning and Back Button
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon("warning", size=20, color="#FF9800"),
                                        ft.Text(t("restart_warning"), size=14, color="#FF9800", weight=ft.FontWeight.W_500),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=8,
                                ),
                                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                                border=ft.border.all(1, "#FF9800"),
                                border_radius=8,
                                bgcolor="#FFF8E1",
                                margin=ft.margin.only(bottom=15),
                            ),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon("arrow_back", size=20),
                                        ft.Text(t("back_to_settings"), size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=8,
                                ),
                                on_click=lambda e: ui.change_page_by_label("settings"),
                                height=50,
                            ),
                        ],
                        spacing=0,
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        ),
        padding=ft.padding.all(30),
        alignment=ft.alignment.top_center,
        bgcolor="#FFFFFF" if not is_dark else "#1E1E1E",
    )
    return co

page = PageMeta(
    label="theme_settings",
    func=get_theme_settings_content,
    title=lambda: t("theme_settings"),
)