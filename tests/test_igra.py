from reversi import Igra
import random

def test_kopija():
    igra = Igra()

    for i in range(10):
        igra.odigraj_potezo(random.choice(igra.mozne_poteze))

    assert igra.mozne_poteze == igra.kopija().mozne_poteze
    assert igra.deska == igra.kopija().deska