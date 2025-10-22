import sys,time,re

class Logable: # étape 3    
    """
    Classe de base pour disposer d'une méthode log
    """

    def __init__(self,name,verbose):
        self.name = name
        self.verbose = verbose

    def log(self,msg):
        if self.verbose:
            print(f"[{self.name}] {msg}", file=logf, flush=True)


class Accessoire(list, Logable):
    def __init__ (self,name,verbose,liste=None):
        if liste is None:
            liste=[]
        list.__init__(liste)
        Logable.__init__(self,name,verbose)


class Pic(Accessoire):
    """ 
    Un pic contient les commandes à  fabriquer.
    Il peut embrocher un post-it contenant une commande 
    (une liste de consommations) par-dessus les post-it 
    déjà  présents et libérer le dernier embroché. 
    """

    def __init__(self,name,verbose):
        super().__init__(name=name,verbose=verbose)

    def embrocher(self,postit):
        self.log(f"post-it '{postit}' embrochée, {len(self)} post-it(s) à traiter")
        self.append(postit)

    def liberer(self):
        if len(self)>0:
            postit = self.pop()
            self.log(f"post-it '{postit}' libéré, {len(self)} post-it(s) à traiter")
            return postit
        else:
            return None


class Bar(Accessoire):
    """ 
    Un bar peut recevoir des commandes (composÃ©es de consommations), 
    en attente d'Ãªtre servies (Ã©vacuÃ©es).
    """

    def __init__(self,name,verbose):
        super().__init__(name=name,verbose=verbose)

    def recevoir(self,commande):
        self.log(f"'{commande}' posée, {len(self)} commande(s) à servir")
        self.append(commande)

    def evacuer(self):
        if len(self)>0:
            commande = self.pop()
            self.log(f"'{commande}' évacuée, {len(self)} commande(s) à servir")
            return commande
        else:
            return None


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
            

class Employé(Logable):
    def __init__(self,pic,bar,clients,name,verbose):
        Logable.__init__(self,name,verbose)
        self.pic=pic
        self.bar=bar
        self.clients=clients
        self.step=0
        self.log("prêt pour le service")


class Serveur(Employé):
    def __init__(self,pic,bar,clients,name,verbose):
        super().__init__(pic, bar,clients,name,verbose)

    def prendre_commande(self):
        while True:
            self.log(f"prêt pour prendre une nouvelle commande ...")
            commande = self.clients.commande()
            if not commande:
                break
            self.log(f"j'ai la commande '{commande}'")
            # commande = commande.split(",") --> inutile car déjà une liste
            self.log(f"j'écris sur le post-it '{commande}'")
            self.pic.embrocher(commande)

    def servir(self):
        while True:
                commande = self.bar.evacuer()
                if not commande:
                    break
                self.log(f"j'apporte la commande '{commande}'")
                
                for conso in commande:
                    self.log(f"je sers '{conso}'")

    def run(self):
        if self.step==0:
            self.step += 1
            self.prendre_commande()
        elif self.step==1:
            self.step += 1
            self.servir()


class Barman(Employé):
    def __init__(self,pic,bar,clients,name,verbose):
        super().__init__(pic,bar,clients,name,verbose)

    def preparer(self):

        while True:
            commande = self.pic.liberer()
            if not commande:
                break
            self.log(f"je commence la fabrication de '{commande}'")
            for conso in commande:
                self.log(f"je prépare {conso}")
            self.bar.recevoir(commande)
            self.log(f"la commande {commande} est prête")

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
  fcommandes = sys.argv[1]

  # étape 3
  logfile = "borabora.log"
  print(f"login in {logfile}...")
  logf = open(logfile,"w")
  print("\n---", file=logf, flush=True)

  les_clients = Clients(fcommandes)
  le_pic = Pic(name="le_pic", verbose=False)
  le_bar = Bar(name="le_bar", verbose=False)
  bob = Barman(le_pic, le_bar, les_clients, name="bob", verbose=True)
  alice = Serveur(le_pic, le_bar, les_clients, name="alice", verbose=False)

  main()