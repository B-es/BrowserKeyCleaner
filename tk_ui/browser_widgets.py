from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkCheckBox, BooleanVar
from PIL.Image import open as image_open 

class BrowserTile(CTkFrame):
    def __init__(self, master, title:str, icon:str, status:bool=False, isExist=False):
        super().__init__(master, fg_color="transparent", width=0, height=0)

        image = CTkImage(light_image=image_open(icon), dark_image=image_open(icon), size=(50,50))
        
        texts = CTkFrame(self)
        self.leading = CTkLabel(self, image=image, text='')
        self.title = CTkLabel(texts, text=title)
        self.isExist = isExist

        self.checked = BooleanVar(value=status)
        text = 'Очищен' if status else 'Не очищен' if isExist else '' 

        self.check_text = CTkLabel(self, text=text)
        self.trailing = CTkCheckBox(self,  state='disabled', width=0, variable=self.checked, text='', checkmark_color='purple', fg_color='grey')
        
        ex_text = "Не установлен" if not isExist else "Установлен"
        color = "grey" if not isExist else "purple"
        self.subtitle = CTkLabel(texts, text=ex_text, text_color=color)
        
        self.title.grid(row=0, column=1, sticky='ew')
        self.subtitle.grid(row=1, column=1, sticky='ew')
        
        self.leading.pack(padx=5, pady=5, side="left")
        texts.pack(side="left")
        self.trailing.pack(side="right", padx=5, pady=5)
        self.check_text.pack(side="right", padx=5, pady=5)
        
    def update_status_and_text(self, status):
        text = 'Очищен' if status else 'Не очищен' if self.isExist else '' 
        self.check_text.configure(text=text)
        self.checked.set(status)
        
class BrowserList(CTkFrame):
    def __init__(self, master, titles:list[str], icons:list[str], init_statuses:list[bool], init_existances:list[bool]):
        super().__init__(master=master)
        self.__statuses = init_statuses
        self.titles = titles
        self.icons = icons
        self.init_existances = init_existances
        self.build_list()
    
    def build_list(self):
        self.controls=[
            BrowserTile(self, t, i, s, e) for t, i, s, e in zip(self.titles, self.icons, self.__statuses, self.init_existances)
        ] 
        
        for control in self.controls:
            control.pack(fill='both', padx=10, pady=5)
    
    def update_statuses(self, statuses):
        self.__statuses = statuses
        
        for control, status in zip(self.controls, self.__statuses):
            control.update_status_and_text(status)