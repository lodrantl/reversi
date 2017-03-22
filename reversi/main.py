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

BELO = 'belo'
CRNO = 'crno'
PRAZNO = 'prazno'
POTEZA = 'poteza'

# Declare all application screens.
class MeniZaslon(Screen):
    pass
class NastavitveZaslon(Screen):
    pass
class IgraZaslon(Screen):
    pass
class PravilaZaslon(Screen):
    pass

class Polje(Image):
    stanje = StringProperty(PRAZNO)
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.stanje ==  PRAZNO:
                print(self.parent.na_vrsti)
                self.stanje = self.parent.na_vrsti
                if self.parent.na_vrsti == BELO:
                    self.parent.na_vrsti = CRNO
                else:
                    self.parent.na_vrsti = BELO


class Deska(RelativeLayout):
    na_vrsti = StringProperty(BELO)
    def __init__(self, **kwargs):
        super(Deska, self).__init__(**kwargs)
        for i in range(8):
            for j in range(8):
                t = Polje(pos_hint={'x': .125 * j, 'y': .125 * i})
                if (i, j) == (3,3) or (i, j) == (4, 4):
                    t.state = BELO
                elif (i, j) == (3, 4) or (i, j) == (4, 3):
                    t.state = CRNO
                self.add_widget(t)


class ReversiApp(App):
    def zacni_en_igralec(self):
        self.root.current = 'igra'

    def zacni_dva_igralca(self):
        self.root.current = 'igra'

    def koncaj_igro(self):
        self.root.current = 'meni'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MeniZaslon(name='meni'))
        sm.add_widget(NastavitveZaslon(name='nastavitve'))
        sm.add_widget(IgraZaslon(name='igra'))
        sm.add_widget(PravilaZaslon(name='pravila'))
        return sm


if __name__ == '__main__':
    ReversiApp().run()
