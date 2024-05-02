from random import randrange
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Rotate, Rectangle
import json

try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {'score': 0, 'click_power': 1, 'teachers': 0, 'ais': 0, 'click_price': 10, 'teacher_price': 25, 'ai_price': 100}


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
        animation = Animation(pos=(x, y + 60), opacity=1, duration=.7, t='out_quad')
        animation += Animation(pos=(x, y + 100), opacity=0, duration=.1, t='out_quad')
        animation.bind(on_complete=self.remove_label)
        animation.start(self)
        self.animation = animation

    def remove_label(self, instance, value):
        self.parent.remove_widget(self)

class ButtonInteraction(ImageButton):
    duration = NumericProperty(1)
    rotation = NumericProperty(33)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation = None
        self.rotation = kwargs.pop('rotation')

    def start_animation(self):
        animation = Animation(rotation=45, duration=self.duration, t='out_quad')
        animation.start(self)
        self.animation = animation

    def remove_label(self, instance, value):
        self.parent.remove_widget(self)

class GameScreen(Screen):
    click_multiplier = 1.5
    teacher_multiplier = 1.8
    ai_multiplier = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        information_block = AnchorLayout(anchor_x='left', anchor_y='top', size_hint = (1, .4))
        interaction_block = BoxLayout(orientation='vertical', size_hint = (1, 1))
        footer_block = BoxLayout(orientation='vertical', size_hint = (1, 1))
        market_block = BoxLayout(orientation='horizontal', size_hint = (1, .1))
        teachers_block = BoxLayout(orientation='vertical')
        ais_block = BoxLayout(orientation='vertical')
        main_block = GridLayout(rows = 4)
        self.floating_labels = FloatLayout()
        self.background_image = Image(source='assets/bg.jpg', allow_stretch=True, size_hint=(1, 1), opacity=.5)
        self.add_widget(self.background_image)
        main_block.add_widget(self.floating_labels)

        self.label = Label(bold=True, font_size=40)
        self.diploma_button = ButtonInteraction(
            rotation=33,
            source='assets/dyploma.png',
            size=(200, 200),
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.diploma_button.bind(on_press=self.click_diploma)

        self.upgrade_button = Button(
            on_press=self.upgrade_click,
            background_color=self.rgba_to_color(32, 205, 175, 0.8),
            background_normal='',
            background_down='',
            color=self.rgba_to_color(255, 255, 255, 1),
            font_size=20,
            size_hint=(1, .1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.teacher_button = Button( 
            on_press=self.hire_teacher,
            background_color=self.rgba_to_color(32, 205, 175, 0.8),
            background_normal='',
            background_down='',
            color=self.rgba_to_color(255, 255, 255, 1),
            font_size=15,
            size_hint=(1, .3),
        )
        self.ai_button = Button(
            on_press=self.hire_ai,
            background_color=self.rgba_to_color(32, 205, 175, 0.8),
            background_normal='',
            background_down='',
            color=self.rgba_to_color(255, 255, 255, 1),
            font_size=15,
            size_hint=(1, .3),
        )
        
        information_block.add_widget(self.label)
        interaction_block.add_widget(self.diploma_button)

        teachers_block.add_widget(self.teacher_button)
        ais_block.add_widget(self.ai_button)

        market_block.add_widget(teachers_block)
        market_block.add_widget(ais_block)

        footer_block.add_widget(self.upgrade_button)
        footer_block.add_widget(market_block)

        main_block.add_widget(information_block)
        main_block.add_widget(interaction_block)
        main_block.add_widget(footer_block)

        self.add_widget(main_block)
        self.update_score()
        self.update_click_upgrade()
        self.update_teacher_upgrade()
        self.update_ai_upgrade()
        self.event = None
        Clock.schedule_interval(self.update, 1)

    def update_score(self):
        self.label.text = f'Очки: {data["score"]}'

    def update_click_upgrade(self):
        self.upgrade_button.text = 'Прокачати клік [+1] \n({} очок)  |  Вартість: {}'.format(data["click_power"], data["click_price"])

    def update_teacher_upgrade(self):
        self.teacher_button.text = f'Найняти викладача [+1] \n({data["teachers"]} очок/сек)  |  Вартість: {data["teacher_price"]}'

    def update_ai_upgrade(self):
        self.ai_button.text = f'Найняти ШІ [+(0-10)] \n({data["ais"]} ШІ)  |  Вартість: {data["ai_price"]}'


    def click_diploma(self, instance):
        data['score'] += data['click_power']
        self.diploma_button.start_animation()
        self.update_score()
        self.save_data()

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

        # Створити анімовані мітки для викладачів
        for _ in range(teacher_points):
            label = FloatingLabel(text='+1', font_size=20, opacity=0)
            label.start_animation(self.teacher_button.pos[0] - randrange(max(1, int(self.teacher_button.size[0] - 20))),
                                self.teacher_button.pos[1] + randrange(max(1, int(self.teacher_button.size[1]))))
            self.floating_labels.add_widget(label)

        # Створити анімовані мітки для ШІ
        ai_points = 0
        for _ in range(data['ais']):
            rand = randrange(10)
            ai_points += rand
            label = FloatingLabel(text=f'+{ai_points // data["ais"]}', font_size=20, opacity=0)
            label.start_animation(self.ai_button.pos[0] - randrange(max(1, int(self.ai_button.size[0] - 20))),
                                self.ai_button.pos[1] + randrange(max(1, int(self.ai_button.size[1]))))
            self.floating_labels.add_widget(label)

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
        return sm

app = DyplomaClickerApp()
app.run()