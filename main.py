#Kivy:
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window # Remove before py --> apk

#KivyMD:
from kivymd.app import MDApp
from kivymd.uix.card import MDCard

#Others:
from random import randint, choice


def Roll_Dice(num_rolls:int, dice:int) -> list:
    '''Roll 2d6 -> [a, b]'''
    rolls = []
    for _ in range(num_rolls):
        a = []
        # to add more randness, roll 5x , pick one at rand
        for i in range(5):
            a.append(randint(1, dice))
        rolls.append(choice(a))
    return rolls


class MainWindow(Screen):
    '''Using root. from KV file you can use funtions from the Class.'''

    container = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.dysplay_disce_card()

    def dysplay_disce_card(self):
        self.ids.container.clear_widgets(children=None)
        for i in range(6):
            self.ids.container.add_widget(
                DiceCard(
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style="elevated",
                    text=f'Card {i}',
                    md_bg_color="#f6eeee",
                    shadow_softness=2,
                    shadow_offset=(0, 1)
                )
            )



class DiceCard(MDCard):
    text = ObjectProperty(None)


class Main(MDApp):
    def __init__(self, **kwargs):
        self.title = "D&D Time!"
        super().__init__(**kwargs)

    def build(self):
        '''using app.mainwindow from kv file can use funtions from MainWindow() Class!!'''

        self.screen_manager = ScreenManager()

        self.main_window = MainWindow()
        screen = Screen(name='Main Window')
        screen.add_widget(self.main_window)
        self.screen_manager.add_widget(screen)

        return self.screen_manager



if __name__ == '__main__':
    Window.size = (405, 700)  # Remove before py --> apk
    main_app = Main()
    main_app.run()