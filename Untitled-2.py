#!/bin/env python3

import sys,time,re

class Pic(Accessoire):
    """ 
    Un pic contient les commandes Ã  fabriquer.
    Il peut embrocher un post-it contenant une commande 
    (une liste de consommations) par-dessus les post-it 
    dÃ©jÃ  prÃ©sents et libÃ©rer le dernier embrochÃ©. 
    """

    def embrocher(self,postit):
        self.append(postit)

    def liberer(self):
        if len(self)>0:
            postit = self.pop()
            return postit
        else:
            return None

class Bar(Accessoire):
    """ 
    Un bar peut recevoir des commandes (composÃ©es de consommations), 
    en attente d'Ãªtre servies (Ã©vacuÃ©es).
    """

    def recevoir(self,commande):
        ...

    def evacuer(self):
        ...

class Serveur(EmployÃ©):
    def __init__(self,pic,bar):
        super().__init__(pic,bar)

    def prendre_commande(self):
        while True:
            commande = input(f"{self.__class__.__name__}: prÃªt pour prendre une commande : ")
            if not commande:
                break
            print(f"{self.__class__.__name__}: j'ai la commande '{commande}'")
            commande = commande.split(",")
            print(f"{self.__class__.__name__}: j'Ã©cris sur le post-it '{commande}'")
            self.pic.embrocher(commande)

    def servir(self):
        while True:
                commande = self.bar.evacuer()
                if not commande:
                    break
                print(f"{self.__class__.__name__}: j'apporte la commande '{commande}'")
                
                for conso in commande:
                    print(f"{self.__class__.__name__}: je sers '{conso}'")

    def run(self):
        if self.step==0:
            self.step += 1
            self.prendre_commande()
        elif self.step==1:
            self.step += 1
            self.servir()

class Barman(EmployÃ©):
    def __init__(self,pic,bar):
        super().__init__(pic,bar)

    def preparer(self):
        while True:
            commande = self.pic.liberer()
            if not commande:
                break
            print(f"{self.__class__.__name__}: je commence la fabrication de '{commande}'")
            for conso in commande:
                print(f"{self.__class__.__name__}: je prÃ©pare '{conso}'")
            self.bar.recevoir(commande)
            print(f"{self.__class__.__name__}: la commande {commande} est prÃªte")

    def run(self):
        self.preparer()

def main():
    alice.run()
    bob.run()
    alice.run()

if __name__=="__main__":
  le_pic = Pic()
  le_bar = Bar()
  bob = Barman(le_pic,le_bar)
  alice = Serveur(le_pic,le_bar)
  main()