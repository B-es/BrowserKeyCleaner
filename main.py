import flet as ft

from browser_widgets import BrowserList
from clear_password import ClearPassword

keys = [
    'chrome',
    'edge',
    'explorer',
    'firefox',
    'yandex',
    'gost',]

titles = [
    'Google Chrome',
    'Microsoft Edge',
    'Internet Explorer',
    'Mozilla Firefox',
    'Yandex Browser',
    'Chromium-Gost']

browser_path_png = '/browsers/'

icons = [
         f'{browser_path_png}chrome.png',
         f'{browser_path_png}edge.png',
         f'{browser_path_png}explorer.png',
         f'{browser_path_png}firefox.png',
         f'{browser_path_png}yandex.png',
         f'{browser_path_png}browser.png',]

const_browser_titles = dict(zip(keys, titles))
const_browser_icons = dict(zip(keys, icons))



def main(page: ft.Page):
    clearPassword = ClearPassword()
    init_statuses:list = clearPassword.get_statuses(keys)
    init_existances:list = clearPassword.get_existances(keys)
    
    #Настройки окна
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximizable = False
    page.window_minimizable = False
    page.window_width = 400
    page.window_height = 550
    page.window_resizable = False
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary='purple'))
    page.window_center()
    
    def clear_click(e):
        clearPassword.delete_passwords()
        statuses = clearPassword.get_statuses(keys)
        browser_list.update_statuses(statuses)
    
    browser_list = BrowserList(titles, icons, init_statuses, init_existances)
    clear_btn = ft.TextButton("Очистить", on_click=clear_click)
        
    page.add(ft.SafeArea(
        expand=1,
        content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                browser_list,
                clear_btn
            ]),
    ))

if __name__ == '__main__':
    ft.app(main, assets_dir='assets')
