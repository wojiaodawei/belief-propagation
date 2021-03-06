#!/usr/bin/python3
# -*- coding: utf-8 -*-

from NoeudPearl import *
from Pearl import *

A = NoeudPearl("A", ["a1", "a2"])
B = NoeudPearl("B", ["b1", "b2"])
C = NoeudPearl("C", ["c1", "c2"])
D = NoeudPearl("D", ["d1", "d2"])
E = NoeudPearl("E", ["e1", "e2"])
F = NoeudPearl("F", ["f1", "f2"])
G = NoeudPearl("G", ["g1", "g2"])
H = NoeudPearl("H", ["h1", "h2"])
I = NoeudPearl("I", ["i1", "i2"])

A.ajouterFils(B)
A.ajouterFils(C)

B.ajouterFils(D)
B.ajouterFils(E)

C.ajouterFils(F)
C.ajouterFils(G)

F.ajouterFils(H)
F.ajouterFils(I)

tpc_A = {None: {"a1": 0.4, "a2": 0.6}}
A.ajouterTableProbCond(tpc_A)

tpc_B = {
    ((A, "a1"),): {"b1": 0.2, "b2": 0.8},
    ((A, "a2"),): {"b1": 0.3, "b2": 0.7}}
B.ajouterTableProbCond(tpc_B)

tpc_D = {
    ((B, "b1"),): {"d1": 0.5, "d2": 0.5},
    ((B, "b2"),): {"d1": 0.35, "d2": 0.65}}
D.ajouterTableProbCond(tpc_D)

tpc_E = {
    ((B, "b1"),): {"e1": 0.15, "e2": 0.85},
    ((B, "b2"),): {"e1": 0.45, "e2": 0.55}}
E.ajouterTableProbCond(tpc_E)

tpc_C = {
    ((A, "a1"),): {"c1": 0.1, "c2": 0.9},
    ((A, "a2"),): {"c1": 0.25, "c2": 0.75}}
C.ajouterTableProbCond(tpc_C)

tpc_G = {
    ((C, "c1"),): {"g1": 0.25, "g2": 0.75},
    ((C, "c2"),): {"g1": 0.1, "g2": 0.9}}
G.ajouterTableProbCond(tpc_G)

tpc_F = {
    ((C, "c1"),): {"f1": 0.3, "f2": 0.7},
    ((C, "c2"),): {"f1": 0.6, "f2": 0.4}}
F.ajouterTableProbCond(tpc_F)

tpc_H = {
    ((F, "f1"),): {"h1": 0.65, "h2": 0.35},
    ((F, "f2"),): {"h1": 0.2, "h2": 0.8}}
H.ajouterTableProbCond(tpc_H)

tpc_I = {
    ((F, "f1"),): {"i1": 0.25, "i2": 0.75},
    ((F, "f2"),): {"i1": 0.5, "i2": 0.5}}
I.ajouterTableProbCond(tpc_I)

liste_noeuds_G1 = [A, B, C, D, E, F, G, H, I]

PearlB = Pearl(liste_noeuds_G1, {E: "e1", H: "h1", G: "g1"})

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
