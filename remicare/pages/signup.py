from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Root layout with background
        root_layout = FloatLayout()

        with root_layout.canvas.before:
            Color(1.0, 0.859, 0.886, 1.0)  # Soft purple background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        root_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout for content
        layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=[30, 50, 30, 30],
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        gif = Image(
            source = 'assets/bird.gif',
            size_hint =(None, None),
            size =(120, 120),
            anim_delay = 0.1,
            allow_stretch = True,
            keep_ratio = True,
        )
        gif_anchor = AnchorLayout(
            anchor_x='center',   # center horizontally
            anchor_y='center',   # center vertically within that 120px slice
            size_hint=(1, None),
            height=120

        )
        layout.add_widget(gif)
        
        # Grouped headers to reduce spacing
        header_layout = BoxLayout(orientation='vertical', spacing=5)
        header_layout.add_widget(Label(text='Welcome to', font_size=65, bold=True, color=(0.0, 0.290, 0.678, 1)))
        header_layout.add_widget(Label(text='RemiCare', font_size=65, bold=True, color=(0.0, 0.290, 0.678, 1)))
        layout.add_widget(header_layout)

        layout.add_widget(Label(text='Sign Up', font_size=35, bold=True, italic=True, color=(0.0, 0.290, 0.678, 1)))

        # Styled input fields
        self.name_input = TextInput(
            hint_text='Name',
            multiline=False,
            size_hint=(1, None),
            height=45,
            padding=[10, 10],
            background_normal='',
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1)
        )
        self.email_input = TextInput(
            hint_text='Email',
            multiline=False,
            size_hint=(1, None),
            height=45,
            padding=[10, 10],
            background_normal='',
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1)
        )
        self.password_input = TextInput(
            hint_text='Password',
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=45,
            padding=[10, 10],
            background_normal='',
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1)
        )

        layout.add_widget(self.name_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)

        # Button
        login_button = Button(
            text='Log In',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5}
        )
        login_button.bind(on_press=self.go_login)
        layout.add_widget(login_button)

        root_layout.add_widget(layout)
        self.add_widget(root_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_login(self, instance):
        print("Name:", self.name_input.text)
        print("Email:", self.email_input.text)
        print("Password:", self.password_input.text)
        self.manager.current = 'home'  # Example screen switch
