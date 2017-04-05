import random
import time
import threading

class Racunalnik():
    def __init__(self, callback, tezavnost):
        self.callback = callback
        self.tezavnost = tezavnost

    def zacni_potezo(self, igra):
        threading.Thread(target=self.izracunaj_potezo, args=(igra,)).start()

    def izracunaj_potezo(self, igra):
        time.sleep(2)
        p = random.choice(list(igra.mozne_poteze))
        self.callback(p)

    def prenehaj_razmisljat(self):
        pass

