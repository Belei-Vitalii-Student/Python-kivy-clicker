# from kivy.app import App
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.core.window import Window
# from kivy.utils import platform
# from kivy.uix.image import Image

# class MenuScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

# class GameScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#     def increase_progress(self):
#       if self.ids.progress.value < self.ids.progress.max:
#         self.ids.progress.value += 1

# class MainApp(App):
#     def build(self):
#         sm = ScreenManager()
#         sm.add_widget(MenuScreen(name = "menu"))
#         sm.add_widget(GameScreen(name = "game"))
#         return sm

# class ButtonImage(Image):
#     def on_touch_down(self, touch):
#         print("Press")
#         # if self.ids.progress.value < self.ids.progress.max:
#         #     self.ids.progress.value += 1


# if platform != "android":
#     Window.size = (400, 800)
#     Window.left = 750

# if __name__ == "__main__":
#     MainApp().run()














from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class GameScreen(Screen):
    progress = NumericProperty(0)
    time_interval = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.schedule_progress_decrease()

    def increase_progress(self):
        if self.progress < 100:
            self.progress += 1

    def decrease_progress(self, dt):
        if self.progress > 0:
            self.progress -= 1
        else:
            self.game_over()

    def schedule_progress_decrease(self):
        Clock.schedule_interval(self.decrease_progress, self.time_interval / 1000)

    def game_over(self):
        print("Game Over")
        # Add your game over logic here

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm

class ButtonImage(Image):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            game_screen = self.parent.parent.parent.parent
            game_screen.increase_progress()

if platform != "android":
    Window.size = (400, 800)
    Window.left = 750

if __name__ == "__main__":
    MainApp().run()