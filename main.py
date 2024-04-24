#Kivy:
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window # Remove before py --> apk
from kivy.uix.boxlayout import BoxLayout

#KivyMD:
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.list import OneLineAvatarIconListItem

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
    dialog = None

    dice = [4, 6, 8, 10, 12, 20]
    dice_to_roll = {}

    def on_kv_post(self, base_widget):
        self.reset_dice()
        self.display_disce_card()

    def display_disce_card(self):
        # Clear widget
        self.ids.container.clear_widgets(children=None)

        # radius change
        a = 0
        rad_b = (5, 30, 5, 30)
        rad_a = (30, 5, 30, 5)

        for i in self.dice:
            rad = rad_a if a % 2 == 0 else rad_b
            a += 1

            self.ids.container.add_widget(
                DiceCard(
                    radius = rad,
                    card_id=f'{i}',
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style="elevated",
                    text=f'Roll: {self.dice_to_roll[f"{i}"]}d{i}',
                    dice_icon=f'dice-d{i}',
                    #md_bg_color= "#f6eeee",
                    shadow_softness=2,
                    shadow_offset=(0, 1)
                )
            )

    def plus_button(self, id):
        self.dice_to_roll[f'{id}'] += 1
        self.display_disce_card()

    def minus_button(self, id):

        if self.dice_to_roll[f'{id}'] > 0:
            self.dice_to_roll[f'{id}'] -= 1
            self.display_disce_card()

    def icon_button(self, id):
        #print(f'Icon [{id}]')
        print(self.dice_to_roll)

    def reset_dice(self):
        for i in self.dice:
            self.dice_to_roll.update({f'{i}': 0})

    def roll_dice_button(self):
        dialog = None # Reset
        results = [] # ('d6, [3,6,1], 10)

        #print("\nRolling:")
        for d in self.dice_to_roll:
            num_rolls = self.dice_to_roll[d]
            if num_rolls > 0:
                #print(f'\t{num_rolls}d{d}')

                rr = Roll_Dice(num_rolls=num_rolls, dice=int(d))
                results.append((f'd{d}', rr, sum(rr)))

        # sorting:
        items_roll = []
        #print("resultados:")
        for i in results:
            dice, rolls, total = i
            dice = f'dice-{dice}'
            rolls_str = ''
            for val in rolls:
                rolls_str += f' [ {val} ]'
            rolls_str += f' = {total}'
            #print(f'{rolls_str = }')

            items_roll.append(
                OneLineAvatarIconListItem(
                    IconLeftWidget(icon=dice),
                    text=rolls_str
                )
            )
            #print('\t', i)

        # Popup:
        self.dialog = MDDialog(
            title="Rolls:",
            type="confirmation",
            items=items_roll,
            content_cls=PopupRolls(),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=main_app.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()



class DiceCard(MDCard):
    text = ObjectProperty(None)
    dice_icon = ObjectProperty(None)
    card_id = ObjectProperty(None)

class PopupRolls(BoxLayout):
    pass


class Main(MDApp):
    def __init__(self, **kwargs):
        self.title = "D&D Time!"
        super().__init__(**kwargs)

    def build(self):
        '''using app.mainwindow from kv file can use funtions from MainWindow() Class!!'''

        # Theme:
        self.theme_cls.theme_style = 'Light' #"Dark"
        #self.theme_cls.primary_palette = "LightBlue"
        #self.theme_cls.accent_palette = "Orange"
        self.THEME_pri = "#fcbc0d" # Orange
        self.THEME_pri_light = '#fadf9b' #"#f2c75a"
        self.THEME_sec = '#000000' #"#19194c" # DarkBlue / "#7d1923" #DarkRed
        self.THEME_acc = "#0080ff" # Blue
        self.THEME_txt = "#787777" # Grey

        # Screen Management:
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