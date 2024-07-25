from termcolor import colored
from browsers import browsers
from winreg import HKEY_CURRENT_USER, KEY_WRITE, REG_SZ, OpenKeyEx, DeleteKeyEx, CreateKeyEx, SetValue
from os import listdir, remove, environ
from os.path import exists, getsize, dirname, realpath
from psutil import process_iter
from shutil import copyfile
from sqlite3 import connect, OperationalError

class BrowserManager:

    __default_browser_password_paths = {
        'Google Chrome': [r"\Local\Google\Chrome\User Data\Default\Login Data", r"\Local\Google\Chrome\User Data\Default\Login Data For Account"],
        'Microsoft Edge': [r"\Local\Microsoft\Edge\User Data\Default\Login Data"],
        'Internet Explorer': [r"Software\Microsoft\Internet Explorer\IntelliForms\Storage2"],
        'Mozilla Firefox': [r"\Roaming\Mozilla\Firefox\Profiles"],
        'Yandex': [r"\Local\Yandex\YandexBrowser\User Data\Default\Ya Passman Data", r"\Local\Yandex\YandexBrowser\User Data\Default\Passman Logs"],
        'Chromium-Gost': [r"\Local\Chromium\User Data\Default\Login Data", r"\Local\Chromium\User Data\Default\Login Data For Account"]
    }

    def get_existances(self, keys)->list:
        browsers_names = self.__get_all_browsers_names()
        exists = [key in browsers_names for key in keys]

        return exists
    
    def get_statuses(self, keys)->list:
        user_path = environ['USERPROFILE']
        app_data_path = user_path + r"\AppData"

        exists_list = self.get_existances(keys)
        statuses = self.__get_statuses(app_data_path, keys, exists_list)

        return statuses

    def __get_statuses(self, app_data_path, keys, exists_list:list)->list:
   
        statuses = []
        

        for is_exists, browser_name in zip(exists_list, keys):

            if(not is_exists):
                statuses.append(False)
                continue

            password_file_paths = self.__get_password_paths(app_data_path, browser_name)
            path = password_file_paths[0]
            
            if(browser_name == "Mozilla Firefox"):
                path = password_file_paths[1]
                status = True
                if exists(path):
                    size = getsize(path) / 1024
                    status = size == 0
                statuses.append(status)
                continue
                
            if(browser_name == "Internet Explorer"):
                status = self.__get_status_internet_explorer(path)
                statuses.append(status)
                continue
          
            try:
                query = '''select count(*) from logins;'''
                filename_temp = f'{dirname(realpath(__file__))}\\temp'
                    
                copyfile(path, filename_temp)

                with connect(filename_temp) as db:
                    cursor = db.cursor()
                    res = cursor.execute(query).fetchone()[0]
                    status = res == 0
                    statuses.append(status)

            except FileNotFoundError:
                statuses.append(True)
            except OperationalError as e:
                if "no such table" in str(e):
                    statuses.append(True)
            
        return statuses

    def __get_status_internet_explorer(self, password_path:str)->bool:

        try:
            location = HKEY_CURRENT_USER
            OpenKeyEx(location, password_path)
            return False

        except FileNotFoundError:
            return True
        
        except Exception as e:
            print(colored(f"ОШИБКА при получении информации о паролях из реестра в Internet Explorer: {e}", 'red', attrs=['bold']))


    def __get_browsers_path_exe(self) -> list:
        items = list(browsers())
        paths = [item.get('path', '') for item in items]
        return paths
    
    def __truncate_path_exe(self, path):
        return path.split('\\')[-1]

    def __close_browsers(self, browser_paths):
        for process in process_iter():
            if process.name() in browser_paths: 
                process.kill()

    def remove_all_passwords(self)->None:
        browser_paths = self.__get_browsers_path_exe() 
        truncated_paths = list(map(self.__truncate_path_exe, browser_paths))
        self.__close_browsers(truncated_paths)
        browsers_names = self.__get_all_browsers_names()
        self.__remove_passwords(browsers_names)
    
    def __get_all_browsers_names(self)->list:
        browsers_list = self.__search_browsers()
        names = [i['display_name'] for i in browsers_list]
        names = list(set(names))
        return names

    def __search_browsers(self)->list:
        browsers_list = list(browsers())
        return browsers_list

    def __remove_passwords(self, browsers_names:list)->None:
        user_path = environ['USERPROFILE']
        app_data_path = user_path + r"\AppData"
        
        for browser_name in browsers_names:
            try:
                password_paths = self.__get_password_paths(app_data_path, browser_name)

                if(browser_name == 'Internet Explorer'):
                    self.__clear_registry(*password_paths)
                else:
                    self.__clear_file(password_paths)

            except Exception as e:
                print(colored(f"ОШИБКА при удалении паролей в {browser_name}: {e}", 'red', attrs=['bold']))

    def __get_password_paths(self, app_data_path:str, browser_name:str)->list:
         
        password_paths = []

        if(browser_name == 'Mozilla Firefox'):
            password_paths = self.__get_password_paths_for_mozilla_firefox(app_data_path, browser_name)
        elif(browser_name == 'Internet Explorer'):
            password_paths = self.__get_password_paths_for_internet_explorer(browser_name)
        else:
            password_paths = self.__get_password_paths_for_other_browsers(app_data_path, browser_name)
        
        return password_paths

    def __get_password_paths_for_mozilla_firefox(self, app_data_path:str, browser_name:str)->list:
        password_paths = []

        names_dirs = listdir(app_data_path + self.__default_browser_password_paths[browser_name][0])
        name_dir = r"Roaming\Mozilla\Firefox\Profiles" + "\\" + max(names_dirs, key=len)

        paths = [
            name_dir + "\key4.db",
            name_dir + "\logins.json",
            name_dir + "\logins-backup.json",
        ]
        
        for path in paths:
            password_paths.append(app_data_path + fr"\{path}") 

        return password_paths

    def __get_password_paths_for_internet_explorer(self, browser_name:str)->list:
        return self.__default_browser_password_paths[browser_name]

    def __get_password_paths_for_other_browsers(self, app_data_path:str, browser_name:str)->list:
        password_paths = []
        for default_browser_password_path in self.__default_browser_password_paths[browser_name]:
            password_paths.append(app_data_path + default_browser_password_path) 
        return password_paths

    def __clear_file(self, file_paths:str)->None:

        for file_path in file_paths:
            if(exists(file_path)):
                remove(file_path)
                open(file_path, 'w').close()

    def __clear_registry(self, password_path:str)->None:

        try:
            location = HKEY_CURRENT_USER
            DeleteKeyEx(location, password_path)

        except FileNotFoundError:
            print(colored(f"Значит в Internet Explorer все чисто ;)", 'red', attrs=['bold']))
        
        except Exception as e:
            print(colored(f"ОШИБКА при удалении паролей из реестра в Internet Explorer: {e}", 'red', attrs=['bold']))
            
    def save_path_browser(self, browser_name:str, path_to_exe:str):

        new_path_browser = f"Software\\Clients\\StartMenuInternet\\{browser_name}"

        self.__create_required_folders_for_save(new_path_browser)
        self.__set_required_values_for_save(browser_name, new_path_browser, path_to_exe)
    def __create_required_folders_for_save(self, path_browser:str):
        key_current_usr = HKEY_CURRENT_USER
        path_create_folders = path_browser + "\\shell\\open\\command"

        CreateKeyEx(key_current_usr, path_create_folders, 0, KEY_WRITE)

    def __set_required_values_for_save(self, browser_name:str, path_browser:str, path_to_exe:str):
        key_current_usr = HKEY_CURRENT_USER

        SetValue(key_current_usr, path_browser, REG_SZ, browser_name)

        path_to_command_folder = path_browser + "\\shell\\open\\command"
        SetValue(key_current_usr, path_to_command_folder, REG_SZ, path_to_exe)
