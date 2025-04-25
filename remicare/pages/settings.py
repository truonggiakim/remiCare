from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background color
        with self.canvas.before:
            Color(0.95, 0.95, 1, 1)  # light purple
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # ScrollView to make it scrollable on smaller screens
        scroll = ScrollView(size_hint=(1, 1))

        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[20, 20, 20, 20], size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Header
        self.layout.add_widget(Label(text="Settings", font_size=28, size_hint_y=None, height=40, color=(0, 0, 0, 1)))

        # General Section
        self.layout.add_widget(Label(text="GENERAL", font_size=16, size_hint_y=None, height=30, color=(0.3, 0.3, 0.3, 1)))
        self.layout.add_widget(self._settings_item("👤", "Account", self.show_account_details))
        self.layout.add_widget(self._settings_item("🔔", "Notifications", self.show_notification_popup))
        self.layout.add_widget(self._settings_item("🚪", "Logout", self.logout_and_redirect))
        self.layout.add_widget(self._settings_item("🗑️", "Delete account", self.show_placeholder))

        # Feedback Section
        self.layout.add_widget(Label(text="FEEDBACK", font_size=16, size_hint_y=None, height=30, color=(0.3, 0.3, 0.3, 1)))
        self.layout.add_widget(self._settings_item("⚠️", "Report a bug", self.show_placeholder))
        self.layout.add_widget(self._settings_item("📨", "Send feedback", self.show_placeholder))

        scroll.add_widget(self.layout)
        
        #BACK BUTTON ON THE TOP LEFT CORNER
        float_container = FloatLayout()
        float_container.add_widget(scroll)

        back_btn = Button(
            text="←",
            size_hint=(None, None),
            size=(50, 40),
            pos_hint={"x": 0.02, "top": 0.98},  # Top-left corner with slight margin
            background_color=(0.8, 0.8, 1, 1),
            color=(0, 0, 0, 1)
            )
        back_btn.bind(on_press=self.go_back_home)
        float_container.add_widget(back_btn)
        self.add_widget(float_container)


    def _settings_item(self, icon, label_text, on_press_action):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, padding=[10, 5, 10, 5], spacing=10)
        with row.canvas.before:
            Color(1, 1, 1, 1)
            row.bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[10])
        row.bind(pos=self._update_bg, size=self._update_bg)

        icon_label = Label(text=icon, font_size=20, size_hint_x=0.1, color=(0, 0, 0, 1))
        text_label = Button(text=label_text, font_size=16, halign='left', valign='middle',
                            color=(0, 0, 0, 1), background_normal='', background_color=(0, 0, 0, 0))
        text_label.bind(on_press=on_press_action)

        row.add_widget(icon_label)
        row.add_widget(text_label)
        return row

    def show_notification_popup(self, instance):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="Sound"))
        layout.add_widget(Switch(active=True))
        layout.add_widget(Label(text="Vibration"))
        layout.add_widget(Switch(active=False))
        close_btn = Button(text="Close", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Notification Settings", content=layout,
                      size_hint=(0.8, 0.5), background_color=(1, 0.859, 0.886, 1))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_account_details(self, instance):
        if hasattr(self, 'account_box'):
            self.layout.remove_widget(self.account_box)
            del self.account_box
        else:
            self.account_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=[20, 0, 20, 0])
            self.account_box.add_widget(Label(text="Email: user@example.com", color=(0, 0, 0, 1)))
            self.account_box.add_widget(Label(text="Username: remiUser01", color=(0, 0, 0, 1)))
            index = self.layout.children.index(self._find_item_by_text("Account"))
            self.layout.add_widget(self.account_box, index=index)
    
    def logout_and_redirect(self, instance):
    # Optional: clear any app state here (e.g., reminders, tokens)
        print("🔒 Logging out and returning to signup screen...")
        self.manager.current = 'signup'

    def _find_item_by_text(self, text):
        for widget in self.layout.children:
            if isinstance(widget, BoxLayout):
                for child in widget.children:
                    if isinstance(child, Button) and child.text == text:
                        return widget
        return None

    def show_placeholder(self, instance):
        popup = Popup(title="Coming Soon",
                      content=Label(text="This feature is not implemented yet."),
                      size_hint=(0.7, 0.3))
        popup.open()

    def _update_bg(self, instance, value):
        if hasattr(instance, 'bg'):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    #back button
    def go_back_home(self, instance):
        self.manager.current = 'home'
    
    
