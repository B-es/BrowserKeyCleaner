from customtkinter import CTk, CTkButton
from tk_ui.browser_widgets import BrowserList

class App(CTk):
    
    browser_path_png = 'browsers\\'

    icons = [
            f'{browser_path_png}chrome.png',
            f'{browser_path_png}edge.png',
            f'{browser_path_png}explorer.png',
            f'{browser_path_png}firefox.png',
            f'{browser_path_png}yandex.png',
            f'{browser_path_png}browser.png',]
    
    titles = [
    'Google Chrome',
    'Microsoft Edge',
    'Internet Explorer',
    'Mozilla Firefox',
    'Yandex',
    'Chromium-Gost']
    
    def __init__(self, path:str, title:str, geometry:str, icon:str, clearPassword):
        super().__init__()
        self.path = path
        
        self.title(title)
        self.geometry(geometry)
        self.wm_iconbitmap(icon)
        self.resizable(width=False, height=False)
        
        init_statuses:list = clearPassword.get_statuses(self.titles)
        init_existances:list = clearPassword.get_existances(self.titles) 
        
        def clear_click():
            #clearPassword.remove_all_passwords()
            statuses:list = clearPassword.get_statuses(self.titles)
            existances:list = clearPassword.get_existances(self.titles) 
            print(statuses)
            browserList.update_statuses(statuses)
            check_btn(statuses, existances)
            
        def check_btn(statuses, existances):
            checks = []
            for s, e in zip(statuses, existances):
                if s:
                    checks.append(s)
                elif not e:
                    checks.append(not e)
                else:
                    checks.append(False)
            
            if all(checks): 
                clear_btn.configure(state='disabled')
            else:
                clear_btn.configure(state='enabled')
                
        clear_btn = CTkButton(self, text="Очистить", command=clear_click)
        check_btn(init_statuses, init_existances)
        
        browserList = BrowserList(self, self.titles, list(map(self.__get_path, self.icons)), init_statuses, init_existances)
        
        browserList.pack(fill='both')
        clear_btn.pack(expand=True, ipadx=10, ipady=5)
        
    def __get_path(self, file):
        return f"{self.path}\\{file}".replace('\\', '/')