from termcolor import colored
import browsers
import os

class BrowserManager:

    __default_browser_password_paths = {
        'Google Chrome': [r"\Local\Google\Chrome\User Data\Default\Login Data", r"\Local\Google\Chrome\User Data\Default\Login Data For Account"],
        'Microsoft Edge': [r"\Local\Microsoft\Edge\User Data\Default\Login Data"],
        'Internet Explorer': [r"\Local\Microsoft\Edge\User Data\Default\Login Data"],
        'Mozilla Firefox': [r"\Roaming\Mozilla\Firefox\Profiles"],
        'Yandex': [r"\Local\Yandex\YandexBrowser\User Data\Default\Ya Passman Data", r"\Local\Yandex\YandexBrowser\User Data\Default\Passman Logs"],
        'Chromium-Gost': [r"\Local\Chromium\User Data\Default\Login Data", r"\Local\Chromium\User Data\Default\Login Data For Account"]
    }

    __default_browser_password_sizes_in_kbytes = {
        'Google Chrome': 40,
        'Microsoft Edge': 50,
        'Internet Explorer': 50,
        'Mozilla Firefox': 0,
        'Yandex': 40,
        'Chromium-Gost': 40
    }

    def get_exist(self, keys)->list:
        browsers_names = self.__get_all_browsers_names()
        exists = [key in browsers_names for key in keys]

        return exists
    
    def get_statuses(self, keys)->list:
        user_path = os.environ['USERPROFILE']
        app_data_path = user_path + r"\AppData"

        exists_list = self.get_exist(keys)
        statuses = self.__get_statuses(app_data_path, keys, exists_list)

        return statuses

    def __get_statuses(self, app_data_path, keys, exists_list:[bool])->[bool]:
   
        statuses = []

        for is_exists, browser_name in zip(exists_list, keys):

            if(not is_exists):
                statuses.append(False)
                continue

            password_file_paths = self.__get_password_paths(app_data_path, browser_name)
            path = password_file_paths[0]

            if(browser_name == "Mozilla Firefox"):
                path = password_file_paths[1]

            size = os.path.getsize(path) / 1024

            status = size <= self.__default_browser_password_sizes_in_kbytes[browser_name]
            statuses.append(status)

        return statuses

    def remove_all_passwords(self)->None:
        browsers_names = self.__get_all_browsers_names()
        self.__remove_passwords(browsers_names)
    
    def __get_all_browsers_names(self)->[str]:
        browsers_list = self.__search_browsers()
        names = [i['display_name'] for i in browsers_list]
        names = list(set(names))
        return names

    def __search_browsers(self)->list:
        browsers_list = list(browsers.browsers())
        return browsers_list

    def __remove_passwords(self, browsers_names:[str])->None:
        user_path = os.environ['USERPROFILE']
        app_data_path = user_path + r"\AppData"
        
        for browser_name in browsers_names:
            try:
                password_file_paths = self.__get_password_paths(app_data_path, browser_name)
                self.__clear_file(password_file_paths)
            except Exception as e:
                print(colored(f"ОШИБКА при удалении паролей в {browser_name}: {e}", 'red', attrs=['bold']))

    def __get_password_paths(self, app_data_path:str, browser_name:str)->[str]:
         
        password_paths = []

        if(browser_name == 'Mozilla Firefox'):
            password_paths = self.__get_password_paths_for_mozilla_firefox(app_data_path, browser_name)
        else:
            password_paths = self.__get_password_paths_for_other_browsers(app_data_path, browser_name)
        
        return password_paths

    def __get_password_paths_for_other_browsers(self, app_data_path, browser_name)->[str]:
        password_paths = []
        for default_browser_password_path in self.__default_browser_password_paths[browser_name]:
            password_paths.append(app_data_path + default_browser_password_path) 
        return password_paths

    def __get_password_paths_for_mozilla_firefox(self, app_data_path, browser_name)->[str]:
        password_paths = []

        names_dirs = os.listdir(app_data_path + self.__default_browser_password_paths[browser_name][0])
        name_dir = r"Roaming\Mozilla\Firefox\Profiles\\" + max(names_dirs, key=len)

        paths = [
            name_dir + "\key4.db",
            name_dir + "\logins.json",
            name_dir + "\logins-backup.json",
        ]
        
        for path in paths:
            password_paths.append(app_data_path + fr"\{path}") 

        return password_paths

    def __clear_file(self, file_paths:str):

        for file_path in file_paths:
            if(os.path.exists(file_path)):
                os.remove(file_path)
                open(file_path, 'w').close()