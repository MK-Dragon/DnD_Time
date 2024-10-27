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
from kivymd.uix.list import OneLineAvatarIconListItem, TwoLineAvatarIconListItem, TwoLineIconListItem, OneLineListItem
from kivymd.uix.textfield import MDTextField


#Others:
from random import randint, choice
import json



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
            #print(f'\nreset i: {i}[{type(i)}]\n') # id == str ( 2, 4, etc.)
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

    def roll_euro_button(self, num_max, n_num, star_max, n_star):
        '''
        EuroMilhões: 5x (1-50) + 2x (1-12)

        EuroDreams: 6x (1-40) + 1x (1-5)
        '''

        #print("\nRolling Euro Milhões:")

        list_num = []
        list_star = []

        # Nums
        for d in range(n_num):
            while True:
                rr = Roll_Dice(1, num_max)
                if rr not in list_num:
                    list_num.append(rr[0])
                    break

        for d in range(n_star):
            while True:
                rr = Roll_Dice(1, star_max)
                if rr not in list_star:
                    list_star.append(rr[0])
                    break

        #print(f'\tNum {list_num.sort()}')
        #print(f'\tStar {list_star.sort()}\n')

        str_num = ''
        a = 0
        for i in list_num:
            str_num += f'{i}'
            if a != n_num-1:
                str_num += ' - '
            a += 1

        str_star = ''
        a = 0
        for i in list_star:
            str_star += f'{i}'
            if a != n_star-1:
                str_star += ' - '
            a += 1


        #print(f'\tNum {str_num}')
        #print(f'\tStar {str_star}\n')

        # sorting:
        items_roll = []

        # TwoLineIconListItem # TwoLineAvatarIconListItem

        items_roll.append(
            TwoLineIconListItem(
                IconLeftWidget(icon=f'dice-5'),
                text=f'{str_num}',
                secondary_text=f'{str_star}'
            )
        )

        # Popup:
        self.dialog = MDDialog(
            title="Euro Rolls:",
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

class Content(BoxLayout):
    container = ObjectProperty(None)


class Main(MDApp):
    # Default Theme:
    user_theme: dict = {
        'style': 'Light',
        'primary': 'LightBlue',
        'accent': 'Blue'
    }

    colors = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo',
              'Blue', 'LightBlue', 'Cyan', 'Teal','Green',
              'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange',
              'DeepOrange', 'Brown', 'Gray', 'BlueGray']

    dialog = None

    def __init__(self, **kwargs):
        self.title = "D&D Time!"
        super().__init__(**kwargs)

    def build(self):
        '''using app.mainwindow from kv file can use funtions from MainWindow() Class!!'''



        # Read User Theme from JSON File
        try:
            self.Read_Theme_File()
            print("\n** User Theme **")
            print(self.user_theme)

        # if file doesn't exist make one!
        except:
            self.Write_Theme_File()
            print("Theme File Created")

        self.apply_user_theme()

        # Screen Management:
        self.screen_manager = ScreenManager()

        self.main_window = MainWindow()
        screen = Screen(name='Main Window')
        screen.add_widget(self.main_window)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def apply_user_theme(self) -> None:
        '''
        Applies User Theme to App
        This is used to Update the Theme if it Changes
        :return:
        '''
        # Theme:
        self.theme_cls.theme_style = self.user_theme['style']
        self.theme_cls.primary_palette = self.user_theme['primary'] #'Blue' # self.user_theme['primary'] # "LightBlue"
        self.theme_cls.accent_palette = self.user_theme['accent']

        # TODO: deprecate Theme below...
        self.THEME_pri = "#fcbc0d"  # Orange
        self.THEME_pri_light = "#80fc4e"  # '#fadf9b' #"#f2c75a"
        self.THEME_sec = '#000000'  # "#19194c" # DarkBlue / "#7d1923" #DarkRed
        self.THEME_acc = "#0080ff"  # Blue
        self.THEME_txt = "#787878"  # Grey

    def Read_Theme_File(self) -> None:
        '''
        Reads User Setting and updates the Theme
        :return:
        '''
        with open('user_settings.json') as json_file:
            data = json.load(json_file)

            print(f'{type(data) = }')
            print(f'{data = }')

            self.user_theme = data

    def Write_Theme_File(self) -> None:
        with open("user_settings.json", "w") as outfile:
            json.dump(self.user_theme, outfile, indent = 4, sort_keys= True)

    def change_theme_setting(self, setting:str, color:str = '') -> None:
        print(f'\n\tSetting {setting}')
        print(f'\t\t\t{self.user_theme[setting] = }')

        if setting == 'style':
            self.user_theme['style'] = 'Dark' if self.user_theme['style'] == 'Light' else 'Light'

        elif setting == 'accent':
            self.user_theme['accent'] = color

        elif setting == 'primary':
            self.user_theme['primary'] = color

        print(f'\t\t\t{self.user_theme[setting] = } -> {color = }\n')

        # Save Changes
        self.Write_Theme_File()
        # Update Theme
        self.apply_user_theme()

    def popup_color_picker(self, setting):
        print(f'{setting = } - {type(setting) = }')

        content = Content()

        for color in self.colors:
            print(f'\t{color}')
            if setting == 'Primary':
                content.ids.container.add_widget(
                    OneLineAvatarIconListItem(
                        IconLeftWidget(
                            icon='duck'
                            # theme_icon_color="Custom",
                            # icon_color=color
                        ),
                        text=f"{color}",
                        id=color,
                        on_release=self.pick_primary_color
                    )
                )
            else:
                content.ids.container.add_widget(
                    OneLineAvatarIconListItem(
                        IconLeftWidget(
                            icon='duck'
                            # theme_icon_color="Custom",
                            # icon_color=color
                        ),
                        text=f"{color}",
                        id=color,
                        on_release=self.pick_accent_color
                    )
                )

        self.dialog = MDDialog(
            title=setting,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )

        self.dialog.open()

    def pick_primary_color(self, instance):
        print(f'[{instance.id}] -> Primary')
        self.dialog.dismiss()
        self.change_theme_setting('primary', instance.id)
        self.apply_user_theme()

    def pick_accent_color(self, instance):
        print(f'[{instance.id}] -> Accent')
        self.dialog.dismiss()
        self.change_theme_setting('accent', instance.id)
        self.apply_user_theme()




if __name__ == '__main__':
    Window.size = (405, 700)  # Remove before py --> apk
    main_app = Main()
    main_app.run()