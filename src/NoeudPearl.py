#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Noeud import *

'''
    Hérite de la classe Noeud
    Implémente un noeud d'un réseau bayésien pour l'algorithme de Pearl
    
    Chaque noeud possède une table de probabilités conditionnelles
    Ainsi qu'une table de probabilités qui sert pour l'algorithme Pearl
'''
class NoeudPearl(Noeud):

    def __init__(self, nom, etats):
        """
        Constructeur logique.

        :param nom: Nom du noeud
        :param etats: Etats possibles du noeud
        """
        super().__init__(nom)
        self.etats = etats
        # Initialisation de la table de probabilités
        self.tableP = {}
        for e in etats:
            self.tableP[e] = {"Pi": None, "Lambda": None, "P": None}
        # Table de probabilités conditionnelles
        self.tableProbCond = {}
        # Dictionnaire des PI-messages recus
        self.pis_recus = {}
        # Dictionnaire des LAMBDA-messages recus
        self.lambdas_recus = {}
        self.pi_calcule = False
        self.lambda_calcule = False

    ##########################
    ## Fonctions sur les PI ##
    ##########################
    def envoyerPi(self, enfant):
        """
        Envoi un PI-message pour chacun des états du noeud courant à son fils

        :param enfant: Noeud fils du noeud courant.
        """
        pis = {}
        for e in self.etats:
            pis[e] = self.tableP[e]["Pi"]
        print(self.nom, "Propagation des PI-messages à", enfant.lireNom(), "-->", pis)
        enfant.recevoirPi(self, pis)

    def receptionPIcomplete(self):
        """
        Vérifie si un noeud a recu tous les PI-messages de ses parents.

        :return: True si le noeud courant a recu tous les PI-messages de ses parents,
                    False sinon
        """
        correspondances = 0
        for parent in self.parents:
            if parent in self.pis_recus:
                correspondances += 1
        return correspondances != 0 and correspondances == len(self.parents)

    def recevoirPi(self, noeud, pis):
        """
        Ajoute le PI-message recu d'un Noeud

        :param noeud: Noeud courant
        :param pis: PI-messages à recevoir
        """
        self.pis_recus[noeud] = pis

    def modifPiCalcule(self, nouv_bool):
        """
        Mutateur

        :param nouv_bool: Booléen
        """
        self.pi_calcule = nouv_bool

    def viderPisRecus(self):
        """
        Vide le dictionnaire des PI-messages recus
        """
        self.pis_recus = {}

    def piEstCalcule(self):
        """
        Accesseur

        :return: True si le PI est calcule, False sinon.
        """
        return self.pi_calcule

    def lirePisRecus(self):
        """
        Accesseur

        :return: Dictionnaire des PI-messages recus
        """
        return self.pis_recus

    ##############################
    ## Fonctions sur les LAMBDA ##
    ##############################
    def envoyerLambda(self, parent):
        """
        Envoi un LAMBDA-message pour
        chacun des états du noeud parent multiplie par la probabilité conditionnelle
        de chacun des etats du noeud courant sachant l'état du parent

        :param parent: Noeud parent du noeud courant.
        """
        etats_parent = parent.lireEtats()
        lmbda_message = {}
        for ep in etats_parent:
            lmbda = 0
            for e in self.etats:
                pc = self.chercheProbCond(parent, ep, e)
                lmbda += pc * self.tableP[e]["Lambda"]
            lmbda_message[ep] = lmbda
        print(self.nom, "Propagation des LAMBDA-messages à", parent.lireNom(), "-->", lmbda_message)
        parent.recevoirLambda(self, lmbda_message)

    def recevoirLambda(self, noeud, lmbda):
        """
        Ajoute le LAMBDA-message recu d'un Noeud

        :param noeud: Noeud courant
        :param lmbda: LAMBDA-messages à recevoir
        """
        self.lambdas_recus[noeud] = lmbda

    def receptionLAMBDAcomplete(self):
        """
        Vérifie si un noeud a recu tous les LAMBDA-messages de ses enfants.

        :return: True si le noeud courant a recu tous les LAMBDA-messages de ses enfants,
                    False sinon
        """
        correspondances = 0
        for enfant in self.fils:
            if enfant in self.lambdas_recus:
                correspondances += 1
        return correspondances != 0 and correspondances == len(self.fils)

    def modifLambdaCalcule(self, nouv_bool):
        """
        Mutateur

        :param nouv_bool: Booléen
        """
        self.lambda_calcule = nouv_bool

    def viderLambdasRecus(self):
        """
        Vide le dictionnaire des LAMBDA-messages recus
        """
        self.lambdas_recus = {}

    def lambdaEstCalcule(self):
        """
        Accesseur

        :return: True si le LAMBDA est calcule, False sinon.
        """
        return self.lambda_calcule

    def lireLambdasRecus(self):
        """
        Accesseur

        :return: Dictionnaire des LAMBDA-messages recus
        """
        return self.lambdas_recus

    #############################
    #  ACCESSEURS & MUTATEURS   #
    #############################
    def chercheProbCond(self, parent, etat_parent, etat):
        """
        Renvoie la probabilité conditionnelle du noeud courant à l'état "etat",
        sachant le noeud parent à l'état "etat_parent"

        :param parent: Noeud parent
        :param etat_parent: Du parent
        :param etat: Du noeud courant
        :return: Une probabilités
        """
        pc = 0
        for t in self.tableProbCond:
            # Un seul parent
            if (parent, etat_parent) in t and len(t) == 1:
                pc = self.tableProbCond[t][etat]
            # Plusieurs parents
            elif (parent, etat_parent) in t and len(t) > 1:
                pc += self.tableProbCond[t][etat]
        return pc

    def ajouterTableProbCond(self, nouv_table):
        self.tableProbCond = nouv_table

    def modifTableP(self, nouv_tablep):
        self.tableP = nouv_tablep

    def instancier(self, etat):
        if etat not in self.etats:
            print("Pas dans les etats possibles du noeud")
            exit(1)

    def lireEtats(self):
        return self.etats

    def lireTableProbCond(self):
        return self.tableProbCond

    def lireTableP(self):
        return self.tableP

    #############
    # AFFICHAGE #
    #############
    def afficher(self):
        print("Noeud :", self.nom)
        print("       PI    |   LAMBDA  |  P")
        print("-----------------------------------")
        for etat in self.etats:
            pi = self.tableP[etat]["Pi"]
            lmbda = self.tableP[etat]["Lambda"]
            p = self.tableP[etat]["P"]
            print(etat, " | ", pi, "  |  ", lmbda, "  | ", p)
        print("\n")

    def __repr__(self):
        return '<NoeudPearl %s>' % self.nom
