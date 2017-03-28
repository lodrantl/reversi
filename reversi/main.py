"""
.. module:: reversi.main
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com, Lenart Treven <lenart.treven44@gmail.com>

Glavni razred reversi aplikacije, vsebuje konfiguracijo uporabniškega vmesnika

"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from enum import Enum
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import NumericProperty, ListProperty, OptionProperty, StringProperty
from kivy.uix.button import ButtonBehavior

from kivy.metrics import sp

from igra import Stanje, Igra


Window.minimum_width = 500
Window.minimum_height = 550


# Declare all application screens.
class MeniZaslon(Screen):
    pass
class NastavitveZaslon(Screen):
    pass
class PravilaZaslon(Screen):
    pass
class IgraZaslon(Screen):
    ime_crnega = StringProperty('Računalnik')
    ime_belega = StringProperty('Človek')

class LepGumb(Button):
    """
    Lepo oblikovan gumb, za uporabo v celotni aplikaciji
    """
    notranja_barva = ListProperty([1, 1, 1, 1])

    def on_state(self, event, x):
        """
        Ob pritisku gumba spremeni notranjo barvo
        """
        if x == 'down':
            self.notranja_barva = [1, 0, 1, 1]
        elif x == 'normal':
            self.notranja_barva = [1, 1, 1, 1]


class Polje(ButtonBehavior, Image):
    """
    Razred vsake polja na plošči, hrani stanje in pa pozna svoje koordinate
    """
    stanje = OptionProperty(Stanje.PRAZNO, options=[Stanje.BELO, Stanje.CRNO, Stanje.PRAZNO, Stanje.MOGOCE])
    koordinate = ListProperty([-1, -1])

    def on_press(self):
        """
        Ob pritisku, če je polje prazno, odigra potezo
        :return:
        """
        if self.stanje == Stanje.MOGOCE:
            self.parent.odigraj_potezo(self.koordinate)

    def nastavi(self, barva):
        """
        Nastavi barvo tega polja
        :param barva: željena barva
        :return:
        """
        self.stanje = barva


class Deska(RelativeLayout):
    """
    Razred, ki vsebuje desko, ob inicializaciji nase postavi 64 polj in jih shrani v tabelo. Hrani tudi podatke o tem kdo je na potezi.
    """
    na_potezi = OptionProperty(Stanje.BELO, options=[Stanje.BELO, Stanje.CRNO])
    polja = []
    igra = Igra()
    stevilo_crnih = NumericProperty(2)
    stevilo_belih = NumericProperty(2)

    def __init__(self, **kwargs):
        """
        Zgenerira polja na deski in si jih shrani v matriko self.polja
        :param kwargs:
        """
        super(Deska, self).__init__(**kwargs)
        for i in range(8):
            self.polja.append([])
            for j in range(8):
                t = Polje(pos_hint={'x': .125 * j, 'y': .125 * i}, koordinate=[i,j])
                self.add_widget(t)
                self.polja[i].append(t)
        self.igra = Igra()
        self.uvozi_igro()

    def izvozi_igro(self):
        polja = [[polje.stanje for polje in vrstica] for vrstica in self.polja]
        return Igra(self.na_potezi, polja)

    def uvozi_igro(self):
        self.stevilo_belih = self.igra.stevilo_belih
        self.stevilo_crnih = self.igra.stevilo_crnih
        for i in range(8):
            for j in range(8):
                if (i, j) in self.igra.mozne_poteze:
                    self.polja[i][j].nastavi(Stanje.MOGOCE)
                else:
                    self.polja[i][j].nastavi(self.igra.deska[i][j])

    def odigraj_potezo(self, koordinate):
        self.igra.odigraj_potezo(koordinate)
        self.uvozi_igro()
        print(koordinate)

class ReversiApp(App):
    barva_primarna = ListProperty([.5, 0, .5, 1])
    barva_sekundarna = ListProperty([0, .5, 0, 1])

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
