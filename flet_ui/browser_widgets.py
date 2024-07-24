from flet import ListTile, ListView, Text, Icon, Image, icons

class BrowserTile(ListTile):
    def __init__(self, title:str, icon:str, status:bool=False, isExist=False):
        super().__init__()
        self.title = Text(title)
        self.leading = Image(src=icon)
        self.trailing = Icon(icons.DONE if status else icons.BLOCK)
        self.subtitle = Text("Не установлен") if not isExist else Text("Установлен")

class BrowserList(ListView):
    def __init__(self, titles:list[str], icons:list[str], init_statuses:list[bool], init_existances:list[bool]):
        super().__init__()
        self.__statuses = init_statuses
        self.titles = titles
        self.icons = icons
        self.init_existances = init_existances
        self.build_list()
    
    def build_list(self):
        self.controls=[
            BrowserTile(t, i, s, e) for t, i, s, e in zip(self.titles, self.icons, self.__statuses, self.init_existances)
        ] 
    
    def update_statuses(self, statuses):
        self.__statuses = statuses
        self.build_list()
        self.update()