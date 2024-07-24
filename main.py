from flet_ui.build_page import start_app
from browser_manager import BrowserManager


if __name__ == '__main__':
    browserManager = BrowserManager()
    start_app(browserManager)
