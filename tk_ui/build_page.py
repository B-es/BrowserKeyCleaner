from os.path import dirname, realpath
from .app import App

path = dirname(realpath(__file__)).replace('\\tk_ui', '')






#def main(clearPassword):
    
    # def check_btn(statuses):
    #     if all(statuses): 
    #         clear_btn.disabled = True
    
    # def clear_click(e):
    #     clearPassword.remove_all_passwords()
    #     statuses = clearPassword.get_statuses(titles)
    #     browser_list.update_statuses(statuses)
    #     check_btn(statuses)
    #     clear_btn.update()
    
    # browser_list = BrowserList(titles, icons, init_statuses, init_existances)
    # clear_btn = TextButton("Очистить", on_click=clear_click)
    # check_btn(init_statuses)


def start_app(clearPassword):
    title = 'Browser Password Cleaner'
    geometry = '350x500'
    assets_path = f'{path}\\assets'
    icon = assets_path + '\\' + 'icon.ico'

    app = App(assets_path, title, geometry, icon, clearPassword)
    app.mainloop()