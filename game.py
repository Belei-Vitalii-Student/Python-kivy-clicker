from random import randrange
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Canvas, Rotate, Rectangle, PushMatrix, PopMatrix
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
import json

try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {'clicks': 0, 'score': 0, 'click_power': 1, 'teachers': 0, 'ais': 0, 'click_price': 10, 'teacher_price': 25, 'ai_price': 100}

Builder.load_file('game.kv')

class MainScreen(Screen):
    data = data
    progress_text = f'Очки: {data["score"]}'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def switch_to_game(self, instance):
        app.root.current = 'game'

class ImageButton(ButtonBehavior, Image):
    pass

class FloatingLabel(Label):
    start_pos = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation = None

    def start_animation(self, x, y):
        self.pos = x, y
        self.start_pos = x, y
        rand = randrange(100)
        animation = Animation(pos=(x, y + rand), opacity=1, duration=.7, t='out_quad')
        animation += Animation(pos=(x, y + rand + 50), opacity=0, duration=.1, t='out_quad')
        animation.bind(on_complete=self.remove_label)
        animation.start(self)
        self.animation = animation

    def remove_label(self, instance, value):
        self.parent.remove_widget(self)

class ButtonInteraction(ImageButton):
    duration = NumericProperty(1)
    angle = NumericProperty(0)
    original_size = ListProperty([200, 200])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation = None
        self.rotation = Rotate(angle=150, origin=self.center)
        # self.rotation = kwargs.pop('rotation')
        self.original_size = (200, 200)  # Зберегти початковий розмір кнопки
        with self.canvas.before:
            PushMatrix()
            Rotate(origin=self.center, angle=0)
        with self.canvas.after:
            PopMatrix()

    def start_animation(self):
        animation = Animation(rotation=45, duration=self.duration, t='out_quad')
        animation.start(self)
        self.animation = animation

    def on_rotation_angle(self, instance, value):
        # Кожного разу, коли значення rotation_angle змінюється, ми оновлюємо кут обертання
        self.rotation.angle = value
        self.canvas.ask_update()  # Оновлюємо canvas

    def remove_label(self, instance, value):
        self.parent.remove_widget(self)

class GameScreen(Screen):
    dyploma_state = 0
    progress_text = f'Очки: {data["score"]}'
    market_upgrade_text = 'Прокачати клік [+1] \n({} очок)  |  \nВартість: {}'.format(data["click_power"], data["click_price"])
    market_teacher_text = f'Найняти викладача [+1] \n({data["teachers"]} очок/сек)  |  \nВартість: {data["teacher_price"]}'
    market_ai_text = f'Найняти ШІ [+(0-10)] \n({data["ais"]} ШІ)  |  \nВартість: {data["ai_price"]}'

    click_multiplier = 1.1
    teacher_multiplier = 1.2
    ai_multiplier = 1.4
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diploma_button = self.ids.dyploma_button
        self.upgrade_button = self.ids.upgrade_button
        self.teacher_button = self.ids.teacher_button
        self.ai_button = self.ids.ai_button
        self.next_dyploma_state = self.dyploma_state_generator()
        Clock.schedule_interval(self.update, 1)

    def dyploma_state_generator(self):
        states = ['assets/dyploma_step_1.png', 'assets/dyploma_step_2.png', 'assets/dyploma_step_3.png', 'assets/dyploma_step_4.png', 'assets/dyploma_step_5.png']
        states_len = len(states)
        index = 0
        while True:
            yield {'state': states[index], 'last': states[index] == states[0]}
            index = (index + 1) % states_len

    def update_score(self):
        self.ids.progress_text.text = f'Очки: {data["score"]}'
        self.progress_text = f'Очки: {data["score"]}'

    def update_click_upgrade(self):
        self.upgrade_button.text = 'Прокачати клік [+1] \n({} очок)  |\n  Вартість: {}'.format(data["click_power"], data["click_price"])

    def update_teacher_upgrade(self):
        self.teacher_button.text = f'Найняти викладача [+1] \n({data["teachers"]} очок/сек)  |\n  Вартість: {data["teacher_price"]}'

    def update_ai_upgrade(self):
        self.ai_button.text = f'Найняти ШІ [+(0-10)] \n({data["ais"]} ШІ)  |\n  Вартість: {data["ai_price"]}'

    def animate_button(self, instance):
        anim = Animation(
            opacity=0.8,
            pos_hint={"center_x": 0.5, "center_y": 0.5}, 
            background_color=self.rgba_to_color(16, 100, 85, 0.8),
            font_size=15,
            duration=0.1, 
            t='out_back'
        )
        anim += Animation(
            opacity=1, 
            pos_hint={"center_x": 0.5, "center_y": 0.5}, 
            background_color=self.rgba_to_color(32, 205, 175, 0.8), 
            duration=0.1,
            font_size=17,
            t='out_back'
        )
        anim.start(instance)

    def click_diploma(self, instance):
        next_icon = next(self.next_dyploma_state)
        if(next_icon['last'] == True):
            data['score'] += self.get_bonus()
        data['clicks'] += 1
        data['score'] += data['click_power']
        self.update_score()
        self.save_data()
        self.button_animation()
        instance.source = next_icon['state']

    def get_bonus(self):
        if(data['clicks'] <= 10):
            bonus = 0
        else:
            bonus = randrange(0, int(data['clicks'] / 10))
        label = FloatingLabel(text=f'+{bonus}', font_size=40, opacity=0, bold=True, color=self.rgba_to_color(111, 222, 220, 1))
        x = self.diploma_button.center[0] - self.diploma_button.size[0]
        y = self.diploma_button.center[1] + self.diploma_button.size[1] / 2
        label.start_animation(x, y)
        self.ids.floating_labels.add_widget(label)

        return bonus


    def button_animation(self):
        if self.diploma_button.animation:
            self.diploma_button.animation.cancel(self.diploma_button)

        anim = Animation(opacity=0.8, size=(self.diploma_button.size[0] / 1.4, self.diploma_button.size[1] / 1.4), pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=0.1, t='out_back')
        
        # Прив'язати функцію, яка оновить джерело зображення та відновить початковий розмір
        def update_image_and_reset_size(animation, widget):
            self.reset_diploma_button()

        anim.bind(on_complete=update_image_and_reset_size)

        # Запустити анімацію
        anim.start(self.diploma_button)
        self.diploma_button.animation = anim

    def reset_diploma_button(self):
        # Створити анімацію відновлення початкового розміру кнопки
        anim = Animation(opacity=1, size=self.diploma_button.original_size, pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=0.1, t='out_back')

        # Запустити анімацію
        anim.start(self.diploma_button)
        self.diploma_button.animation = anim

    def upgrade_click(self, instance):
        self.upgrade_button.background_color = self.rgba_to_color(16, 100, 85, 0.8)
        cost = data['click_price']
        if data['score'] >= cost:
            data['score'] -= cost
            data['click_power'] += 1
            data['click_price'] = int(data['click_price'] * self.click_multiplier)
            self.update_score()
            self.update_click_upgrade()
            self.save_data()

    def hire_teacher(self, instance):
        cost = data['teacher_price']
        if data['score'] >= cost:
            data['score'] -= cost
            data['teachers'] += 1
            data['teacher_price'] = int(data['teacher_price'] * self.teacher_multiplier)
            self.update_score()
            self.update_teacher_upgrade()
            self.save_data()
    
    def hire_ai(self, instance):
        cost = data['ai_price']
        if data['score'] >= cost:
            data['score'] -= cost
            data['ais'] += 1
            data['ai_price'] = int(data['ai_price'] * self.ai_multiplier)
            self.update_score()
            self.update_ai_upgrade()
            self.save_data()

    def update(self, dt):
        teacher_points = data['teachers']
        offset = 15

        # Створити анімовані мітки для викладачів
        for _ in range(teacher_points):
            label = FloatingLabel(text='+1', font_size=20, opacity=0)

            x = (self.teacher_button.pos[0] + offset) + (randrange(max(1, int(self.teacher_button.size[0]))) - offset) - self.teacher_button.size[0]
            y = self.teacher_button.pos[1] + self.teacher_button.size[1]

            label.start_animation(x, y)
            self.ids.floating_labels.add_widget(label)

        # Створити анімовані мітки для ШІ
        ai_points = 0
        for _ in range(data['ais']):
            rand = randrange(10)
            ai_points += rand
            label = FloatingLabel(text=f'+{ai_points // data["ais"]}', font_size=20, opacity=0)

            x = self.ai_button.pos[0] - offset + randrange(max(1, int(self.ai_button.size[0]))) - offset - self.ai_button.size[0]
            y = self.ai_button.pos[1] + self.ai_button.size[1]
        
            label.start_animation(x, y)
            self.ids.floating_labels.add_widget(label)

        data['score'] += teacher_points + ai_points
        self.update_score()
        self.save_data()

    def save_data(self):
        with open('data.json', 'w') as f:
            json.dump(data, f)
    
    def rgba_to_color(self, red, green, blue, alpha):
        return (red/255, green/255, blue/255, alpha)

class DyplomaClickerApp(App):
    def build(self):
        from kivy.config import Config

        Config.set('graphics', 'width', '600')
        Config.set('graphics', 'height', '600')
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(GameScreen(name='game'))
        sm.current = 'main'
        return sm

app = DyplomaClickerApp()
app.run()
