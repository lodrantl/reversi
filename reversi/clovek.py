"""
.. module:: reversi.clovek
.. moduleauthor:: Luka Lodrant <luka.lodrant@gmail.com, Lenart Treven <lenart.treven44@gmail.com>

Interface človeškega igralca

"""

class Clovek:
    """
    Interface človeškega igralca
    """
    def __init__(self, callback):
        """
        :param callback: funkcija, ki se jo pokliče z izbrano potezo  
        """
        self.callback = callback

    def zacni_potezo(self, igra):
        # Sem človek zato ne naredim nič, ampak le čakam na klik
        pass

    def klik(self, koordinate):
        """
        Ob kliku na desko odigra potezo
        :param koordinate: koordinate klika
        """
        self.callback(koordinate)


