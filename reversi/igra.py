"""
.. module:: reversi.igra
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com, Lenart Treven <lenart.treven44@gmail.com>

Logika igra reversi

"""


class Stanje():
    BELO = 'belo'
    CRNO = 'crno'
    PRAZNO = 'prazno'
    MOGOCE = 'mogoce'

    def obrni(stanje):
        if stanje == Stanje.BELO:
            return Stanje.CRNO
        elif stanje == Stanje.CRNO:
            return Stanje.BELO

SMERI = [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

class Igra:
    deska = [[Stanje.PRAZNO for _ in range(8)] for _ in range(8)]
    na_potezi = Stanje.CRNO
    mozne_poteze = set()
    stevilo_belih = 2
    stevilo_crnih = 2

    def __init__(self):
        self.deska[3][3], self.deska[4][4] = Stanje.CRNO, Stanje.CRNO
        self.deska[3][4], self.deska[4][3] = Stanje.BELO, Stanje.BELO
        self.mozne_poteze = self.dobi_mozne_poteze()

    def dobi_mozne_poteze(self):
        mozne_poteze = set()
        for i in range(8):
            for j in range(8):
                if self._preveri_polje(i, j):
                    mozne_poteze.add((i, j))
        return mozne_poteze



    def _preveri_polje(self, x, y):
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
                print("Še enkrat na vrsti")
                self.na_potezi = Stanje.obrni(self.na_potezi)
                self.mozne_poteze = self.dobi_mozne_poteze()
                if len(self.mozne_poteze) == 0:
                    print("konec igre")
            print(self.mozne_poteze)

        else:
            print("Polje ni na izbiro")
            pass

    def obrni_za(self, x, y):
        for smer_x, smer_y in SMERI:
            i, j = x + smer_x, y + smer_y
            trenutna_polja = []
            while 0 <= i and i <= 7 and 0 <= j and j <= 7:
                print((i, j))
                if self.deska[i][j] == Stanje.PRAZNO:
                    break
                if self.deska[i][j] == self.na_potezi:
                    self.obrni_zetone(trenutna_polja)
                    break
                trenutna_polja.append((i, j))
                i, j = i + smer_x, j + smer_y

    def obrni_zetone(self, seznam):
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