from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.utils import platform

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name = "menu"))
        sm.add_widget(GameScreen(name = "game"))
        return sm
    
if platform != "android":
    Window.size = (400, 800)
    Window.left = 750

if __name__ == "__main__":
    MainApp().run()
