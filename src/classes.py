#%%
#Differentes classes de proprietaires

#une personne simple
class Personne:
    """
    Cette classe représente une personne, ou un famille si membreFamille est non-nul

    Attributs :
    prenom1 (string) : le premier prenom
    prenom2 (string) : deuxième prénom si prénom composé
    nom1 (string) : premier nom de famille
    nom2 (string): second nom de famille éventuel
    membreFamille (string) : relation qui unie le groupe
    di (string) : mot qui vient aprés le "di"
    titre (string) : ce qui définit autre que les attributs précédents

    parcSeul (liste d'integer) : id des parcelles que la personne possède seul
    parcQuond (liste d'integer) : id des parcelles possédées et où le quondam est precisé
    parcFamille (liste d'integer) : id des parcelles possédées avec sa famille
    ParcAutres (liste d'integer) : id des parcelles possédée avec des inconnus

    isAQuondam (booléen) : si la personne est le 'quondam' et non le propriétaire
    isMorto (booléen) : si la personne est morte

    lien (liste de (Personne, String)) : les personnes avec qui elle a un lien et le nom du lien 
        (ex: (objet de 'GUERRA Stefano',fratello))
    """
    def __init__(self,nm1,pr1=None,pr2=None,nm2=None,di=None,mf=None,titre=None,
            ps=None,pq=None,pf=None,pa = None,pi=None,isqd=False, isMor=False):
        """
        Paramètres :
        nm1 (string) : premier nom de famille
        pr1 (string) : le premier prenom
        pr2 (string) : deuxième prénom si prénom composé
        nm2 (string): second nom de famille éventuel
        mf (string) : relation qui unie le groupe
        di (string) : mot qui vient aprés le "di"
        titre (string) : ce qui définit autre que les attributs précédents

        ps (liste d'integer) : id des parcelles que la personne possède seul
        pq (liste d'integer) : id des parcelles possédées et où le quondam est precisé
        pf (liste d'integer) : id des parcelles possédées avec sa famille
        pa (liste d'integer) : id des parcelles possédée avec des inconnus

        isqd (booléen) : si la personne est le 'quondam' et non le propriétaire
        isMor (booléen) : si la personne est morte

        """
        
        self.prenom1 = pr1
        self.prenom2 = pr2
        
        self.nom1 = nm1
        self.nom2 = nm2
        self.membreFamille = mf
        self.di = di
        self.titre = titre

        self.parcSeul = ps if ps is not None else []
        self.parcQuond = pq if pq is not None else []
        self.parcFamille = pf if pf is not None else []
        self.parcAutre = pa if pa is not None else []
        self.parIndivi = pi if pi is not None else []

        self.isQuondam = isqd
        self.isMorto = isMor
        self.lien = []

    def __str__(self):
        """
        affiche le nom et prénom de la personne
        """
        return 'Personne(nom: '+ self.nom1 + ', prenom: ' + self.prenom1+", parcelles: "+ \
            str(self.parcSeul+ self.parcQuond+ self.parcFamille+ self.parcAutre+ self.parIndivi)+")"
    def __repr__(self):
        return self.__str__()

class Parcelle:
    """
    Représente une parcelles ou une sous-parcelle
    
    Attributs : 
    number (int) : id de la parcelle ou sous-parcelle
    owner (Personne) : son/sa propriétaire 
    """
    def __init__(self,number, owner):
        """
        paramètres :
        number (int) : id de la parcelle ou sous-parcelle
        owner (Personne) : son/sa propriétaire
        """
        self.number = number
        self.owner = owner
    def __str__(self):
        return f"Parcelle({self.number}, owner={self.owner})"
    def __repr__(self):
        return self.__str__()



"""
classe pouvant être complétée dans un travail futur
""" 
class Chiesa:
    def __init__(self,nom,parcelles,entite=None):
        self.nom = nom
        self.parcelles = parcelles
        self.entite = entite
        self.lien = []

class Pretre:
    def __init__(self,nom,parcelles):
        self.nom = nom
        self.parcelles = parcelles
        self.lien = []

class Public:
    def __init__(self,nom,parcelles,prov=None):
        self.nom = nom
        self.parcelles = parcelles
        self.provenienza = prov


# %%
