#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Implémente un arbre:
    Chaque noeud possède un nom,
    ainsi qu'un nombre arbitraire d'enfants
    et aussi un nombre arbitraire de parents
"""
class Noeud(object):

    def __init__(self, nom):
        self.nom = nom
        self.parents = []
        self.fils = []

    def ajouterParent(self, nouv_parent):
        self.parents.append(nouv_parent)

    def ajouterFils(self, nouv_fils):
        nouv_fils.ajouterParent(self)
        self.fils.append(nouv_fils)

    def estRacine(self):
        return len(self.parents) == 0

    def estFeuille(self):
        return len(self.fils) == 0

    def lireParents(self):
        return self.parents

    def lireFils(self):
        return self.fils

    def lireNom(self):
        return self.nom

    def __repr__(self):
        return '<Noeud %s>' % self.nom


