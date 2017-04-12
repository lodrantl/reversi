"""
.. module:: reversi.tema
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com>, Lenart Treven <lenart.treven44@gmail.com>

Kivy barvna tema aplikacije

"""

from kivy.utils import get_color_from_hex as from_hex
from kivy.properties import ListProperty
from kivy.uix.widget import Widget


class Tema(Widget):
    """
    Kivy barvna tema aplikacije
    """
    deska = ListProperty(from_hex('#8BC34A'))
    deska_rob = ListProperty(from_hex('#689F38'))
    ozadje = ListProperty()
    ozadje_temno = ListProperty()
    ozadje_svetlo = ListProperty()
    senca = ListProperty()
    poudarjeno = ListProperty()
    tekst_ozadje = ListProperty()
    tekst_ozadje_temno = ListProperty()
    tekst_locila = ListProperty()
    locila = ListProperty()
    onemogoceno = ListProperty()

    def __init__(self, ime):
        super(Tema, self).__init__()
        self.nastavi(ime)

    def nastavi(self, ime):
        """
        Zamenja temo
        :param ime: ime nove teme
        """

        if ime == 'svetla':
            self.svetla()
        elif ime == 'modra':
            self.modra()
        elif ime == 'oranzna':
            self.oranzna()

    def svetla(self):
        """
        Belo ozadje z modrimi in zelnimi poudarki
        """
        self.ozadje = from_hex('#FFFFFF')
        self.ozadje_temno = from_hex('#3F51B5')
        self.ozadje_svetlo = from_hex('#6677E3')
        self.senca = from_hex('#757575')
        self.poudarjeno = from_hex('#8BC34A')
        self.tekst_ozadje = from_hex('#3F51B5')
        self.tekst_ozadje_temno = from_hex('#FFFFFF')
        self.tekst_locila = from_hex('#FFFFFF')
        self.locila = from_hex('#3F51B5')
        self.onemogoceno = from_hex('#505050')

    def modra(self):
        """
        Modro ozadje z zelenimi poudarki
        """
        self.ozadje = from_hex('#3F51B5')
        self.ozadje_temno = from_hex('#303F9F')
        self.ozadje_svetlo = from_hex('#C5CAE9')
        self.poudarjeno = from_hex('#8BC34A')
        self.tekst_ozadje = from_hex('#FFFFFF')
        self.tekst_ozadje_temno = from_hex('#FFFFFF')
        self.senca = from_hex('#757575')
        self.tekst_locila = from_hex('#212121')
        self.locila = from_hex('#FFFFFF')
        self.onemogoceno = from_hex('#AAAAAA')

    def oranzna(self):
        """
        Oranžno ozadje z zelenimi poudarkis
        """
        self.ozadje = from_hex('#FF5722')
        self.ozadje_temno = from_hex('#E64A19')
        self.ozadje_svetlo = from_hex('#FFCCBC')
        self.senca = from_hex('#757575')
        self.poudarjeno = from_hex('#8BC34A')
        self.tekst_ozadje = from_hex('#FFFFFF')
        self.tekst_ozadje_temno = from_hex('#FFFFFF')
        self.tekst_locila = from_hex('#212121')
        self.locila = from_hex('#FFFFFF')
        self.onemogoceno = from_hex('#AAAAAA')
