import random
import time
import threading

from reversi.minimax import Minimax

class Racunalnik():
    def __init__(self, callback, tezavnost, barva):
        self.callback = callback
        self.tezavnost = tezavnost
        self.barva = barva

        if self.tezavnost > 0:
            self.minimax = Minimax(self.tezavnost * 3, self.callback)

    def zacni_potezo(self, igra):
        if self.tezavnost == 0:
            time.sleep(0.3)
            poteza = random.choice(list(igra.mozne_poteze))
            self.callback(poteza)
        else:
            threading.Thread(target=self.minimax.izracunaj_potezo, args=(igra,)).start()