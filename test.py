from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Клікер дипломної роботи', font_size=30, pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        self.add_widget(Label(text='Рекорд: ' + str(App.get_running_app().record), font_size=20, pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.add_widget(Button(text='Почати гру', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3}, on_press=self.start_game))

    def start_game(self, instance):
        self.manager.current = 'game'

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.progress = ProgressBar(max=100, value=50, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.8, 0.8))
        self.add_widget(self.progress)
        self.add_widget(Button(background_normal='diploma.png', size_hint=(0.2, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.3}, on_press=self.increment_progress))
        self.time_label = Label(text='Час: 0', font_size=20, pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.add_widget(self.time_label)
        self.time = 0
        self.event = None

    def on_enter(self):
        self.event = Clock.schedule_interval(self.decrement_progress, 0.3)

    def increment_progress(self, instance):
        if self.progress.value < 100:
            self.progress.value += 1

    def decrement_progress(self, dt):
        if self.progress.value > 0:
            self.progress.value -= 1
        else:
            self.game_over()
        self.time += dt
        self.time_label.text = 'Час: {:.2f}'.format(self.time)

    def game_over(self):
        self.event.cancel()
        if self.time > App.get_running_app().record:
            App.get_running_app().record = self.time
        self.manager.current = 'start'

class ClickerApp(App):
    def build(self):
        Window.size = (400, 800)
        self.record = 0
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    ClickerApp().run()