import sys,time,re

class Accessoire(list): # ici pas besoin d'implémenter append et pop car on hérite de la classe list qui a déjà ces méthodes

    def __init__ (self,liste=None):
        if liste is None:
            liste=[]
        super().__init__(liste)

# ou :

""" class Accessoire(): # ATTENTION ici problème avec len(self)
    def __init__ (self,liste=None):
        if liste is None:
            liste=[]
        self.commande = liste

    # nécessaire car on ne peut pas faire self.append ou .pop sur un objet, seulement sur une liste (on n'hérite pas de list ici)
    def append(self,element):
        return self.commande.append(element)
    
    def pop(self):
        return self.commande.pop() """

class Pic(Accessoire):
    """ 
    Un pic contient les commandes à  fabriquer.
    Il peut embrocher un post-it contenant une commande 
    (une liste de consommations) par-dessus les post-it 
    déjà  présents et libérer le dernier embroché. 
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
        self.append(commande)

    def evacuer(self):
        if len(self)>0:
            commande=self.pop()
            return commande
        else:
            return None

class Employé():
    def __init__(self,pic,bar):
        self.pic=pic
        self.bar=bar
        self.step=0 # pour le Serveur --> on commence par prendre la commande
        print("prêt pour le service")

class Clients:
    def __init__(self,fname):
        commandes = []

        start = time.time()
        fmt = re.compile(r"(\d+)\s+(.*)")
        with open(fname,"r") as f:
            for line in f:
                found = fmt.search(line)
                if found:
                    when = int(found.group(1))
                    what = found.group(2)
                    commandes.append((start+when,what.split(",")))
        self.commandes = commandes[::-1] # liste des commandes

    def commande(self):
            if len(self.commandes)>0:
              while True:
                if time.time()>self.commandes[-1][0]:
                    return self.commandes.pop()[1]
            else:
                return None

class Serveur(Employé):
    def __init__(self,pic,bar,clients):
        super().__init__(pic, bar)
        if isinstance(clients,Clients):
            self.clients=clients

    def prendre_commande(self):
        while True:
            print(f"{self.__class__.__name__}: prêt pour prendre une nouvelle commande ...")
            commande = self.clients.commande()
            if not commande:
                break
            print(f"{self.__class__.__name__}: j'ai la commande '{commande}'")
            # commande = commande.split(",") --> inutile car déjà une liste
            print(f"{self.__class__.__name__}: j'écris sur le post-it '{commande}'")
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

class Barman(Employé):
    def __init__(self,pic,bar,clients):
        super().__init__(pic,bar)
        if isinstance(clients,Clients):
            self.clients=clients

    def preparer(self):

        while True:
            commande = self.pic.liberer()
            if not commande:
                break
            print(f"{self.__class__.__name__}: je commence la fabrication de '{commande}'")
            for conso in commande:
                print(f"{self.__class__.__name__}: je prépare '{conso}'")
            self.bar.recevoir(commande)
            print(f"{self.__class__.__name__}: la commande {commande} est prête")

    def run(self):
        self.preparer()

def usage():
    print(f"usage: {sys.argv[0]} fichier")
    exit(1)
            

def main():
    alice.run()
    bob.run()
    alice.run()

if __name__=="__main__":
  if len(sys.argv)!=2:
    usage()
  fcommandes = sys.argv[1] # fichier des commandes

  le_pic = Pic()
  le_bar = Bar()
  les_clients = Clients(fcommandes)
  bob = Barman(le_pic,le_bar,les_clients)
  alice = Serveur(le_pic,le_bar,les_clients)
  main()