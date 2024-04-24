import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock  # Імпортуємо модуль Clock
import json

# Завантажуємо збережені дані
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {'score': 0, 'click_power': 1, 'teachers': 0}

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text=f'Очки: {data["score"]}')
        play_button = Button(text='Грати', on_press=self.switch_to_game)
        layout.add_widget(self.label)
        layout.add_widget(play_button)
        self.add_widget(layout)

    def switch_to_game(self, instance):
        app.root.current = 'game'

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text=f'Очки: {data["score"]}')
        self.diploma_button = Button(text='🎓', on_press=self.click_diploma, font_size=48)
        self.upgrade_button = Button(text=f'Прокачати клік ({data["click_power"] + 1} очок)', on_press=self.upgrade_click)
        self.teacher_button = Button(text=f'Найняти викладача ({data["teachers"] + 1} очок/сек)', on_press=self.hire_teacher)
        layout.add_widget(self.label)
        layout.add_widget(self.diploma_button)
        layout.add_widget(self.upgrade_button)
        layout.add_widget(self.teacher_button)
        self.add_widget(layout)
        self.event = None

    def click_diploma(self, instance):
        data['score'] += data['click_power']
        self.label.text = f'Очки: {data["score"]}'
        self.save_data()

    def upgrade_click(self, instance):
        cost = data['click_power'] + 1
        if data['score'] >= cost:
            data['score'] -= cost
            data['click_power'] += 1
            self.label.text = f'Очки: {data["score"]}'
            self.upgrade_button.text = f'Прокачати клік ({data["click_power"] + 1} очок)'
            self.save_data()

    def hire_teacher(self, instance):
        cost = data['teachers'] + 1
        if data['score'] >= cost:
            data['score'] -= cost
            data['teachers'] += 1
            self.label.text = f'Очки: {data["score"]}'
            self.teacher_button.text = f'Найняти викладача ({data["teachers"] + 1} очок/сек)'
            self.save_data()
            if self.event is None:
                self.event = Clock.schedule_interval(self.auto_click, 1)

    def auto_click(self, dt):
        data['score'] += data['teachers']
        self.label.text = f'Очки: {data["score"]}'
        self.save_data()

    def save_data(self):
        with open('data.json', 'w') as f:
            json.dump(data, f)

class DyplomaClickerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(GameScreen(name='game'))
        return sm

app = DyplomaClickerApp()
app.run()