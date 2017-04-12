"""
.. module:: reversi.racunalnik
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com, Lenart Treven <lenart.treven44@gmail.com>

Interface racunalniskega igralca

"""

import random
import time
import threading

from minimax import Minimax


class Racunalnik:
    """
    Interface racunalniskega igralca
    """

    def __init__(self, callback, tezavnost=1):
        """
        :param callback: funkcija, ki se jo pokliče z izbrano potezo
        :param tezavnost: težavnost računalnika (globina MiniMaxa) med 0 in 2
        """
        self.callback = callback
        self.tezavnost = tezavnost

        if self.tezavnost > 0:
            self.minimax = Minimax(self.tezavnost + 2, self.callback)

    def zacni_potezo(self, igra):
        """
        V novi niti izračuna potezo
        :param igra: trenutna verzija igre
        """
        threading.Thread(target=self.izracunaj_potezo, args=(igra,)).start()

    def izracunaj_potezo(self, igra):
        """
        Pri težavnosti 0 vrne naključno potezo, sicer uporabi MiniMax 
        :param igra: trenutna verzija igre 
        """
        if self.tezavnost == 0:
            time.sleep(0.3)
            poteza = random.choice(list(igra.mozne_poteze()))
            self.callback(poteza)
        else:
            self.minimax.izracunaj_potezo(igra.kopija())

    def prekini(self):
        """
        Prekine minimax 
        """
        if self.tezavnost > 0:
            self.minimax.prekini()

    def klik(self, koordinate):
        # Ne naredim nič saj sem računalnik
        pass
