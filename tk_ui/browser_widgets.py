from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkCheckBox, BooleanVar, CTkButton
from PIL.Image import open as image_open 

class BrowserTile(CTkFrame):
    def __init__(self, master, title:str, browser_icon_str:str, folder_icon_str:str, status:bool, isExist, update_function):
        super().__init__(master, fg_color="transparent", width=0, height=0)

        self.update_function = update_function
        browser_icon = CTkImage(light_image=image_open(browser_icon_str), dark_image=image_open(browser_icon_str), size=(50,50))
        folder_icon = CTkImage(light_image=image_open(folder_icon_str), dark_image=image_open(folder_icon_str), size=(10,10))
        
        texts = CTkFrame(self)
        self.leading = CTkLabel(self, image=browser_icon, text='')
        
        self.title = CTkLabel(texts, text=title)
        self.isExist = isExist
        self.open_file_btn = CTkButton(texts, text='', hover_color='purple',image=folder_icon, command=self.update_path_in_reg, fg_color="transparent", width=0)

        self.checked = BooleanVar(value=status)
        text = 'Очищен' if status else 'Не очищен' if isExist else '' 

        self.check_text = CTkLabel(self, text=text)
        self.trailing = CTkCheckBox(self,  state='disabled', width=0, variable=self.checked, text='', checkmark_color='grey', fg_color='purple')
        
        ex_text = "Не установлен" if not self.isExist else "Установлен"
        color = "grey" if not self.isExist else "purple"
        self.subtitle = CTkLabel(texts, text=ex_text, text_color=color)
        
        self.title.grid(row=0, column=1, sticky='ew')
        self.subtitle.grid(row=1, column=1, sticky='ew')
        if not self.isExist:
            self.open_file_btn.grid(row=1, column=2, sticky='ew')
        
        self.leading.pack(padx=5, pady=5, side="left")
        texts.pack(side="left")
        self.trailing.pack(side="right", padx=5, pady=5)
        self.check_text.pack(side="right", padx=5, pady=5)
        
    def update_existance_and_text(self, existance):
        self.isExist = existance
        self.open_file_btn.destroy()
        
        ex_text = "Не установлен" if not self.isExist else "Установлен"
        color = "grey" if not self.isExist else "purple"
        self.subtitle.configure(text=ex_text)
        self.subtitle.configure(text_color=color)
        
    def update_status_and_text(self, status):
        text = 'Очищен' if status else 'Не очищен' if self.isExist else '' 
        self.check_text.configure(text=text)
        self.checked.set(status)
    
    def update_path_in_reg(self):
        self.update_function(self.title.cget('text'))
        
class BrowserList(CTkFrame):
    def __init__(self, master, titles:list, icons:list, init_statuses:list, init_existances:list, folder_icon_str:str, update_function):
        super().__init__(master=master)
        self.__statuses = init_statuses
        self.titles = titles
        self.icons = icons
        self.__existances = init_existances
        self.folder_icon_str = folder_icon_str
        self.update_function = update_function
        self.build_list()
    
    def build_list(self):
        self.controls=[
            BrowserTile(self, t, i, self.folder_icon_str, s, e, self.update_function) for t, i, s, e in zip(self.titles, self.icons, self.__statuses, self.__existances)
        ] 
        
        for control in self.controls:
            control.pack(fill='both', padx=10, pady=5)
    
    def update_s_e(self, statuses, existances):
        self.__statuses = statuses
        self.__existances = existances
        
        for control, status, existance in zip(self.controls, self.__statuses, self.__existances):
            control.update_existance_and_text(existance)
            control.update_status_and_text(status)
            