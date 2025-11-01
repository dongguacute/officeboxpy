import flet as ft
import flet_pages
import sys
from flet_pages.router import PageMeta
from flet_pages.i18n import t, I18n

def get_settings_content(ui: flet_pages.pages):
    # Get current theme mode for dynamic styling
    is_dark = ui.the_page.theme_mode == ft.ThemeMode.DARK
    def change_language(e):
        # 更新配置文件並重新初始化 i18n
        import json
        import os
        from flet_pages.i18n import I18n

        config_path = "./.config/i18n_config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        config = {"lang": e.control.value}
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f)

        # 从JSON文件重新加载翻译并重新创建i18n实例
        import json
        translations_path = "./.config/translations.json"
        with open(translations_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        global i18n_instance
        i18n_instance = I18n(translations, e.control.value, "./.config", True)

        # 強制重新加載所有頁面
        ui.update_pages()
        ui.the_page.update()

    # 获取当前语言
    import json
    import os
    config_path = "./.config/i18n_config.json"
    current_lang = "en"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                current_lang = config.get("lang", "en")
        except:
            pass

    language_dropdown = ft.Dropdown(
        label=t("language"),
        options=[
            ft.dropdown.Option("zh-CN", "中文(简体)"),
            ft.dropdown.Option("zh-TW", "中文(繁體)"),
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("ja", "日本語"),
            ft.dropdown.Option("fr", "Français"),
        ],
        value=current_lang,
        on_change=change_language,
    )

    co = ft.Container(
        content=ft.Column(
            [
                # Header
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon("settings", size=32, color="#000000" if not is_dark else "#FFFFFF"),
                            ft.Text(t("settings"), size=28, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    margin=ft.margin.only(bottom=30),
                ),

                # Language Section
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon("language", size=24, color="#000000" if not is_dark else "#FFFFFF"),
                                        ft.Text(t("language"), size=18, weight=ft.FontWeight.W_600),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=10,
                                ),
                                margin=ft.margin.only(bottom=15),
                            ),
                            ft.Container(
                                content=language_dropdown,
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

                # Theme Settings Section
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon("palette", size=24, color="#000000" if not is_dark else "#FFFFFF"),
                                        ft.Text(t("theme_settings"), size=18, weight=ft.FontWeight.W_600),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=10,
                                ),
                                margin=ft.margin.only(bottom=15),
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row(
                                        [
                                            ft.Icon("arrow_forward", size=20),
                                            ft.Text(t("theme_settings"), size=16),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=8,
                                    ),
                                    on_click=lambda e: ui.change_page_by_label("theme_settings"),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        bgcolor="#E3F2FD" if not is_dark else "#1E3A5F",
                                        color="#1976D2" if not is_dark else "#64B5F6",
                                    ),
                                    height=50,
                                    width=200,
                                ),
                                alignment=ft.alignment.center_left,
                            ),
                        ],
                        spacing=0,
                    ),
                    margin=ft.margin.only(bottom=30),
                ),

                # Back Button
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon("arrow_back", size=20),
                                ft.Text(t("back"), size=16),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        on_click=lambda e: ui.change_page_by_label("start"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                        height=50,
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
    label="settings",
    func=get_settings_content,
    title=lambda: t("settings"),
)