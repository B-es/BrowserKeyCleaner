from customtkinter import CTk, CTkButton, StringVar, set_appearance_mode, filedialog
from tktooltip import ToolTip
from tk_ui.browser_widgets import BrowserList
from threading import Thread

class App(CTk):
    set_appearance_mode('dark')
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
    
    tip = '''
    Внимание!!!
    Перед удалением программа сначала закроет все открытые браузеры,
    а затем начнётся удаление всех паролей на установленных браузерах.
    '''
    
    def __init__(self, path:str, title:str, geometry:str, icon:str, clearPassword):
        super().__init__()
        self.path = path
        
        self.title(title)
        self.geometry(geometry)
        self.wm_iconbitmap(icon)
        self.resizable(width=False, height=False)
        
        init_existances:list = clearPassword.get_existances(self.titles) 
        init_statuses:list = clearPassword.get_statuses(self.titles)
        
        
        def clear_click():
            clear_btn_text.set('Очищается...')
            clear_btn.configure(state='disabled', require_redraw=True)
            self.update_idletasks()
            clearPassword.remove_all_passwords()
            statuses:list = clearPassword.get_statuses(self.titles)
            existances:list = clearPassword.get_existances(self.titles) 
            browserList.update_s_e(statuses, existances)
            check_btn(statuses, existances)
            clear_btn_text.set('Очистить')
            
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

                
        clear_btn_text = StringVar(value="Очистить")
        clear_btn = CTkButton(self, textvariable=clear_btn_text, command=clear_click, fg_color='purple')
        check_btn(init_statuses, init_existances)
        
        ToolTip(clear_btn, msg=self.tip, delay=0.02,
        parent_kwargs={"bg": "purple", "padx": 2, "pady": 2},
        fg="#ffffff", bg="#1c1c1c", padx=10, pady=10)
        
        def update_function(browser_name):
            title = 'Выберите исполнительный файл(.exe) браузера'
            file_types = [("Исполнительный файл", "*.exe")]
            exe_path = filedialog.askopenfilename(title=title, filetypes=file_types, defaultextension='.exe')
            if not exe_path: return
            clearPassword.save_path_browser(browser_name, exe_path)
            existances:list = clearPassword.get_existances(self.titles) 
            statuses:list = clearPassword.get_statuses(self.titles)
            browserList.update_s_e(statuses, existances)
            check_btn(statuses, existances)
        
        browserList = BrowserList(self, self.titles, list(map(self.__get_path, self.icons)), init_statuses, init_existances, self.__get_path('folder_icon.png'), update_function)
        
        browserList.pack(fill='both')
        clear_btn.pack(expand=True, ipadx=10, ipady=5)
        
    def __get_path(self, file):
        return f"{self.path}\\{file}".replace('\\', '/')