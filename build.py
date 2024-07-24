import subprocess, os

cwd = os.path.dirname(os.path.realpath(__file__)) 
name = 'BrowserPasswordCleaner'
description = 'Desktop Browser Password Cleaner'
copyright = 'RDDH'
version = '1.0'
icon_path = cwd + '\\' + 'icon.ico'
output_dir = 'dist'
include = target = 'assets'
main_script = "main.py"

#from flet.__pyinstaller.win_utils import update_flet_view_icon
    

if __name__ == '__main__':
    #update_flet_view_icon(r'C:\Users\ivan2\AppData\Local\Programs\Python\Python311\Lib\site-packages\flet\bin\flet\flet.exe', f'{cwd}\\icon.ico')
    
    commands = ['python', '-m', 'nuitka', f'--windows-icon-from-ico={icon_path}' , f'--output-dir={output_dir}', '--follow-imports', '--onefile', f'--file-description="{description}"', f'--copyright="{copyright}"', f'--product-version={version}', '--standalone', '--windows-console-mode=disable', f'--include-data-dir={include}={target}', f'--output-filename={name}','--plugin-enable=pyqt5', main_script]
    print(cwd)
    print(' '.join(commands))
    subprocess.run(args=commands, cwd=cwd)
    
# pyinstaller --noconfirm --onefile --windowed --icon "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\icon.ico" --upx-dir "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\assets\browsers" --clean --add-data "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\assets;assets/" --exclude-module "pip" --exclude-module "setuptools" --exclude-module "pillow" --exclude-module "numpy" --exclude-module "matplotlib"  "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\main.py"