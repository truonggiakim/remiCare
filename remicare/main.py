from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '740')
Config.set('graphics', 'width', '360')   # Standard phone width
Config.set('graphics', 'height', '740')  # Standard phone height

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from pages.signup import SignUpScreen
from pages.signup    import SignUpScreen
from pages.homepage  import HomeScreen
from pages.settings  import SettingsScreen
from pages.gpspage import GPSScreen
from pages.settings import SettingsScreen
#if want to make a ViewAllScreen:
#from pages.view_all import ViewAllScreen

class RemiCareApp(App):
    def build(self):
        print("App is starting...")

        sm = ScreenManager()
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GPSScreen(name='gps'))
        # sm.add_widget(ViewAllScreen(name='view_all'))
        sm.current = 'signup'
        return sm

if __name__ == '__main__':
    RemiCareApp().run()