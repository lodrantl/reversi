"""
.. module:: reversi.main
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com>, Lenart Treven <lenart.treven44@gmail.com>

Glavni modul reversi aplikacije, vsebuje konfiguracijo uporabniškega vmesnika

"""

import logging

logger = logging.getLogger('reversi_main')
logger.setLevel(logging.DEBUG)

# Spremeni trenutno mapo, če je aplikacija zagnana kot PyInstaller exe (dirty)
import sys
import os

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# Nastavi velikost okna
from kivy.config import Config

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '550')

# Nastavi minimalno velikost okna
from kivy.core.window import Window

Window.minimum_width = 500
Window.minimum_height = 550

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import NumericProperty, ListProperty, OptionProperty, StringProperty, ObjectProperty, \
    BooleanProperty
from kivy.uix.button import ButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.modalview import ModalView
from kivy.clock import mainthread

from igra import Stanje, Igra
from hoverable import HoverBehavior
from racunalnik import Racunalnik
from clovek import Clovek
from tema import Tema


class Polje(ButtonBehavior, AnchorLayout, HoverBehavior):
    """
    Razred vsakega polja na plošči, hrani stanje in pozna svoje koordinate
    """
    koordinate = ListProperty()
    stanje = OptionProperty(Stanje.PRAZNO, options=[Stanje.BELO, Stanje.CRNO, Stanje.PRAZNO, Stanje.MOGOCE])
    moznost = StringProperty('')

    def on_enter(self):
        """
        Če se z miško pomaknemo v možno polje se v polju pojavi prosojen žeton
        :return:
        """
        if self.stanje == Stanje.MOGOCE:
            self.moznost = self.parent.na_potezi

    def on_leave(self):
        """
        Izbrišemo prosojen žeton
        :return:
        """
        if self.moznost:
            self.moznost = ''

    def on_press(self):
        """
        Ob pritisku, če je polje prazno, odigra potezo
        :return:
        """

        if self.stanje == Stanje.MOGOCE:
            self.moznost = ''
            self.parent.igralca[self.parent.na_potezi].klik(self.koordinate)

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
    obstaja_zgodovina = BooleanProperty(False)

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

    def nova_igra(self, tezavnost=None, barva=None):
        """
        Začne novo igro
        :param tezavnost: tezavnost racunalnika (od 0 do 2) oz. None v primeru igre za 2 igralca
        :param barva: barva cloveskega igralca oz. None
        """
        if tezavnost is not None and barva is not None:
            self.ime_belega = 'Igralec' if barva == Stanje.BELO else 'Računalnik'
            self.ime_crnega = 'Računalnik' if barva == Stanje.BELO else 'Igralec'

            self.igralca[barva] = Clovek(self.odigraj_potezo)
            self.igralca[Stanje.obrni(barva)] = Racunalnik(self.odigraj_potezo, tezavnost)
        else:
            self.ime_belega = 'Igralec 1'
            self.ime_crnega = 'Igralec 2'
            self.igralca[Stanje.CRNO] = Clovek(self.odigraj_potezo)
            self.igralca[Stanje.BELO] = Clovek(self.odigraj_potezo)

        self.igra = Igra()
        self.osvezi()
        self.igralca[self.na_potezi].zacni_potezo(self.igra)

    def osvezi(self):
        """
        Osveži desko na ekranu z novim stanjem v self.igra
        :return:
        """
        self.stevilo_belih, self.stevilo_crnih = self.igra.stevilo_zetonov()

        dolzina = len(self.igra.zgodovina)
        tip = type(self.igralca[self.na_potezi])
        self.obstaja_zgodovina = (dolzina > 1) or (dolzina == 1 and tip == Clovek)

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
        Odigra potezo na pritisnjenem polju v glavni niti
        :param koordinate: koordinate, tuple (x, y)
        :return:
        """

        self.igra.odigraj_potezo(koordinate)
        self.osvezi()

        if self.igra.koncana:
            po = PonoviIgroPopup(deska=self)
            po.open()
        else:
            self.igralca[self.na_potezi].zacni_potezo(self.igra)

    def ponovi_igro(self):
        """
        Začne novo igro z istimi igralci
        """
        self.igra = Igra()
        self.osvezi()
        self.igralca[self.na_potezi].zacni_potezo(self.igra)

    def koncaj_igro(self):
        """
        Konča igro in te vrne na začetni zaslon
        """
        for i in self.igralca.values():
            if type(i) == Racunalnik:
                i.prekini()
        self.manager.current = 'meni'

    def koncaj_igro_popup(self):
        """
        Prikaže dialog z vprašanjem ali ste prepričani zapustit igro
        """
        po = KoncajIgroPopup(deska=self)
        po.open()

    def razveljavi(self):
        """
        Razveljavi zadnjo človeško potezo
        """
        self.igra.razveljavi()
        if type(self.igralca[self.igra.na_potezi]) == Racunalnik:
            self.igra.razveljavi()
        self.osvezi()
        self.igralca[self.na_potezi].zacni_potezo(self.igra)


class PonoviIgroPopup(ModalView):
    """
    Prikaže dialog z imenom zmagovalca in vprašanjem o ponovitvi igre
    """
    deska = ObjectProperty()

    def __init__(self, **kwargs):
        super(PonoviIgroPopup, self).__init__(**kwargs)
        self.deska = kwargs['deska']


class KoncajIgroPopup(ModalView):
    """
    Prikaže dialog z vprašanjem o končanju igre
    """
    deska = ObjectProperty()

    def __init__(self, **kwargs):
        super(KoncajIgroPopup, self).__init__(**kwargs)
        self.deska = kwargs['deska']


class ReversiApp(App):
    """
    Glavni Kivy Application razred, definira ScreenManager z našimi zasloni in vsebuje par uporabnih konstant
    """
    tema = ObjectProperty(Tema('svetla'))

    @staticmethod
    def radio_vrednost(skupina):
        """      
        :param skupina: ime skupine ToggleButtonov
        :return: trenutno vrednost skupine
        """
        gumb = [x for x in ToggleButton.get_widgets(skupina) if x.state == 'down']
        if gumb:
            return gumb[0].value
        else:
            raise Exception('Noben gumb ni izbran!!')

    def build(self):
        self.icon = 'grafika/ikona.png'


if __name__ == '__main__':
    ReversiApp().run()
