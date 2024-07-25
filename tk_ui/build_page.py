from os.path import dirname, realpath
from .app import App

path = dirname(realpath(__file__)).replace('\\tk_ui', '')

def start_app(clearPassword):
    title = 'Browser Password Cleaner'
    geometry = '350x500'
    assets_path = f'{path}\\assets'
    icon = assets_path + '\\' + 'icon.ico'

    app = App(assets_path, title, geometry, icon, clearPassword)
    app.mainloop()