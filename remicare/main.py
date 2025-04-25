from kivy.config import Config
Config.set('graphics', 'width', '360')   # Standard phone width
Config.set('graphics', 'height', '740')  # Standard phone height

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from pages.signup import SignUpScreen
from pages.homepage import HomeScreen  # Make sure homepage.py is in a folder named "pages"
from pages.gpspage import GPSScreen
from pages.settings import SettingsScreen

class RemiCareApp(App):
    def build(self):
        print("App is starting...")

        sm = ScreenManager()

        signup = SignUpScreen(name='signup')
        home = HomeScreen(name='home')
        #print("HomeScreen object created.") check
        gps = GPSScreen(name='gps')
        settings = SettingsScreen(name='settings')

        sm.add_widget(signup)
        sm.add_widget(home)
        sm.add_widget(gps)
        sm.current = 'home'
        sm.add_widget(settings)
        sm.current = 'signup'
        
        return sm

if __name__ == '__main__':
    RemiCareApp().run()