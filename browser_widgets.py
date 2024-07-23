import flet as ft

class BrowserTile(ft.ListTile):
    def __init__(self, title:str, icon:str, status:bool=False, isExist=False):
        super().__init__()
        self.title = ft.Text(title)
        self.leading = ft.Image(src=icon)
        self.trailing = ft.Icon(ft.icons.DONE if status else ft.icons.BLOCK)
        self.subtitle = ft.Text("Не установлен") if not isExist else ft.Text("Установлен")

class BrowserList(ft.ListView):
    def __init__(self, titles:list[str], icons:list[str], init_statuses:list[bool], init_existances:list[bool]):
        super().__init__()
        self.__statuses = init_statuses
        
        self.controls=[
            BrowserTile(t, i, s, e) for t, i, s, e in zip(titles, icons, self.__statuses, init_existances)
        ]   
        print()
    
    def update_statuses(self, statuses):
        self.__statuses = statuses
        self.update()