import env

from reversi.igra import Igra
import random

def nakljucna_igra(n=15):
    """
    Zgenerira naključno pozicijo na deski po n potezah
    :param n: število potez
    :return: 
    """
    igra = Igra()

    for i in range(n):
        igra.odigraj_potezo(random.choice(list(igra.mozne_poteze())))
    return igra

def test_kopija():
    """
    Preveri ali igra.kopija() dejansko naredi novo kopijo igre
     """
    igra = nakljucna_igra()
    kopija = igra.kopija()
    assert igra.deska == kopija.deska
    assert igra.na_potezi == kopija.na_potezi
    igra.odigraj_potezo(random.choice(list(igra.mozne_poteze())))
    assert igra.deska != kopija.deska