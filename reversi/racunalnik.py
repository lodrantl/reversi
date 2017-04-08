import random
import time
import threading

from minimax import Minimax

class Racunalnik():
    def __init__(self, callback, tezavnost, barva):
        self.callback = callback
        self.tezavnost = tezavnost
        self.barva = barva

        self.minimax = Minimax(self.tezavnost + 2, self.callback)

    def zacni_potezo(self, igra):
        threading.Thread(target=self.izracunaj_potezo, args=(igra,)).start()

    def izracunaj_potezo(self, igra):
        if self.tezavnost == 0:
            time.sleep(0.3)
            poteza = random.choice(list(igra.mozne_poteze()))
            self.callback(poteza)
        else:
            self.minimax.izracunaj_potezo(igra.kopija())

    def prekini(self):
        if self.tezavnost > 0:
            self.minimax.prekini()