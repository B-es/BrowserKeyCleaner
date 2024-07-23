
class ClearPassword:

    def __get_existance(self, key:str) -> bool:
        pass
    
    def __get_status(self, key:str) -> bool:
        pass
    
    def get_existances(self, keys:list):
        return list(map(self.__get_existance, keys))
    
    def get_statuses(self, keys:list):
        return list(map(self.__get_status, keys))
    
    def delete_passwords(self):
        pass
    
    