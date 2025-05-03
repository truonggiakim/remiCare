from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import mainthread

# optional: pip install kivy_garden.mapview
try:
    from kivy_garden.mapview import MapView, MapMarker
    MAPVIEW_AVAILABLE = True
except ImportError:
    MAPVIEW_AVAILABLE = False

import threading
import time
import requests


class GPSScreen(Screen):
    POLL_S = 5
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ---------- purple background ----------
        with self.canvas.before:
            Color(0.95, 0.95, 1, 1)          # same pastel purple
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # ---------- main content ----------
        content = BoxLayout(orientation="vertical",
                            spacing=15,
                            padding=[20, 20, 20, 15])

        # headline
        title = Label(text="RemiCare-GPS", bold=True,
                      font_size=32, size_hint_y=None, height=50,
                      halign='center', valign = 'middle',
                      color=(0.0, 0.290, 0.678, 1))
        title.bind(size=title.setter("text_size"))
        content.add_widget(title)

        # subtitle
        subtitle = self._rounded_label("Child-tracker Dashboard",
                                       font_size=26,
                                       bg=(1, 0.8, 0.9, 1))
        content.add_widget(subtitle)

        # Map or fallback
        if MAPVIEW_AVAILABLE:
            self.mapview = MapView(zoom=16, lat=0, lon=0)  # start blank
            content.add_widget(self.mapview)

            # quick helper to update marker from elsewhere in the app
            self.marker = MapMarker(lat=0, lon=0)
            self.mapview.add_widget(self.marker)
        else:
            warn = Label(text="[i]Install kivy_garden.mapview "
                               "for the live map[/i]",
                          markup=True)
            content.add_widget(warn)

        # ----- FloatLayout so nav‑bar sticks to bottom -----
        root = FloatLayout()
        root.add_widget(content)

        nav = self._nav_bar()
        root.add_widget(nav)
        content.size_hint = (1, None)
        content.height = 700
        content.pos_hint = {"top": 1}


        #back button
        back_btn = Button(
            text="<",
            size_hint=(None, None),
            size=(50, 40),
            pos_hint={"x": 0.02, "top": 0.98},
            background_color=(0,0,0,0),
            color=(0, 0, 0, 1)
        )
        back_btn.bind(on_press=self.go_back_home)
        root.add_widget(back_btn)
        self.add_widget(root)

    #--pulling the gps data---
    def on_enter(self):
        """Start pulling the data from the api on enter"""
        self._stop = False
        threading.Thread(target=self._poll_loop, daemon=True).start()


    def on_leave(self):
        """Stops the thread when the user leaves the gps screen"""
        self._stop = True


    def _poll_loop(self):
        while not self._stop:
            try:
                r = requests.get("http://127.0.0.1:8000/location", timeout=10)
                r.raise_for_status()
                data = r.json()
                self._update_safe(data['lat'], data['lon'])
            except Exception as excep:
                print("API ERROR:", excep)
            time.sleep(self.POLL_S)

    @mainthread
    def _update_safe(self, lat, lon):

        if MAPVIEW_AVAILABLE:
            self.mapview.center_on(lat,lon)
            self.marker.lat, self.marker.lon = lat,lon


    # ---------- helpers ----------
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _rounded_label(self, text, font_size, bg):
        box = BoxLayout(size_hint_y=None, height=50, padding=[10, 5, 10, 5])
        with box.canvas.before:
            Color(*bg)
            box.rect = RoundedRectangle(radius=[20], pos=box.pos,
                                         size=box.size)
        box.bind(pos=self._sync_rect, size=self._sync_rect)
        lbl = Label(text=text, font_size=font_size, color=(0, 0, 0, 1))
        box.add_widget(lbl)
        return box

    def _sync_rect(self, instance, _):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def _nav_bar(self):
        nav = BoxLayout(orientation='horizontal',
                        size_hint=(1, None), height=50, spacing=10,
                        pos_hint={'x': 0, 'y': 0})

        nav.add_widget(self._nav_btn("Home", self.go_home))
        nav.add_widget(self._nav_btn("GPS", lambda *_: None))  # current
        nav.add_widget(self._nav_btn("Settings", self.go_settings))
        return nav

    def _nav_btn(self, text, cb):
        btn = Button(text=text, background_color=(0.7, 0.7, 1, 1),
                     color=(0.7, 0.7, 1, 1), size_hint_y=None, height=50)
        btn.bind(on_press=cb)
        return btn

    # --- screen switches ---
    def go_home(self, *_):
        self.manager.current = 'home'

    def go_settings(self, *_):
        self.manager.current = 'settings'  # implement later
    

    #back button to homescreen

    def go_back_home(self, instance):
        self.manager.current = 'home'


    
