"""
.. module:: reversi.minimax
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com>, Lenart Treven <lenart.treven44@gmail.com>

Algoritem Minimax z alfa-beta rezi

"""

import logging

from igra import Stanje


# Uteži uporabljene za ocenjevanje pozicije
UTEZI = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120]
]


class Minimax:
    """
    Minimax algoritem predstavljen kot objekt, uprablja igro opisano v igra.py,
    nima pa dostopa do GUI elementov, saj teče v svoji niti.
    """

    def __init__(self, globina, callback):
        """
        :param globina: globina do katere algoritem preiskuje drevo
        :param callback: funkcija, ki jo ob koncu pokliče z koordinatami izbrane poteze (npr. self.callback((1,2)))
                            funkcija naj sama poskrbi, da bo zagnana v pravi niti
        """
        self.globina = globina
        self.callback = callback

        self.prekinitev = False  # ali moramo končati?
        self.igra = None  # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)

    def prekini(self):
        """
        Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
        je uporabnik zaprl okno ali izbral novo igro.
        """
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """
        Izračunaj potezo za trenutno stanje dane igre.
        To metodo naj se pokliče v vzporednem vlaknu.
        :param igra: kopija trenutne igre kot objekt razreda Igra
        """
        self.igra = igra
        self.prekinitev = False  # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi

        # Poženemo minimax
        (poteza, vrednost) = self.alphabeta(self.globina, True)

        # Preverimo, da minimax in alfabeta vrneta enak rezultat
        # self.igra = i2
        # (poteza2, vrednost2) = self.minimax(self.globina, True)
        # assert poteza == poteza2, "{}, {}".format(poteza, poteza2)

        # Odstranimo trenutno stanje igre
        self.jaz = None
        self.igra = None

        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.callback(poteza)

    # Vrednosti igre
    ZMAGA = 100000  # Mora biti večje od najvišje vrednosti pozicije
    NESKONCNO = ZMAGA + 1  # Več kot zmaga

    def vrednost_pozicije(self):
        """
        Izračuna oceno trenutne pozicije z uporabo matrike uteži
        :return: ocena trenutne pozicije
        """
        nasprotnik = Stanje.obrni(self.jaz)
        vrednost = 0
        for i in range(8):
            for j in range(8):
                if self.igra.deska[i][j] == self.jaz:
                    vrednost += UTEZI[i][j]
                if self.igra.deska[i][j] == nasprotnik:
                    vrednost -= UTEZI[i][j]
        return vrednost

    def minimax(self, globina, maksimiziramo):
        """
        Glavna metoda minimax brez alfa beta rezov
        :param globina: globina do katere algoritem preiskuje drevo
        :param maksimiziramo: boolean: ali želimo vrednost maksimizirati ali minimizirati
        """
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        zmagovalec = self.igra.zmagovalec()
        if zmagovalec:
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == Stanje.obrni(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        else:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for p in self.igra.mozne_poteze():
                        self.igra.odigraj_potezo(p)
                        vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in self.igra.mozne_poteze():
                        self.igra.odigraj_potezo(p)
                        vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)

    def alphabeta(self, globina, maksimiziramo, alpha=-NESKONCNO, beta=NESKONCNO):
        """
        Glavna metoda minimax z alfa beta rezi
        :param globina: globina do katere algoritem preiskuje drevo
        :param maksimiziramo: boolean: ali želimo vrednost maksimizirati ali minimizirati
        :param alpha: največja najdena vrednost v drevesu na poti do izhodišča
        :param beta: najmanjša najdena vrednost v drevesu na poti do izhodišča
        """
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)

        zmagovalec = self.igra.zmagovalec()
        if zmagovalec:
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == Stanje.obrni(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        else:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Če trenutni igralec nima možne poteze zamenjamo igralca
                moznosti = self.igra.mozne_poteze()
                if len(moznosti) == 0:
                    return self.alphabeta(globina, not maksimiziramo, alpha, beta)

                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for p in moznosti:
                        self.igra.odigraj_potezo(p)
                        vrednost = self.alphabeta(globina - 1, not maksimiziramo, alpha, beta)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            alpha = max(alpha, vrednost)
                            najboljsa_poteza = p
                            if beta <= alpha:
                                break
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in moznosti:
                        self.igra.odigraj_potezo(p)
                        vrednost = self.alphabeta(globina - 1, not maksimiziramo, alpha, beta)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                            beta = min(beta, vrednost_najboljse)
                            if beta <= alpha:
                                break

                assert (najboljsa_poteza is not None), "AlphaBeta: izračunal None"
                return (najboljsa_poteza, vrednost_najboljse)
