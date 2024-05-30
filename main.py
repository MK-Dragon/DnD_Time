#Kivy:
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window # Remove before py --> apk
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

#KivyMD:
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import IconLeftWidget, IconRightWidget
from kivymd.uix.list import OneLineAvatarIconListItem, TwoLineAvatarIconListItem, TwoLineIconListItem
from kivymd.uix.textfield import MDTextField


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
    '''Using root. from KV file you can use functions from the Class.'''

    container = ObjectProperty(None)
    dialog = None

    dice = [4, 6, 8, 10, 12, 20]
    dice_to_roll = {}
    dice_prop = {} # {id: DiceCard(instance)} -> dice_prop[id].text = "Hello" to update text!

    def on_kv_post(self, base_widget):
        #self.reset_dice() # Deprecated
        # Set Dice to Zero
        for i in self.dice:
            print(f'\nreset i: {i}[{type(i)}]\n') # id == str ( 2, 4, etc.)
            self.dice_to_roll.update({f'{i}': 0})
        self.display_dice_card()

    def display_dice_card(self):
        self.dice_prop = {}
        # Clear widget
        self.ids.container.clear_widgets(children=None)

        # radius change
        a = 0
        #rad_b = (5, 30, 5, 30)
        #rad_a = (30, 5, 30, 5)
        rad_b = (45, 15, 15, 45) # |) (|
        rad_a = (15, 45, 45, 15)

        for i in self.dice:
            rad = rad_a if a % 2 == 0 else rad_b
            a += 1

            dice_card = DiceCard(
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
            #print(f'\n\nDice Card: {i}[{type(i)}]\n\n')
            self.dice_prop.update({i: dice_card})
            self.ids.container.add_widget(self.dice_prop[i])

            # Deprecated
            '''self.ids.container.add_widget(
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
            )'''

    def update_dice_card(self, dice:str):
        self.dice_prop[int(dice)].text = f'Roll: {self.dice_to_roll[f"{dice}"]}d{dice}'

    def plus_button(self, id):
        #print(f'\nplus id: {id}[{type(id)}]\n') # id == str ( 2, 4, etc.)
        self.dice_to_roll[f'{id}'] += 1
        #self.display_disce_card() # deprecated
        self.update_dice_card(id)

    def minus_button(self, id):
        if self.dice_to_roll[f'{id}'] > 0:
            self.dice_to_roll[f'{id}'] -= 1
            #self.display_disce_card() # deprecated
            self.update_dice_card(id)

    def icon_button(self, id):
        #print(f'Icon [{id}]')
        #print(f'Roll a d{id} -> {Roll_Dice(1, dice=int(id))[0]}')
        #print(self.dice_to_roll)

        items_roll:list = []
        items_roll.append(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon=f'dice-d{id}'),
                IconRightWidget(icon=f'dice-d{id}'),
                text=f'd{id} = [ {Roll_Dice(1, dice=int(id))[0]} ]'
            ),

        )
        # print('\t', i)

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

    def reset_dice(self):
        for i in self.dice:
            #print(f'\nreset i: {i}[{type(i)}]\n') # id == str ( 2, 4, etc.)
            self.dice_to_roll.update({f'{i}': 0})
            self.update_dice_card(f'{i}')

    def roll_dice_button(self):
        #dialog = None # Reset
        results:list[tuple] = [] # like: [('d6, [3,6,1], 10),]

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
            #dice = f'dice-{dice}'
            rolls_str = ''
            for val in rolls:
                rolls_str += f'[{val}] '
            #rolls_str += f' = {total}'
            #print(f'{rolls_str = }')

            # TwoLineIconListItem # TwoLineAvatarIconListItem

            items_roll.append(
                TwoLineIconListItem(
                    IconLeftWidget(icon=f'dice-{dice}'),
                    text=f'{len(rolls)}{dice} = {total}',
                    secondary_text=rolls_str
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
        self.THEME_pri_light = "#80fc4e" #'#fadf9b' #"#f2c75a"
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