import subprocess, os

cwd = os.path.dirname(os.path.realpath(__file__)) 
name = 'BrowserPasswordCleaner'
description = 'Desktop Browser Password Cleaner'
copyright = 'RDDH'
company = 'RDDH'
version = '1.0'
icon_path = cwd + '\\assets\\' + 'icon.ico'
output_dir = 'dist'
include = target = 'assets'
main_script = "main.py"
    

if __name__ == '__main__':
    
    #Flet
    # commands = ['python', '-m', 'nuitka', f'--windows-icon-from-ico={icon_path}' , f'--output-dir={output_dir}', '--follow-imports', '--onefile', f'--file-description="{description}"', f'--copyright="{copyright}"', f'--product-version={version}', '--standalone', '--windows-console-mode=disable', f'--include-data-dir={include}={target}', f'--output-filename={name}','--plugin-enable=pyqt5', main_script]
    
    #CTk
    commands = ['python', '-m', 'nuitka', f'--windows-icon-from-ico={icon_path}' , f'--output-dir={output_dir}', '--follow-imports', '--onefile', f'--file-description={description}', f'--copyright={copyright}', f'--product-version={version}', f'--company-name={company}', '--standalone', '--windows-console-mode=disable', f'--include-data-dir={include}={target}', f'--output-filename={name}','--plugin-enable=tk-inter', main_script]
    
    print(cwd)
    print(' '.join(commands))
    subprocess.run(args=commands, cwd=cwd)
    
# pyinstaller --noconfirm --onefile --windowed --icon "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\icon.ico" --upx-dir "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\assets\browsers" --clean --add-data "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\assets;assets/" --exclude-module "pip" --exclude-module "setuptools" --exclude-module "pillow" --exclude-module "numpy" --exclude-module "matplotlib"  "B:\MeinCode\Offers\Kwork\TideXim\BrowserKeyCleaner\main.py"