from flet import Page, ThemeMode, Theme, ColorScheme, TextButton, SafeArea, CrossAxisAlignment, Column, app
from os.path import dirname, realpath

from .browser_widgets import BrowserList

path = dirname(realpath(__file__)).replace('\\flet_ui', '')

titles = [
    'Google Chrome',
    'Microsoft Edge',
    'Internet Explorer',
    'Mozilla Firefox',
    'Yandex Browser',
    'Chromium-Gost']

browser_path_png = 'browsers\\'

icons = [
         f'{browser_path_png}chrome.png',
         f'{browser_path_png}edge.png',
         f'{browser_path_png}explorer.png',
         f'{browser_path_png}firefox.png',
         f'{browser_path_png}yandex.png',
         f'{browser_path_png}browser.png',]


def main(page: Page, clearPassword):
    init_statuses:list = clearPassword.get_statuses(titles)
    init_existances:list = clearPassword.get_existances(titles)
    
    #Настройки окна
    page.title = 'Browser Password Cleaner'
    page.theme_mode = ThemeMode.DARK
    page.window_maximizable = False
    page.window_minimizable = False
    page.window_width = 400
    page.window_height = 550
    page.window_resizable = False
    page.theme = Theme(color_scheme=ColorScheme(primary='purple'))
    page.window_center()
    
    def check_btn(statuses):
        if all(statuses): 
            clear_btn.disabled = True
    
    def clear_click(e):
        clearPassword.remove_all_passwords()
        statuses = clearPassword.get_statuses(titles)
        browser_list.update_statuses(statuses)
        check_btn(statuses)
        clear_btn.update()
    
    browser_list = BrowserList(titles, icons, init_statuses, init_existances)
    clear_btn = TextButton("Очистить", on_click=clear_click)
    check_btn(init_statuses)
   
        
    page.add(SafeArea(
        expand=1,
        content=Column(horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                browser_list,
                clear_btn
            ]),
    ))


def start_app(clearPassword):
    assets_path = f'{path}\\assets'
    app(lambda page: main(page, clearPassword), assets_dir=assets_path)