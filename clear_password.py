
class ClearPassword:

    #! Ключи можешь найти в файле main.py
    
    #TODO: Реализовать существует ли браузер по ключу
    def __get_existance(self, key:str) -> bool: 
        return False
    
    #TODO: Реализовать очищен ли браузер по ключу
    def __get_status(self, key:str) -> bool:
        return False
    
    def get_existances(self, keys:list):
        return list(map(self.__get_existance, keys))
    
    def get_statuses(self, keys:list):
        return list(map(self.__get_status, keys))
    
    #TODO: Реализовать очистку всех паролей
    def delete_passwords(self):
        pass
    
    