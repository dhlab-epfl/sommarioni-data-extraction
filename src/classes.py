#%%
#Differentes classes de proprietaires

#une personne simple
class Personne:
    def __init__(self,nm1,pr1=None,pr2=None,nm2=None,di=None,mf=None,titre=None,
            ps=None,pq=None,pf=None,pa = None,pi=None,isqd=False):
        self.prenom1 = pr1
        self.prenom2 = pr2
        
        self.nom1 = nm1
        self.nom2 = nm2
        self.membreFamille = mf
        self.di = di
        self.titre = titre

        self.parcSeul = ps
        self.parcQuond = pq
        self.parcFamille = pf
        self.parcAutre = pa
        self.parIndivi = pi

        self.isAquondam = isqd
        self.lien = []

    def __eq__(self, other):
        self.prenom1 == other.prenom1
        self.prenom2 == other.prenom2
        self.nom1 == other.nom1
        self.nom2 == other.nom2
        self.di == other.di
        self.isAquondam == other.isAquondam

    def __str__(self):
        return 'Nom : ' + self.nom1 + ' Prenom : ' + self.prenom1

    def get_all_parcelles():
        pass

#eglise 
class Chiesa:
    def __init__(self,nom,parcelles,entite=None):
        self.nom = nom
        self.parcelles = parcelles
        self.entite = entite
        self.lien = []

#pretre qui a un benefizio/goduto
class Pretre:
    def __init__(self,nom,parcelles):
        self.nom = nom
        self.parcelles = parcelles
        self.lien = []

class Public:
    def __init__(self,nom,parcelles):
        self.nom = nom
        self.parcelles = parcelles

class Parcelle:
    def __init__(self,number, owner):
        self.number = number
        self.owner = owner
# %%
