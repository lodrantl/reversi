"""
.. module:: reversi.igra
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com, Lenart Treven <lenart.treven44@gmail.com>

Logika igre reversi

"""

import logging

logger = logging.getLogger('reversi_igra')
logger.setLevel(20)


class Stanje:
    """
    Stanje, ki ga bodo imeli žetoni na deski.
    """
    BELO = 'belo'
    CRNO = 'crno'
    PRAZNO = 'prazno'
    MOGOCE = 'mogoce'
    NEODLOCENO = 'neodloceno'

    @staticmethod
    def obrni(stanje):
        """
        Črno stanje spremeni v belo in obratno.
        :return: Novo stanje
        """
        if stanje == Stanje.BELO:
            return Stanje.CRNO
        elif stanje == Stanje.CRNO:
            return Stanje.BELO


SMERI = [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


class Igra:
    """
    Razred, katerega elemnti nosijo podatke o stanju igre, kot so število črnih in belih žetonov na polju,
    kdo je na potezi, kakšne so možne poteze, kako izgleda deska.
    """

    def __init__(self):
        """
        Naredi matriko, ki predstavlja desko, nanj na sredino postavi dva bela in črna žetona, preveri,
        katere so možne poteze.
        """
        self.koncana = False
        self.na_potezi = Stanje.CRNO
        self.stevilo_belih = self.stevilo_crnih = 2

        self.deska = [[Stanje.PRAZNO for _ in range(8)] for _ in range(8)]

        self.deska[3][3], self.deska[4][4] = Stanje.CRNO, Stanje.CRNO
        self.deska[3][4], self.deska[4][3] = Stanje.BELO, Stanje.BELO

        self.mozne_poteze = self.dobi_mozne_poteze()
        self.zgodovina = []

    def shrani_desko(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.deska[i][:] for i in range(8)]
        self.zgodovina.append((p, self.na_potezi))

    def razveljavi(self):
        deska, na_potezi = self.zgodovina.pop()
        self.deska = deska
        self.na_potezi = na_potezi
        self.mozne_poteze = self.dobi_mozne_poteze()

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        # Kopijo igre naredimo, ko poženemo na njej algoritem.
        # Če bi algoritem poganjali kar na glavni igri, ki jo
        # uporablja GUI, potem bi GUI mislil, da se menja stanje
        # igre (kdo je na potezi, kdo je zmagal) medtem, ko bi
        # algoritem vlekel poteze
        k = Igra()
        k.deska = [self.deska[i][:] for i in range(8)]
        k.mozne_poteze = k.dobi_mozne_poteze()
        k.na_potezi = self.na_potezi
        return k

    def dobi_mozne_poteze(self):
        """
        Preveri, katere so možne poteze, ki jih lahko igralec, ki je trenutno na vrsti izvede.
        :return: množica moožnih potez
        """
        mozne_poteze = set()
        for i in range(8):
            for j in range(8):
                if self._preveri_polje(i, j):
                    mozne_poteze.add((i, j))
        return mozne_poteze

    def _preveri_polje(self, x, y):
        """
        Za dano polje s koordinatami x in y preveri, če igralec, ki je na vrsti lahko igra na to polje.
        :param x: x koordinata polja
        :param y: y koordinata polja
        :return: True, če igralec lahko igra na to polje, False, sicer.
        """
        if self.deska[x][y] == Stanje.PRAZNO:
            for smer_x, smer_y in SMERI:
                zastavica = False
                i, j = x + smer_x, y + smer_y
                while 0 <= i <= 7 and 0 <= j <= 7:
                    if self.deska[i][j] == Stanje.PRAZNO:
                        break
                    if self.deska[i][j] == self.na_potezi and not zastavica:
                        break
                    if self.deska[i][j] == self.na_potezi and zastavica:
                        return True
                    i, j = i + smer_x, j + smer_y
                    zastavica = True
        return False

    def odigraj_potezo(self, koordinate):
        """
        Igralec igra potezo na koordinatah, žeton se tja postavi, če je možno, sicer ne. Žetoni na deski se obrnejo.
        Na vrsti je naslednji. Ko je konec igre, se vklopi stikalo na konec.
        :param koordinate: (x, y) koordinate, kjer bi igralec rad izvedel potezo.
        :return:
        """
        x, y = koordinate
        if (x, y) in self.mozne_poteze:
            self.deska[x][y] = self.na_potezi
            self.obrni_za(x, y)

            if self.na_potezi == Stanje.BELO:
                self.stevilo_belih += 1
                self.na_potezi = Stanje.CRNO
            elif self.na_potezi == Stanje.CRNO:
                self.stevilo_crnih += 1
                self.na_potezi = Stanje.BELO

            self.mozne_poteze = self.dobi_mozne_poteze()
            if len(self.mozne_poteze) == 0:
                logging.debug("Še enkrat na vrsti")
                self.na_potezi = Stanje.obrni(self.na_potezi)
                self.mozne_poteze = self.dobi_mozne_poteze()
                if len(self.mozne_poteze) == 0:
                    self.koncana = True
                    logging.debug("konec igre")
            logging.debug(self.mozne_poteze)
            self.shrani_desko()
        else:
            raise Exception("Polje {} ni na izbiro".format(koordinate))

    def obrni_za(self, x, y):
        """
        Za nov žeton na koordinatah x, y preveri v vse smeri, kateri žetoni so za obrnit in jih obrne.
        :param x: x koordinata novega žetona
        :param y: y koordinata novega žetona
        :return:
        """
        for smer_x, smer_y in SMERI:
            i, j = x + smer_x, y + smer_y
            trenutna_polja = []
            while 0 <= i <= 7 and 0 <= j <= 7:
                logging.debug((i, j))
                if self.deska[i][j] == Stanje.PRAZNO:
                    break
                if self.deska[i][j] == self.na_potezi:
                    self.obrni_zetone(trenutna_polja)
                    break
                trenutna_polja.append((i, j))
                i, j = i + smer_x, j + smer_y

    def obrni_zetone(self, seznam):
        """
        Žetonom v seznamu zamneja stanje iz belega v črno in obratno, ter poskrbi za štetje žetonov na deski ob obratih.
        :param seznam: Seznam žetonov, ki jih obrnemo
        :return:
        """
        for x, y in seznam:
            if self.deska[x][y] == Stanje.BELO:
                self.stevilo_belih -= 1
                self.stevilo_crnih += 1
                self.deska[x][y] = Stanje.CRNO
            elif self.deska[x][y] == Stanje.CRNO:
                self.stevilo_belih += 1
                self.stevilo_crnih -= 1
                self.deska[x][y] = Stanje.BELO
            else:
                raise Exception("Na plošči še ni žetona")

    def zmagovalec(self):
        if self.koncana:
            if self.stevilo_crnih == self.stevilo_crnih:
                return Stanje.NEODLOCENO
            return Stanje.BELO if self.stevilo_belih > self.stevilo_crnih else Stanje.CRNO
        else:
            return None
