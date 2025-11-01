import flet as ft
import flet_pages
import flet_pages.i18n as i18n_module
from flet_pages.i18n import I18n
from pages import about, start, settings, theme_settings
import os
import sys
import tempfile

def get_pages():
    pages = [
        start.page,
        about.page,
        settings.page,
        theme_settings.page
    ]
    return pages

def check_single_instance():
    """检查是否已有实例运行，如果有则退出"""
    lock_file = os.path.join(tempfile.gettempdir(), "officeboxpy.lock")
    try:
        # 尝试创建锁文件
        lock_fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        os.write(lock_fd, str(os.getpid()).encode())
        # 不要关闭文件描述符，保持锁定
        return lock_fd
    except OSError:
        # 锁文件已存在，说明已有实例运行
        try:
            with open(lock_file, 'r') as f:
                pid = f.read().strip()
            # 检查进程是否真的在运行
            try:
                os.kill(int(pid), 0)  # 发送信号0来检查进程是否存在
                print(f"应用已在运行 (PID: {pid})，退出当前实例。")
                sys.exit(1)
            except OSError:
                # 进程不存在，删除锁文件并继续
                try:
                    os.remove(lock_file)
                except:
                    pass
                # 重新尝试创建锁文件
                try:
                    lock_fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                    os.write(lock_fd, str(os.getpid()).encode())
                    return lock_fd
                except OSError:
                    print("无法创建锁文件，退出当前实例。")
                    sys.exit(1)
        except:
            print("应用已在运行，退出当前实例。")
            sys.exit(1)

def main(page: ft.Page):
    global i18n_instance
    # 检查单实例锁
    lock_fd = check_single_instance()

    # 檢查配置文件中的語言設置
    import json
    config_path = "./.config/i18n_config.json"
    default_lang = "en"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                default_lang = config.get("lang", "en")
        except:
            pass

    # 从JSON文件加载翻译
    import json
    translations_path = "./.config/translations.json"
    with open(translations_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    i18n_instance = I18n(translations, default_lang, "./.config", True)

    # 应用UI颜色设置
    ui_config_path = "./.config/ui_config.json"
    primary_color = "#1976D2"  # 默认蓝色
    if os.path.exists(ui_config_path):
        try:
            with open(ui_config_path, 'r', encoding='utf-8') as f:
                ui_config = json.load(f)
                primary_color = ui_config.get("primary_color", "#1976D2")
        except:
            pass

    page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=primary_color))
    page.title = "OfficeBoxPy"
    page.window.icon = "public/logo.png"
    pages = get_pages()
    ui = flet_pages.pages(pages, page, False)

    # 应用关闭时清理锁文件
    def on_close(e):
        try:
            lock_file = os.path.join(tempfile.gettempdir(), "officeboxpy.lock")
            if os.path.exists(lock_file):
                os.remove(lock_file)
        except:
            pass

    page.on_close = on_close

ft.app(main)