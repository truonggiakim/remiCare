from kivy.config import Config
Config.set('graphics', 'width', '360')   # Standard phone width
Config.set('graphics', 'height', '740')  # Standard phone height


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from pages.homepage import HomeScreen  # Make sure homepage.py is in a folder named "pages"

class RemiCareApp(App):
    def build(self):
        print("🟣 App is starting...")

        sm = ScreenManager()

        home = HomeScreen(name='home')
        print("✅ HomeScreen object created.")

        sm.add_widget(home)
        sm.current = 'home'

        print("HomeScreen added to ScreenManager.")
        return sm

if __name__ == '__main__':
    RemiCareApp().run()
