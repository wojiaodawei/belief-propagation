#!/usr/bin/python3
# -*- coding: utf-8 -*-

from NoeudPearl import *
from Pearl import *

v1 = NoeudPearl("V1", [True, False])
v2 = NoeudPearl("V2", [True, False])
v3 = NoeudPearl("V3", [True, False])
v4 = NoeudPearl("V4", [1, 2])
v5 = NoeudPearl("V5", [2, 4, 6])
v6 = NoeudPearl("V6", [1, 2, 3])

# Instance de E avec juste la feuille V5
E = {v5: 4} 
# ou instance de E avec V3 et V5
# E = {v3: False, v5: 4} 

v1.ajouterFils(v2)
v1.ajouterFils(v3)

v2.ajouterFils(v4)
v2.ajouterFils(v6)

v3.ajouterFils(v4)

v4.ajouterFils(v5)

table_proba_cond_V1 = {None: {True: 0.8, False: 0.2}}
v1.ajouterTableProbCond(table_proba_cond_V1)

table_proba_cond_V2 = {
    ((v1, True),): {True: 0.4, False: 0.6},
    ((v1, False),): {True: 0.9, False: 0.1}
}
v2.ajouterTableProbCond(table_proba_cond_V2)

table_proba_cond_V3 = {
    ((v1, True),): {True: 0.4, False: 0.6},
    ((v1, False),): {True: 0.7, False: 0.2}
}
v3.ajouterTableProbCond(table_proba_cond_V3)

table_proba_cond_V4 = {
    ((v2, True), (v3, True)): {1: 0.2, 2: 0.5},
    ((v2, True), (v3, False)): {1: 0.4, 2: 0.3},
    ((v2, False), (v3, True)): {1: 0.1, 2: 0.2},
    ((v2, False), (v3, False)): {1: 0.2, 2: 0.2}
}
v4.ajouterTableProbCond(table_proba_cond_V4)

table_proba_cond_V5 = {
    ((v4, 1),): {2: 0.3, 4: 0.6, 6: 0.9},
    ((v4, 2),): {2: 0.8, 4: 0.3, 6: 0.2}
}
v5.ajouterTableProbCond(table_proba_cond_V5)

table_proba_cond_V6 = {
    ((v2, True),): {1: 0.3, 2: 0.6, 3: 0.9},
    ((v2, False),): {1: 0.8, 2: 0.3, 3: 0.2}
}
v6.ajouterTableProbCond(table_proba_cond_V6)

liste_noeuds_G1 = [v1, v2, v3, v4, v5, v6]


PearlB = Pearl(liste_noeuds_G1, E)

PearlB.initialisation()
for v in liste_noeuds_G1:
    v.afficher()

input("Appuyez sur une touche de votre clavier pour lancer l'initialisation de la propagation...")

PearlB.initPropagation()
for v in liste_noeuds_G1:
    v.afficher()

input("Appuyez sur une touche de votre clavier pour lancer le reste de la propagation...")

PearlB.propagation()
for v in liste_noeuds_G1:
    v.afficher()
