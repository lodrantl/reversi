class Stanje():
    BELO = 'belo'
    CRNO = 'crno'
    PRAZNO = 'prazno'
    MOGOCE = 'mogoce'

class Igra:
    deska = [[Stanje.PRAZNO for _ in range(8)] for _ in range(8)]
    na_potezi = Stanje.BELO
    mozne_poteze = set()
    stevilo_belih = 2
    stevilo_crnih = 2

    def __init__(self):
        self.deska[3][3] , self.deska[4][4] = Stanje.BELO, Stanje.BELO
        self.deska[3][4], self.deska[4][3] = Stanje.CRNO, Stanje.CRNO
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
            for smer_x, smer_y in [(1,0), (0,1), (0,-1), (-1,0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                zastavica = False
                i , j = x + smer_x, y + smer_y
                while 0 <= i <= 7 and 0<= j <= 7:
                    if self.deska[i][j] == Stanje.PRAZNO:
                        break
                    if self.deska[i][j] == self.na_potezi and not zastavica:
                        break
                    if self.deska[i][j] == self.na_potezi and zastavica:
                        return True
                    i  += smer_x
                    j += smer_y
                    zastavica = True
        return False


    def odigraj_potezo(self, koordinate):
        x, y = koordinate
        if (x, y) in self.mozne_poteze:
            self.deska[x][y] = self.na_potezi
            if self.na_potezi == Stanje.BELO:
                self.stevilo_belih += 1
                self.na_potezi = Stanje.CRNO
            elif self.na_potezi == Stanje.CRNO:
                self.stevilo_crnih += 1
                self.na_potezi = Stanje.BELO
            self.mozne_poteze = self.dobi_mozne_poteze()
        else:
            print("Polje ni na izbiro: ", koordinate)
            pass

    def obrni_zeton(self, x, y):
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





