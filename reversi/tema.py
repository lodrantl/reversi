from kivy.utils import get_color_from_hex as hex
from kivy.properties import ListProperty
from kivy.uix.widget import Widget


class Tema(Widget):
    deska = ListProperty()
    deska_rob = ListProperty()
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
        self.deska = hex('#8BC34A')
        self.deska_rob = hex('#689F38')
        self.nastavi(ime)


    def nastavi(self, ime):
        if ime == 'svetla':
            self.svetla()
        elif ime == 'modra':
            self.modra()
        elif ime == 'oranzna':
            self.oranzna()

    def svetla(self):
        self.ozadje = hex('#FFFFFF')
        self.ozadje_temno = hex('#3F51B5')
        self.ozadje_svetlo = hex('#6677E3')
        self.senca = hex('#757575')
        self.poudarjeno = hex('#8BC34A')
        self.tekst_ozadje = hex('#3F51B5')
        self.tekst_ozadje_temno = hex('#FFFFFF')
        self.tekst_locila = hex('#FFFFFF')
        self.locila = hex('#3F51B5')
        self.onemogoceno = hex('#505050')

    def modra(self):
        self.ozadje = hex('#3F51B5')
        self.ozadje_temno = hex('#303F9F')
        self.ozadje_svetlo = hex('#C5CAE9')
        self.poudarjeno = hex('#8BC34A')
        self.tekst_ozadje = hex('#FFFFFF')
        self.tekst_ozadje_temno = hex('#FFFFFF')
        self.senca = hex('#757575')
        self.tekst_locila = hex('#212121')
        self.locila = hex('#FFFFFF')
        self.onemogoceno = hex('#AAAAAA')

    def oranzna(self):
        self.ozadje = hex('#FF5722')
        self.ozadje_temno = hex('#E64A19')
        self.ozadje_svetlo = hex('#FFCCBC')
        self.senca = hex('#757575')
        self.poudarjeno = hex('#8BC34A')
        self.tekst_ozadje = hex('#FFFFFF')
        self.tekst_ozadje_temno = hex('#FFFFFF')
        self.tekst_locila = hex('#212121')
        self.locila = hex('#FFFFFF')
        self.onemogoceno = hex('#AAAAAA')

