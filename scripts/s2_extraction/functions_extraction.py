#%%
import json
import re
import spacy



import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from data_filepaths import s2_setPrenoms
from data_filepaths import s2_setFamilles

import classes as c 
 
#from sys import from_sommarioni_to_countedTronqued
#from sys import from_countedTronqued_listByTypes



#%%
"""
les sets utilisés pour l'extraction
"""
with open(s2_setFamilles, encoding="utf-8") as f:
    setFamille = json.load(f)

with open(s2_setPrenoms,encoding="utf-8") as f:
    setPrenoms = json.load(f)

listDeTitre = ['commisaria','sacerdote','primo','secondo']
setTitre = sorted(set(listDeTitre))

listDeMembre = ['fratelli','fratello','nipote','nipoti','sorelle','sorella','eredi','consorti','vedova','famiglia','figlio','figli','fillio','compagni','conorti']
setMembre = sorted(set(listDeMembre))

listFaconDecrireQuondam = ['quondam','q.','q.m.','q.m']
setQuondam = sorted(set(listFaconDecrireQuondam))

"""
Set des inclassable, pas encore utilisé mais peut servir à l'avenir
"""
setSpecial = [['cimiterio'],['sottoportico', 'pubblico', "dell'angelo"],
    ['scola', 'maggiore'],['scola', 'maggior'],['compagnia', 'dei', 'mercanti'],
    ['possessori', 'ignoti'],['scuola', 'italiana'],['scuola', 'mensulamin'],
    ['patriarcato', 'di', 'venezia'],['reale', 'corrona'],['corona', 'reale'],
    ['proprietario', 'ignotto'], ['possessore', 'ignotto']]


#%%
def decoupe_corresp(tableau, taille, decoupe):
    """
    Vérifie si une entrée correspond à un format de taille i
    
    paramètres :
        tableau (liste de sets) : les sets auquels doivent appartenir les mots de l'entrée pour correspondre au format
        taille : taille de la liste à comparer
        decoupe : l'entrée découpée en mots

    retourne : True si l'entrée correspond au format 
    
    """

    for i in range(taille):
        if decoupe[i] not in tableau[i]:
            return False
    return True

# %%
def ajouterLien(persA, persB, typeDeLien):
    """
    Ajoute un lieu entre deux personnes

    paramètre :
        persA (Personne) : une personne auquel on ajoute le lien
        persB (Personne) : l'autre personne auquel on ajoute le lien
        typeDeLien (String) : Le lien qu'on veut ajouter

    Ne retourne rien
    """
    persA.lien.append((persB, typeDeLien))
    persB.lien.append((persA, typeDeLien))


#%%
#gestion des nom seul
#nomSeultemp = listByType_plusNumber[0][1]


def gestion_nom_seul(nomSeul, aff_result=False):
    """
    Reconnait des formats dans la liste des noms Seuls et crée des personnes le cas échéant, ainsi que les parcelles correspondantes,
        crée aussi les liens entre personnes et entre les propriétaires et leurs parcelles  
    
    paramètres :
        nomSeul ( [list de String, liste de liste d'integer] ) : la liste des entrées appartenant à la catégorie nomSeul,
            chacune associée aux parcelles qu'elle possède (se situent au même index dans les deux listes principales)
        aff_result (booléen) : si True, les statistiques d'extraction sont affichées

    Retourne :
        listdePersonne (liste de Personne) : les personne créées 
        listdeParcelle (list de Parcelles): les parcelles classées (donc créées en tant qu'objet)  
        pasEncoreClasse ( [list de String, liste de liste d'integer] ) : les propriétaires pas encore identifiés et leurs parcelles
    """
    listdePersonne = []
    listdeParcelle = []

    pasEncoreClasse = []
    nbParcNonClass = 0

    #parcours tous les noms seul
    for i in range(len(nomSeul)):
        a=0
    for i in range(len(nomSeul)):
        decoupe = re.split("\s",nomSeul[i][0].lower())
        #print(decoupe)
        taille = len(decoupe)
        parcelles = nomSeul[i][1]
        if (decoupe[taille-1] == ''):
            decoupe.pop()
            taille -= 1
        if taille == 1:
            #nom de famille
            if decoupe[0] in setFamille:
                personne = c.Personne(decoupe[0], ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne)) 
            else : 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 2 :
            #nom-prenom
            if decoupe_corresp([setFamille,setPrenoms], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-membre
            elif decoupe_corresp([setFamille,setMembre], taille, decoupe):
                personne = c.Personne(decoupe[0],mf=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-titre
            elif decoupe_corresp([setFamille,setTitre], taille, decoupe):
                personne = c.Personne(decoupe[0],titre=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-nom
            elif decoupe_corresp([setFamille,setFamille], taille, decoupe):
                personne = c.Personne(decoupe[0],nm2=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            else :
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 3:
            #nom-prenom-prenom
            if decoupe_corresp([setFamille,setPrenoms,setPrenoms], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[1],decoupe[2],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-nom-prenom
            elif decoupe_corresp([setFamille,setFamille,setPrenoms], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[2],nm2=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-prenom-membre
            elif decoupe_corresp([setFamille,setPrenoms,setMembre], taille, decoupe):
                personne = c.Personne(decoupe[0],nm2=decoupe[1],mf=decoupe[2],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-membre-quondam
            elif decoupe_corresp([setFamille,setPrenoms,setQuondam], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-membre-indivisi
            elif decoupe_corresp([setFamille,setMembre,['indivisi','indivise']], taille, decoupe):
                personne = c.Personne(decoupe[0],mf=decoupe[1],ps=parcelles,pi=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-nom-indivisi
            elif decoupe_corresp([setFamille,setFamille,['indivisi','indivise']], taille, decoupe):
                personne = c.Personne(decoupe[0],nm2=decoupe[1],ps=parcelles,pi=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))        
            #nom-titre-prenom
            elif decoupe_corresp([setFamille,setTitre,setPrenoms], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[2],titre=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-prenom-titre
            elif decoupe_corresp([setFamille,setPrenoms,setTitre], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[1],titre=decoupe[2],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))  
            else:
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 4:
            #Nom-membre(lien)-di-prenom
            if (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di") & (decoupe[3] in setPrenoms):
                personne = c.Personne(decoupe[0],decoupe[3],mf=decoupe[1],pq=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-prenom-di-...
            elif (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) &(decoupe[2] == "di"):
                personne = c.Personne(decoupe[0],decoupe[1],di=decoupe[3],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-membre(lien)-di-...
            elif (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di"):
                personne = c.Personne(decoupe[0],mf=decoupe[1],di=decoupe[3],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            else:
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        else:
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    if aff_result:
        print('personnes créées ',len(listdePersonne))
        print('non classées ',len(pasEncoreClasse))
        print('total ',len(nomSeul))
        print('parcelles classée ',len(listdeParcelle))
        print('parcelles non classé ',nbParcNonClass)

    return listdePersonne, listdeParcelle, pasEncoreClasse 

#%%
#gestion des nom avec quondam
def gestion_avec_quondam(nomAvecQuondam, aff_result=False):
    """
    Reconnait des formats dans la liste des noms avec quondam et crée des personnes le cas échéant, ainsi que les parcelles correspondantes,
        crée aussi les liens entre personnes et entre les propriétaires et leurs parcelles  
    
    paramètres :
        nomSeul ( [list de String, liste de liste d'integer] ) : la liste des entrées appartenant à la catégorie nomEtQuondam,
            chacune associée aux parcelles qu'elle possède (se situent au même index dans les deux listes principales)
        aff_result (booléen) : si True, les statistiques d'extraction sont affichées

    Retourne :
        listdePersonne (liste de Personne) : les personne créées 
        listdeParcelle (list de Parcelles): les parcelles classées (donc créées en tant qu'objet)  
        pasEncoreClasse ( [list de String, liste de liste d'integer] ) : les propriétaires pas encore identifiés et leurs parcelles
    """

    listdePersonne = []
    listdeParcelle = []
    pasEncoreClasse = []
    nbParcNonClass = 0

    #parcours tout les noms avec quondam
    for i in range(len(nomAvecQuondam)):
        decoupe = re.split("\s",nomAvecQuondam[i][0].lower())
        taille = len(decoupe)
        parcelles = nomAvecQuondam[i][1]
        if re.search('^\.+$',decoupe[taille-1]) is not None:
            taille -= 1
        #si termine par quondam, meme cas que nom seul
        if (decoupe[taille-1]in setQuondam):
            taille -= 1
            if taille == 1:
                #nom de famille
                if decoupe[0] in setFamille:
                    personne = c.Personne(decoupe[0], ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne)) 
                else : 
                    pasEncoreClasse.append(decoupe)
                    nbParcNonClass += len(parcelles)
            elif taille == 2 :
                #nom-prenom
                if decoupe_corresp([setFamille,setPrenoms], taille, decoupe):
                    personne = c.Personne(decoupe[0],decoupe[1],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                #nom-membre
                elif decoupe_corresp([setFamille,setMembre], taille, decoupe):
                    personne = c.Personne(decoupe[0],mf=decoupe[1],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                else :
                    pasEncoreClasse.append(decoupe)
                    nbParcNonClass += len(parcelles)
            elif taille == 3:
                #nom-prenom-prenom
                if decoupe_corresp([setFamille,setPrenoms,setPrenoms], taille, decoupe):
                    personne = c.Personne(decoupe[0],decoupe[1],decoupe[2],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                #nom-nom-prenom
                elif decoupe_corresp([setFamille,setFamille,setPrenoms], taille, decoupe):
                    personne = c.Personne(decoupe[0],decoupe[2],nm2=decoupe[1],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                #nom-prenom-membre
                elif decoupe_corresp([setFamille,setPrenoms,setMembre], taille, decoupe):
                    personne = c.Personne(decoupe[0],nm2=decoupe[1],mf=decoupe[2],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                #nom-titre-prenom
                elif decoupe_corresp([setFamille,setTitre,setPrenoms], taille, decoupe):
                    personne = c.Personne(decoupe[0],decoupe[2],titre=decoupe[1],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                #nom-prenom-titre
                elif decoupe_corresp([setFamille,setPrenoms,setTitre], taille, decoupe):
                    personne = c.Personne(decoupe[0],decoupe[1],titre=decoupe[2],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))  
                else:
                    pasEncoreClasse.append(decoupe)
                    nbParcNonClass += len(parcelles)
            elif taille == 4:
                #Nom-membre(lien)-di-prenom
                if (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di") & (decoupe[3] in setPrenoms):
                    personne = c.Personne(decoupe[0],decoupe[3],mf=decoupe[1],pq=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                #nom-prenom-di-...
                elif (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) &(decoupe[2] == "di"):
                    personne = c.Personne(decoupe[0],decoupe[1],di=decoupe[3],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                #nom-membre(lien)-di-...
                elif (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di"):
                    personne = c.Personne(decoupe[0],mf=decoupe[1],di=decoupe[3],ps=parcelles)
                    listdePersonne.append(personne)
                    for par in parcelles:
                        listdeParcelle.append(c.Parcelle(par, personne))
                else :
                    pasEncoreClasse.append(decoupe)
                    nbParcNonClass += len(parcelles)
        elif taille == 4:
            #nom-prenom-quondam-prenom
            if decoupe_corresp([setFamille,setPrenoms,setQuondam, setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')
            #nom-membre(lien)-quondam-prenom
            elif decoupe_corresp([setFamille,setMembre,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],mf=decoupe[1],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')
            #nom-prenom-vedova-nom
            elif decoupe_corresp([setFamille,setPrenoms,['vedova'],setFamille], taille, decoupe):
                personneA = c.Personne(decoupe[0],pr1=decoupe[1],pq=parcelles)
                personneB = c.Personne(decoupe[3],isMor=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'vedova')
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 5:
            #nom-prenom-prenom-quondam-prenom
            if decoupe_corresp([setFamille,setPrenoms,setPrenoms,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pr2=decoupe[2],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[4],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')
            #nom-nom-prenom-quondam-prenom
            elif decoupe_corresp([setFamille,setFamille,setPrenoms,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],nm2=decoupe[1],pr1=decoupe[2],pq=parcelles)
                personneB = c.Personne(decoupe[0],nm2=decoupe[1],pr1=decoupe[4],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')
            #nom-titre-prenom-quondam-prenom
            elif decoupe_corresp([setFamille,setTitre,setPrenoms,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],titre=decoupe[1],pr1=decoupe[2],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[4],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')
            #nom-prenom-quondam-prenom-prenom
            elif decoupe_corresp([setFamille,setPrenoms,setQuondam,setPrenoms,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],decoupe[4],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')
            #nom-membre(lien)-quondam-prenom-prenom
            elif decoupe_corresp([setFamille,setMembre,setQuondam,setPrenoms,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],mf=decoupe[1],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],pr2=decoupe[4],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')  
            #nom-prenom-membre(lien)-quondam-prenom
            elif decoupe_corresp([setFamille,setPrenoms,setMembre,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],pr1=decoupe[1],mf=decoupe[2],pq=parcelles)
                personneB = c.Personne(decoupe[0],pr1=decoupe[4],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam') 
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille ==6:
            #nom-prenom-prenom-quondam-prenom-prenom
            if decoupe_corresp([setFamille,setPrenoms,setPrenoms,setQuondam,setPrenoms,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pr2=decoupe[2],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[4],pr2=decoupe[5],isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personneA))
                ajouterLien(personneA,personneB,'quondam')
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        else : 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)

    if aff_result:
        print('personnes créées ',len(listdePersonne))
        print('non classées ',len(pasEncoreClasse))
        print('total ',len(nomAvecQuondam))
        print('parcelles classée ',len(listdeParcelle))
        print('parcelles non classé ',nbParcNonClass)

    return listdePersonne, listdeParcelle, pasEncoreClasse

#%%
#gestion des nom avec membre de la famille
def gestion_avec_famille(nomAvecFamille, aff_result=False):
    """
    Reconnait des formats dans la liste des noms avec famille et crée des personnes le cas échéant, ainsi que les parcelles correspondantes,
        crée aussi les liens entre personnes et entre les propriétaires et leurs parcelles  
    
    paramètres :
        nomSeul ( [list de String, liste de liste d'integer] ) : la liste des entrées appartenant à la catégorie nomAvecFamille,
            chacune associée aux parcelles qu'elle possède (se situent au même index dans les deux listes principales)
        aff_result (booléen) : si True, les statistiques d'extraction sont affichées

    Retourne :
        listdePersonne (liste de Personne) : les personne créées 
        listdeParcelle (list de Parcelles): les parcelles classées (donc créées en tant qu'objet)  
        pasEncoreClasse ( [list de String, liste de liste d'integer] ) : les propriétaires pas encore identifiés et leurs parcelles
    """

    listdePersonne = []
    listdeParcelle = []
    pasEncoreClasse = []
    nbParcNonClass = 0

    #parcours tous les noms avec famille
    for i in range(len(nomAvecFamille)):
        decoupe = re.split("\s",nomAvecFamille[i][0].lower())
        taille = len(decoupe)
        parcelles= nomAvecFamille[i][1]
        if taille == 4:
            #nom-prenom-e-membre(lien)
            if decoupe_corresp([setFamille,setPrenoms,['e','ed'],setMembre], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[1],mf=decoupe[3],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-prenom-e-prenom
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms], taille, decoupe):
                personneA= c.Personne(decoupe[0],decoupe[1],pf=parcelles)
                personneB= c.Personne(decoupe[0],decoupe[3],pf=parcelles)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, [personneA,personneB]))
                ajouterLien(personneA,personneB,'fratello')
            #nom-e-membre-indivisi
            elif decoupe_corresp([setFamille,['e','ed'],setMembre,['indivisi','indivise']],taille, decoupe):
                personne = c.Personne(decoupe[0],mf=decoupe[2],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)   
        elif taille == 5:
            #nom-prenom-e-prenom-membre
            if decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,setMembre], taille, decoupe):
                personneA= c.Personne(decoupe[0],decoupe[1],pf=parcelles)
                personneB= c.Personne(decoupe[0],decoupe[3],pf=parcelles)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, [personneA,personneB]))
                ajouterLien(personneA,personneB,decoupe[4])
            #nom-prenom-e-membre(lien)-indivisi
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setMembre,['indivisi','indivise']], taille, decoupe):
                personne = c.Personne(decoupe[0],decoupe[1],mf=decoupe[3],ps=parcelles, pi=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            #nom-prenom-e-prenom-indivisi
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,['indivisi','indivise']], taille, decoupe):
                personneA= c.Personne(decoupe[0],decoupe[1],pf=parcelles,pi=parcelles)
                personneB= c.Personne(decoupe[0],decoupe[3],pf=parcelles,pi=parcelles)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, [personneA,personneB]))
                ajouterLien(personneA,personneB,'fratello')
            #nom-prenom-prenom-e(d)-prenom
            elif decoupe_corresp([setFamille,setPrenoms,setPrenoms,['e','ed'],setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],pr1=decoupe[1],pr2=decoupe[2],pf=parcelles)
                personneB = c.Personne(decoupe[0],pr1=decoupe[4],pf=parcelles)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, [personneA,personneB]))
                ajouterLien(personneA,personneB,'fratello')
            #nom-prenom-prenom-e(d)-membre
            elif decoupe_corresp([setFamille,setPrenoms,setPrenoms,['e','ed'],setMembre],taille,decoupe):
                personne = c.Personne(decoupe[0],decoupe[1],pr2=decoupe[2],mf=decoupe[4],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 6:
            #nom-prenom-e-membre(lien)-quondam-prenom
            if decoupe_corresp([setFamille,setPrenoms,['e','ed'],setMembre,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],mf=decoupe[3],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[5], isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,'quondam')
            #nom-prenom-e-prenom-quondam-prenom
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles)
                personneC = c.Personne(decoupe[0],decoupe[5],isqd=True)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,'fratello')
                ajouterLien(personneA,personneC,'quondam')
                ajouterLien(personneB,personneC,'quondam')
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                listdePersonne.append(personneC)
            #nom-prenom-e-prenom-membre(lien)-indivisi
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,setMembre,['indivisi','indivise']], taille, decoupe):
                personneA= c.Personne(decoupe[0],decoupe[1],pf=parcelles,pi=parcelles)
                personneB= c.Personne(decoupe[0],decoupe[3],pf=parcelles,pi=parcelles)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, [personneA,personneB]))
                ajouterLien(personneA,personneB,decoupe[4])
            #nom-prenom-prenom-e-prenom-indivisi
            elif decoupe_corresp([setFamille,setPrenoms,setPrenoms,['e','ed'],setPrenoms,['indivisi','indivise']],taille, decoupe):
                personneA= c.Personne(decoupe[0],decoupe[1],pr2=decoupe[2],pf=parcelles, pi=parcelles)
                personneB= c.Personne(decoupe[0],decoupe[4],pf=parcelles, pi=parcelles)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, [personneA,personneB]))
                ajouterLien(personneA,personneB,'fratello')
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 7:
            #nom-prenom-e-prenom-membre(lien)-quondam-prenom
            if decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,setMembre,setQuondam,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles)
                personneC = c.Personne(decoupe[0],decoupe[6],isqd=True)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,decoupe[4])
                ajouterLien(personneA,personneC,'quondam')
                ajouterLien(personneB,personneC,'quondam')
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                listdePersonne.append(personneC)
            #nom-prenom-e-membre(lien)-quondam-prenom-prenom
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setMembre,setQuondam,setPrenoms,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],mf=decoupe[3],pq=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[5],pr2=decoupe[6], isqd=True)
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,'quondam')
            #nom-prenom-prenom-e(d)-membre-quondam-prenom
            elif decoupe_corresp([setFamille,setPrenoms,setPrenoms,['e','ed'],setMembre,setQuondam,setPrenoms],taille,decoupe):
                personneA= c.Personne(decoupe[0],decoupe[1],pr2=decoupe[2],mf=decoupe[4],pq=parcelles)
                personneB= c.Personne(decoupe[0],decoupe[6],isqd=True)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,'quondam')
            #nom-prenom-e-prenom-quondam-prenom-prenom
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,setQuondam,setPrenoms,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles)
                personneC = c.Personne(decoupe[0],decoupe[5],pr2=decoupe[6],isqd=True)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,'fratello')
                ajouterLien(personneA,personneC,'quondam')
                ajouterLien(personneB,personneC,'quondam')
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                listdePersonne.append(personneC)
            #nom-prenom-e-prenom-quondam-prenom-indivisi
            elif decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,setQuondam,setPrenoms,['indivisi','indivise']], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles,pi=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles,pi=parcelles)
                personneC = c.Personne(decoupe[0],decoupe[5],isqd=True)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,'fratello')
                ajouterLien(personneA,personneC,'quondam')
                ajouterLien(personneB,personneC,'quondam')
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                listdePersonne.append(personneC)
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 8:
            #nom-prenom-e-prenom-membre(lien)-quondam-prenom-prenom
            if decoupe_corresp([setFamille,setPrenoms,['e','ed'],setPrenoms,setMembre,setQuondam,setPrenoms,setPrenoms], taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles)
                personneC = c.Personne(decoupe[0],decoupe[6],pr2=decoupe[7],isqd=True)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,decoupe[4])
                ajouterLien(personneA,personneC,'quondam')
                ajouterLien(personneB,personneC,'quondam')
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                listdePersonne.append(personneC)
            #nom-prenom-prenom-e-prenom-membre(lien)-quondam-prenom
            elif decoupe_corresp([setFamille,setPrenoms,setPrenoms,['e','ed'],setPrenoms,setMembre,setQuondam,setPrenoms],taille, decoupe):
                personneA = c.Personne(decoupe[0],decoupe[1],pr2=decoupe[2],pq=parcelles,pf=parcelles)
                personneB = c.Personne(decoupe[0],decoupe[4],pq=parcelles,pf=parcelles)
                personneC = c.Personne(decoupe[0],decoupe[7],isqd=True)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, personne))
                ajouterLien(personneA,personneB,decoupe[5])
                ajouterLien(personneA,personneC,'quondam')
                ajouterLien(personneB,personneC,'quondam')
                listdePersonne.append(personneA)
                listdePersonne.append(personneB)
                listdePersonne.append(personneC)
            else:
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        else:
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)

    if aff_result:
        print('personnes créées ',len(listdePersonne))
        print('non classées ',len(pasEncoreClasse))
        print('total ',len(nomAvecFamille))
        print('parcelles classée ',len(listdeParcelle))
        print('parcelles non classé ',nbParcNonClass)

    return listdePersonne, listdeParcelle, pasEncoreClasse


# %%
"""
Les fonctions suivantes sont des ébauches de gestion des catégories Venezia et Demanio
"""


def gestion_venezia(nomVenezia, aff_result=False):
    listPublic = []
    listdeParcelle = []
    pasEncoreClasse = []
    pasEncoreClasseParcelle = []
    nbParcNonClass = 0

    #parcours tous les nom avec venezia
    for i in range(len(nomVenezia)):
        decoupe = re.split("\s",nomVenezia[i][0].lower())
        taille = len(decoupe)
        parcelles= nomVenezia[i][1]
        if taille == 3:
            if (decoupe[2] == 'venezia'):
                public = c.Public(decoupe[0],parcelles)
                listPublic.append(public)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, public))
            else: 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        else :  
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    if aff_result:
        print('personnes créées ',len(listPublic))
        print('non classées ',len(pasEncoreClasse))
        print('total ',len(nomVenezia))
        print('parcelles classée ',len(listdeParcelle))
        print('parcelles non classé ',nbParcNonClass)

    return listPublic, listdeParcelle, pasEncoreClasse


#%%
def gestion_demanio(nomDemanio, aff_result=False):
    listPublic = []
    listdeParcelle = []
    pasEncoreClasse = []
    nbParcNonClass = 0

    for i in range(len(nomDemanio)):
        decoupe = re.split("\s",nomDemanio[i][0].lower())
        taille = len(decoupe)
        parcelles= nomDemanio[i][1]
        if taille==2:
            if (decoupe[1] == 'demanio'):
                public = c.Public(decoupe[1],parcelles)
                listPublic.append(public)
                for par in parcelles:
                    listdeParcelle.append(c.Parcelle(par, public))
        else :  
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    if aff_result:
        print('personnes créées ',len(listPublic))
        print('non classées ',len(pasEncoreClasse))
        print('total ',len(nomDemanio))
        print('parcelles classée ',len(listdeParcelle))
        print('parcelles non classé ',nbParcNonClass)

    return listPublic, listdeParcelle, pasEncoreClasse

# %%
