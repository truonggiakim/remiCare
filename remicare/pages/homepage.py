from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from api_client import ApiClient
from kivy.clock import mainthread
import threading, time
POLL_S=5

class RoundedLabel(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.5, None)
        self.height = 40
        self.padding = [10, 5, 10, 5]
        with self.canvas.before:
            Color(1, 0.8, 0.9, 1)  # soft pink
            self.rect = RoundedRectangle(radius=[15], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.label = Label(text=text, color=(0, 0, 0, 1), font_size=16)
        self.add_widget(self.label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.reminders = [] #create the list we are going to store the previous reminders in.
        ApiClient.background(self.load_reminders)()


        with self.canvas.before:
            Color(0.85, 0.80, 1, 1)  # pastel purple
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.main_layout = BoxLayout(orientation='vertical', spacing=15, padding=[20, 20, 20, 15])
        self.main_layout.add_widget(self._make_label("RemiCare", 32, 50, color=(0.0, 0.290, 0.678, 1), bold=True))
        self.main_layout.add_widget(self._make_rounded_box_label("Today's reminder for your kids", 26, (1, 0.8, 0.9, 1)))
        """these are the defaults reminders for testing
        self.reminders = [
            {"name": "Time to drink water", "time": "10:00 AM"},
            {"name": "Time to do your assignment", "time": "2:00 PM"},
            {"name": "Time to go to bed", "time": "8:30 PM"}
        ]"""

        header_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        header_row.add_widget(RoundedLabel("Reminders"))
        header_row.add_widget(RoundedLabel("Time"))
        self.main_layout.add_widget(header_row)

        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.refresh_grid()
        self.main_layout.add_widget(self.grid)

        add_btn = Button(
            text="+",
            font_size=26,
            size_hint=(None, None),
            size=(50, 50),
            background_color=(0.286, 0.329, 0.745, 1),  # #4954be
            color=(1, 1, 1, 1),
            on_press=self.add_reminder_popup
        )
        anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        anchor.add_widget(add_btn)
        self.main_layout.add_widget(anchor)

         #view all reminder button
        # view_btn = Button(
        #     text="View All Reminders",
        #     size_hint_y=None,
        #     height=45,
        #     background_color=(0.737, 0.745, 0.980, 1),  # light purple
        #     color=(0, 0, 0, 1),
        #     background_normal='',
        # )
        # with view_btn.canvas.before:
        #     Color(0.737, 0.745, 0.980, 1)
        #     self.view_rect = RoundedRectangle(radius=[20], pos=view_btn.pos, size=view_btn.size)
        #     view_btn.bind(pos=self._update_view_btn, size=self._update_view_btn)
        # self.main_layout.add_widget(view_btn)

        float_layout = FloatLayout()
        float_layout.add_widget(self.main_layout)

        nav_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10, pos_hint={'x': 0, 'y': 0})
        nav_bar.add_widget(self._make_button("Home", self.go_home))
        nav_bar.add_widget(self._make_button("GPS", self.go_location))
        nav_bar.add_widget(self._make_button("Settings", self.go_settings))
        float_layout.add_widget(nav_bar)

        self.main_layout.size_hint = (1, None)
        self.main_layout.height = 700
        self.main_layout.pos_hint = {"top": 1}

        self.add_widget(float_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_view_btn(self, instance, value):
        self.view_rect.pos = instance.pos
        self.view_rect.size = instance.size

    def _make_label(self, text, size, height, color=(0, 0, 0, 1), bold=False):
        lbl = Label(
            bold=bold,
            text=text,
            font_size=size,
            size_hint_y=None,
            height=height,
            halign='center',
            color=color
        )
        lbl.bind(size=lbl.setter('text_size'))
        return lbl

    def _make_rounded_box_label(self, text, font_size, bg_color):
        container = BoxLayout(size_hint_y=None, height=50, padding=[10, 5, 10, 5])
        with container.canvas.before:
            Color(*bg_color)
            container.rect = RoundedRectangle(radius=[20], pos=container.pos, size=container.size)
        container.bind(pos=self.update_rect, size=self.update_rect)
        label = Label(text=text, font_size=font_size, color=(0, 0, 0, 1))
        container.add_widget(label)
        return container

    def update_rect(self, instance, value):
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

    def _make_button(self, text, action=None, height=50):
        btn = Button(
            text=text,
            size_hint_y=None,
            height=height,
            background_color=(0.7, 0.7, 1, 1),
            color=(0, 0, 0, 1)
        )
        if action:
            btn.bind(on_press=action)
        return btn

    def refresh_grid(self):
        self.grid.clear_widgets()
        for index, r in enumerate(self.reminders):
            row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
            reminder_btn = Button(
                text=r["reminder"],
                size_hint_x=0.7,
                background_color=(1, 0.859, 0.886, 1),  # #ffdbe2
                background_normal='',
                color=(0, 0, 0, 1),
                on_press=lambda btn, i=index: self.edit_reminder(i)
            )
            time_btn = Button(
                text=r["time"],
                size_hint_x=0.3,
                background_color=(1, 0.859, 0.886, 1),  # #ffdbe2
                background_normal='',
                color=(0, 0, 0, 1),
                on_press=lambda btn, i=index: self.edit_time(i)
            )
            row.add_widget(reminder_btn)
            row.add_widget(time_btn)
            self.grid.add_widget(row)

    def edit_time(self, index):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        hours = [f"{i:02}" for i in range(1, 13)]
        minutes = [f"{i:02}" for i in range(0, 60, 5)]
        meridian = ["AM", "PM"]
        hour_spin = Spinner(text=self.reminders[index]['time'][:2], values=hours)
        minute_spin = Spinner(text= self.reminders[index]['time'][3:5], values=minutes)
        meridian_spin = Spinner(text=self.reminders[index]['time'][6:8], values=meridian)
        time_row = BoxLayout()
        time_row.add_widget(hour_spin)
        time_row.add_widget(minute_spin)
        time_row.add_widget(meridian_spin)
        save_btn = Button(text="Set Time", size_hint_y=None, height=40)

        def save_and_close(instance):
            new_time = f"{hour_spin.text}:{minute_spin.text} {meridian_spin.text}"
            rem = self.reminders[index]
            ApiClient.background(self.api_update)(rem["id"], rem["reminder"], new_time)
            popup.dismiss()

        save_btn.bind(on_press=save_and_close)
        popup_layout.add_widget(time_row)
        popup_layout.add_widget(save_btn)
        popup = Popup(title="Edit Time", content=popup_layout, size_hint=(0.8, 0.3))
        popup.open()

    def edit_reminder(self, index):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        input_box = TextInput(text=self.reminders[index]["reminder"], multiline=False)
        save_btn = Button(text="Save", size_hint_y=None, height=40)

        def save_and_close(instance):
            #self.reminders[index]["name"] = input_box.text
            #self.refresh_grid()
            #popup.dismiss()
            name = input_box.text.strip()
            if name:
                rem = self.reminders[index]
                ApiClient.background(self.api_update)(rem["id"], name, rem["time"])
                popup.dismiss()

        save_btn.bind(on_press=save_and_close)
        popup_layout.add_widget(input_box)
        popup_layout.add_widget(save_btn)
        popup = Popup(title="Edit Reminder", content=popup_layout, size_hint=(0.8, 0.3))
        popup.open()

    def add_reminder_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)


        name_input = TextInput(hint_text="Reminder name", multiline=False)
        popup_layout.add_widget(name_input)
        hours   = [f"{i:02}" for i in range(1, 13)]
        minutes = [f"{i:02}" for i in range(0, 60, 5)]
        meridian= ["AM", "PM"]

        hour_spin     = Spinner(text=hours[0],   values=hours)
        minute_spin   = Spinner(text=minutes[0], values=minutes)
        meridian_spin = Spinner(text=meridian[0],values=meridian)

        time_row = BoxLayout(spacing=5, size_hint_y=None, height=40)
        time_row.add_widget(hour_spin)
        time_row.add_widget(minute_spin)
        time_row.add_widget(meridian_spin)
        popup_layout.add_widget(time_row)


        save_btn = Button(text="Add", size_hint_y=None, height=40)

        def add_and_close(btn):
            name = name_input.text.strip()
            time = f"{hour_spin.text}:{minute_spin.text} {meridian_spin.text}"
            if name and time:
                #self.reminders.append({"name": name, "time": time})
                #self.refresh_grid()
                #popup.dismiss()
                ApiClient.background(self.api_add)(name,time)
                popup.dismiss()

        save_btn.bind(on_press=add_and_close)
        popup_layout.add_widget(save_btn)
        popup = Popup(title="New Reminder", content=popup_layout, size_hint=(0.8, 0.4))
        popup.open()

    
    def load_reminders(self):
        data = ApiClient.list_reminders()
        self.set_reminders(data)
    
    @mainthread
    def set_reminders(self, data):
        self.reminders = data
        self.refresh_grid()

    def api_add(self, name, time):
        new = ApiClient.add_reminder(name,time)
        self.set_reminders(self.reminders + [new])

    def api_update(self, rem_id, name, time):
        ApiClient.update_reminder(rem_id,name, time)
        self.load_reminders()

    def delete_reminder(self, index):
        rem_id = self.reminders[index]["id"]
        ApiClient.background(self.api_delete)(rem_id)

    def api_delete(self, rem_id):
        ApiClient.delete_reminder(rem_id)
        self.load_reminders()

    def on_enter(self):
        self.stop_poll = False
        threading.Thread(target=self.poll_loop, daemon=True).start()

    def on_leave(self):
        self._stop_poll = True
    
    def poll_loop(self):
        while not self.stop_poll:
            try:
                data = ApiClient.list_reminders()
                if data != self.reminders:
                    self.load_reminders()
            except Exception as excep:
                print("reminders could not update", excep)
            time.sleep(POLL_S)

    def go_home(self, instance):
        print("Navigating to Home")

    def go_location(self, instance):
        self.manager.current = 'gps'
        print("Navigating to GPS")
        
    def go_settings(self, instance):
        self.manager.current = 'settings'
        print("Navigating to Settings")
        self.manager.current = 'settings'
