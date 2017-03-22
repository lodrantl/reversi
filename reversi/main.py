from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from enum import Enum
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

WHITE = 'white'
BLACK = 'black'
EMPTY = 'empty'

# Declare all application screens.
class MenuScreen(Screen):
    pass
class SettingsScreen(Screen):
    pass
class GameScreen(Screen):
    pass
class RulesScreen(Screen):
    pass

class Tile(Image):
    state = StringProperty(EMPTY)
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.state ==  EMPTY:
                print(self.parent.turn)
                self.state = self.parent.turn
                if self.parent.turn == WHITE:
                    self.parent.turn = BLACK
                else:
                    self.parent.turn = WHITE


class Board(RelativeLayout):
    turn = StringProperty(WHITE)
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        for i in range(8):
            for j in range(8):
                t = Tile(pos_hint={'x': .125*j, 'y': .125*i})
                if (i, j) == (3,3) or (i, j) == (4, 4):
                    t.state = WHITE
                elif (i, j) == (3, 4) or (i, j) == (4, 3):
                    t.state = BLACK
                self.add_widget(t)


class ReversiApp(App):
    def start_single_player(self):
        self.root.current = 'game'

    def start_two_players(self):
        self.root.current = 'game'

    def end_game(self):
        self.root.current = 'menu'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(RulesScreen(name='rules'))
        return sm


if __name__ == '__main__':
    ReversiApp().run()
