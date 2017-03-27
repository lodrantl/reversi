from enum import Enum

class Stanje():
    BELO = 'belo'
    CRNO = 'crno'
    PRAZNO = 'prazno'
    MOGOCE = 'mogoce'

class Igra:
    def __init__(self, poteza, deska):
        self.poteza = poteza
        self.deska = deska

    def mozne_poteze(self):
        return [(0,0)]
