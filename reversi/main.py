"""
.. module:: reversi.main
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com, Lenart Treven <lenart.treven44@gmail.com>

Glavni razred reversi aplikacije, vsebuje konfiguracijo uporabniškega vmesnika

"""

# Spremeni trenutno mapo, če je aplikacija zagnana kot PyInstaller exe (dirty)
import sys
import os
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

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
from kivy.properties import NumericProperty, ListProperty, OptionProperty, StringProperty, ObjectProperty
from kivy.uix.button import ButtonBehavior
from kivy.uix.togglebutton import ToggleButton, ToggleButtonBehavior
from kivy.metrics import sp
from kivy.uix.modalview import ModalView

from reversi import Stanje, Igra, Clovek, Racunalnik, HoverBehavior

Window.minimum_width = 500
Window.minimum_height = 550


# Declare all application screens.
class MeniZaslon(Screen):
    pass
class NastavitveZaslon(Screen):
    def radio_vrednost(self, skupina):
        gumb = next([x for x in ToggleButton.get_widgets(skupina) if x.state == 'down'], None)
        if gumb:
            return gumb.text
        else:
            raise Exception('Noben gumb ni izbran!!')

class PravilaZaslon(Screen):
    pass
class IgraZaslon(Screen):
    ime_crnega = StringProperty('Računalnik')
    ime_belega = StringProperty('Človek')


class Polje(ButtonBehavior, Image, HoverBehavior):
    """
    Razred vsake polja na plošči, hrani stanje in pa pozna svoje koordinate
    """
    stanje = OptionProperty(Stanje.PRAZNO, options=[Stanje.BELO, Stanje.CRNO, Stanje.PRAZNO, Stanje.MOGOCE])
    koordinate = ListProperty([-1, -1])
    stil = StringProperty('')

    def on_enter(self):
        """
        Če se z miško pomaknemo v možno polje se v polju pojavi prosojen žeton
        :return:
        """
        if self.stanje == Stanje.MOGOCE:
            self.stil = '_' + self.parent.na_potezi

    def on_leave(self):
        """
        Izbrišemo prosojen žeton
        :return:
        """
        if self.stil.startswith('_'):
            self.stil = ''

    def on_press(self):
        """
        Ob pritisku, če je polje prazno, odigra potezo
        :return:
        """

        if self.stanje == Stanje.MOGOCE:
            self.stil = ''
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
    Razred, ki vsebuje desko, ob inicializaciji nase postavi 64 polj in jih shrani v tabelo.
    V self.igra je shranjeno trenutno stanje v obliki razreda Igra
    """
    polja = []
    igra = None

    stevilo_crnih = NumericProperty(-1)
    stevilo_belih = NumericProperty(-1)
    na_potezi = OptionProperty(Stanje.BELO, options=[Stanje.BELO, Stanje.CRNO])

    def __init__(self, **kwargs):
        """
        Zgenerira polja na deski in si jih shrani v matriko self.polja
        :param kwargs: argumenti za Kivy RelativeLayout
        """
        super(Deska, self).__init__(**kwargs)
        for i in range(8):
            self.polja.append([])
            for j in range(8):
                t = Polje(pos_hint={'x': .125 * j, 'y': .125 * i}, koordinate=[i,j])
                self.add_widget(t)
                self.polja[i].append(t)

    def nova_igra(self, tezavnost=False, barva=False):
        if tezavnost != False and barva != False:
            if barva == Stanje.BELO:
                self.beli = Clovek()
                self.crni = Racunalnik(tezavnost)
            else:
                self.beli = Racunalnik(tezavnost)
                self.crni = Clovek()
            self.igra = Igra()
            self.osvezi()
        else:
            print("nova igra")
            self.beli = Clovek()
            self.crni = Clovek()
            self.igra = Igra()
            self.osvezi()

    def osvezi(self):
        """
        Osveži desko na ekranu z novim stanjem v self.igra
        :return:
        """
        self.stevilo_crnih = self.igra.stevilo_crnih
        self.stevilo_belih = self.igra.stevilo_belih
        self.na_potezi = self.igra.na_potezi
        for i in range(8):
            for j in range(8):
                if (i, j) in self.igra.mozne_poteze:
                    self.polja[i][j].nastavi(Stanje.MOGOCE)
                else:
                    if self.igra.deska[i][j] != Stanje.PRAZNO:
                        print('polje', i, j, self.igra.deska[i][j])
                    self.polja[i][j].nastavi(self.igra.deska[i][j])

    def odigraj_potezo(self, koordinate):
        """
        Odigra potezo na pritisnjenem polju
        :param koordinate: koordinate, tuple (x, y)
        :return:
        """
        self.igra.odigraj_potezo(koordinate)
        self.osvezi()

        if not self.igra.konec:
            po = DialogKonec()
            po.open()

class DialogKonec(ModalView):
    pass

class ReversiApp(App):
    """
    Glavni Kivy Application razred, definira ScreenManager z našimi zasloni in vsebuje par uporabnih konstant
    """
    igra_zaslon = ObjectProperty()

    def koncaj_igro(self):
        self.root.current = 'meni'

    def build(self):
        self.icon = 'grafika/ikona.png'
        sm = ScreenManager()
        sm.add_widget(MeniZaslon(name='meni'))
        sm.add_widget(NastavitveZaslon(name='nastavitve'))
        self.igra_zaslon = IgraZaslon(name='igra')
        sm.add_widget(self.igra_zaslon)
        sm.add_widget(PravilaZaslon(name='pravila'))
        return sm


if __name__ == '__main__':
    ReversiApp().run()
