"""
.. module:: reversi.main
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com>, Lenart Treven <lenart.treven44@gmail.com>

Glavni razred reversi aplikacije, vsebuje konfiguracijo uporabniškega vmesnika

"""

import sys
import os
import logging

# Spremeni trenutno mapo, če je aplikacija zagnana kot PyInstaller exe (dirty)
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

import kivy
kivy.require('1.9.1')

# Nastavi velikost okna
from kivy.config import Config
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '550')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, OptionProperty, StringProperty, ObjectProperty
from kivy.uix.button import ButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.modalview import ModalView
from kivy.clock import mainthread

from igra import Stanje, Igra
from hoverable import HoverBehavior
from racunalnik import Racunalnik
from clovek import Clovek

# Nastavi minimalno velikost okna
Window.minimum_width = 500
Window.minimum_height = 550

logger = logging.getLogger('reversi_main')
logger.setLevel(logging.DEBUG)


# Declare all application screens.
class MeniZaslon(Screen):
    pass


class NastavitveZaslon(Screen):
    def radio_vrednost(self, skupina):
        gumb = [x for x in ToggleButton.get_widgets(skupina) if x.state == 'down']
        if gumb:
            return gumb[0].value
        else:
            raise Exception('Noben gumb ni izbran!!')


class PravilaZaslon(Screen):
    pass


class IgraZaslon(Screen):
    pass


class Polje(ButtonBehavior, AnchorLayout, HoverBehavior):
    """
    Razred vsake polja na plošči, hrani stanje in pa pozna svoje koordinate
    """
    koordinate = ListProperty()
    stanje = OptionProperty(Stanje.PRAZNO, options=[Stanje.BELO, Stanje.CRNO, Stanje.PRAZNO, Stanje.MOGOCE])
    mozno = StringProperty('')

    def on_enter(self):
        """
        Če se z miško pomaknemo v možno polje se v polju pojavi prosojen žeton
        :return:
        """
        print("on enter", self.koordinate)
        if self.stanje == Stanje.MOGOCE:
            self.mozno = self.parent.na_potezi

    def on_leave(self):
        """
        Izbrišemo prosojen žeton
        :return:
        """
        print("on leave", self.koordinate)
        if self.mozno:
            self.mozno = ''

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
    ime_belega = StringProperty()
    ime_crnega = StringProperty()
    stevilo_crnih = NumericProperty()
    stevilo_belih = NumericProperty()

    na_potezi = OptionProperty(Stanje.BELO, options=[Stanje.BELO, Stanje.CRNO])

    def __init__(self, **kwargs):
        """
        Zgenerira polja na deski in si jih shrani v matriko self.polja
        :param kwargs: argumenti za Kivy RelativeLayout
        """
        super(Deska, self).__init__(**kwargs)
        self.polja = []
        self.igra = None
        self.igralca = dict()

        for i in range(8):
            self.polja.append([])
            for j in range(8):
                t = Polje(pos_hint=dict(x=.125 * j, y=.125 * i), koordinate=[i, j])
                self.add_widget(t)
                self.polja[i].append(t)

    def nova_igra(self, tezavnost=False, barva=False):
        if tezavnost is not False and barva is not False:
            if barva == Stanje.BELO:
                self.ime_belega = 'Igralec'
                self.ime_crnega = 'Računalnik'
            else:
                self.ime_crnega = 'Igralec'
                self.ime_belega = 'Računalnik'

            self.igralca[barva] = Clovek()
            self.igralca[Stanje.obrni(barva)] = Racunalnik(self.odigraj_potezo, tezavnost, Stanje.obrni(barva))
        else:
            self.ime_belega = 'Igralec 1'
            self.ime_crnega = 'Igralec 2'
            self.igralca[Stanje.CRNO] = Clovek()
            self.igralca[Stanje.BELO] = Clovek()

        self.igra = Igra()
        self.osvezi()
        self.igralca[self.na_potezi].zacni_potezo(self.igra)

    def osvezi(self):
        """
        Osveži desko na ekranu z novim stanjem v self.igra
        :return:
        """
        self.stevilo_belih, self.stevilo_crnih = self.igra.stevilo_zetonov()

        self.na_potezi = self.igra.na_potezi
        poteze = self.igra.mozne_poteze()
        for i in range(8):
            for j in range(8):
                if (i, j) in poteze and type(self.igralca[self.na_potezi]) == Clovek:
                    self.polja[i][j].nastavi(Stanje.MOGOCE)
                else:
                    self.polja[i][j].nastavi(self.igra.deska[i][j])

    @mainthread
    def odigraj_potezo(self, koordinate):
        """
        Odigra potezo na pritisnjenem polju
        :param koordinate: koordinate, tuple (x, y)
        :return:
        """

        self.igra.odigraj_potezo(koordinate)
        self.osvezi()

        if self.igra.koncana:
            po = PonoviIgroPopup(deska = self)
            po.open()
        else:
            self.igralca[self.na_potezi].zacni_potezo(self.igra)

    def ponovi_igro(self):
        self.igra = Igra()
        self.osvezi()
        self.igralca[self.na_potezi].zacni_potezo(self.igra)

    def koncaj_igro(self):
        for i in self.igralca.values():
            if type(i) == Racunalnik:
                i.prekini()
        self.manager.current = 'meni'

    def koncaj_igro_popup(self):
        po = KoncajIgroPopup(deska=self)
        po.open()

    def razveljavi(self):
        #TODO
        pass


class PonoviIgroPopup(ModalView):
    deska = ObjectProperty()
    def __init__(self, **kwargs):
        super(PonoviIgroPopup, self).__init__(**kwargs)
        self.deska = kwargs['deska']


class KoncajIgroPopup(ModalView):
    deska = ObjectProperty()
    def __init__(self, **kwargs):
        super(KoncajIgroPopup, self).__init__(**kwargs)
        self.deska = kwargs['deska']



class ReversiApp(App):
    """
    Glavni Kivy Application razred, definira ScreenManager z našimi zasloni in vsebuje par uporabnih konstant
    """

    def build(self):
        self.icon = 'grafika/ikona.png'


if __name__ == '__main__':
    ReversiApp().run()
