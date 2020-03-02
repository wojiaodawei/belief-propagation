#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    Implémente l'algorithme de propagation de croyances Pearl

    L'algorithme se décompose en deux grandes étapes : initialisation et propagation (calcul + envoi messages)
'''
class Pearl(object):

    def __init__(self, noeuds, evidences):
        """
        Constructeur logique.

        :param noeuds: liste des noeuds du réseau bayésien
        :param evidences: liste des noeuds évidents (avec leur état instancié)
        """
        self.noeuds = noeuds
        self.evidences = evidences
        for n in self.evidences:
            n.instancier(self.evidences[n])

    def initialisation(self):
        """
        Etape d'initialisation du réseau bayésien dans l'algo Pearl
        """

        print("\n---------------------- INITIALISATION ----------------------")

        for noeud in self.noeuds:
            for etat in noeud.tableP:
                if self.estEvident(noeud) and etat == self.evidences[noeud]:
                    noeud.tableP[etat]["Lambda"] = 1
                    noeud.tableP[etat]["Pi"] = 1
                    noeud.tableP[etat]["P"] = 1
                    noeud.modifPiCalcule(True)
                elif self.estEvident(noeud):
                    noeud.tableP[etat]["Lambda"] = 0
                    noeud.tableP[etat]["Pi"] = 0
                    noeud.tableP[etat]["P"] = 0
                    noeud.modifPiCalcule(True)
                elif noeud.estRacine():
                    noeud.tableP[etat]["Pi"] = noeud.tableProbCond[None][etat]
                    noeud.tableP[etat]["P"] = noeud.tableProbCond[None][etat]
                    noeud.tableP[etat]["Lambda"] = 1
                    noeud.modifPiCalcule(True)
                else:
                    noeud.tableP[etat]["Lambda"] = 1
            noeud.modifLambdaCalcule(True)

    def initPropagation(self):
        """
        Première étape de propagation de l'algorithme de Pearl dans le réseau bayésien noeuds
        """

        print("\n---------------------- INITIALISATION DE LA PROPRAGATION ----------------------")

        ######################################
        ## Initialisation de la propagation ##
        ######################################
        for noeud in self.noeuds:
            if noeud.estRacine() or self.estEvident(noeud):
                for f in noeud.lireFils():
                    noeud.envoyerPi(f)
            if noeud.estFeuille() or self.estEvident(noeud):
                for p in noeud.lireParents():
                    noeud.envoyerLambda(p)

            if not noeud.estRacine():
                if not self.estEvident(noeud):
                    self.calculPi(noeud)
                    for e in noeud.etats:
                        noeud.tableP[e]["P"] = noeud.tableP[e]["Pi"]
                    for f in noeud.lireFils():
                        noeud.envoyerPi(f)

    def propagation(self):
        """
        Etapes de propagation de l'algorithme de Pearl dans le réseau bayésien noeuds
        """

        print("\n---------------------- PROPRAGATION ----------------------")

        changement = True
        while changement:
            changement = False

            # ##################
            # ## Calcul du PI ##
            # ##################
            for noeud in self.noeuds:
                if not noeud.estRacine() and noeud.receptionPIcomplete() and not self.estEvident(noeud):
                    self.calculPi(noeud)
                    noeud.viderPisRecus()
                    changement = True

            # ######################
            # ## Calcul du LAMBDA ##
            # ######################
            for noeud in self.noeuds:
                if not noeud.estFeuille() and noeud.receptionLAMBDAcomplete() and not self.estEvident(noeud):
                    self.calculLambda(noeud)
                    noeud.viderLambdasRecus()
                    changement = True


            ###############################
            ## Envoi des LAMBDA-messages ##
            ###############################
            for noeud in self.noeuds:
                if not noeud.estRacine() and noeud.lambdaEstCalcule():
                    parents = noeud.lireParents()
                    pr = noeud.lirePisRecus()
                    if not noeud.receptionPIcomplete():
                        for p in parents:
                            if p not in pr and not self.estEvident(p):
                                noeud.envoyerLambda(p)
                                changement = True
                    noeud.modifLambdaCalcule(False)

            ###########################
            ## Envoi des PI-messages ##
            ###########################
            for noeud in self.noeuds:
                if not noeud.estFeuille() and noeud.piEstCalcule():
                    fils = noeud.lireFils()
                    lr = noeud.lireLambdasRecus()
                    if not noeud.receptionLAMBDAcomplete():
                        for f in fils:
                            if f not in lr and not self.estEvident(f):
                                noeud.envoyerPi(f)
                                changement = True
                    noeud.modifPiCalcule(False)

            ##################################
            ## Calcul de BEL(X) = λ(x).π(x) ##
            ##################################
            for noeud in self.noeuds:
                self.BEL(noeud)

    def calculPi(self, noeud):
        """
        Calcul du PI du noeud noeud lorsqu'il a reçu tous les PI-messages de ses parents

        :param noeud: Noeud courant dont le PI doit être calculé.
        """
        if not noeud.estRacine() and noeud.receptionPIcomplete() and not self.estEvident(noeud):
            print(noeud.lireNom(), "calcule son nouveau PI")
            tpc = noeud.lireTableProbCond()
            etats = noeud.lireEtats()
            tablep = noeud.lireTableP()
            for etat in etats:
                tablep[etat]["Pi"] = 0
                for pc in tpc:
                    pires = tpc[pc][etat]
                    for pcp in pc:
                        pires *= noeud.pis_recus[pcp[0]][pcp[1]]
                    tablep[etat]["Pi"] += pires
            noeud.viderPisRecus()
            noeud.modifTableP(tablep)
            noeud.modifPiCalcule(True)

    def calculLambda(self, noeud):
        """
        Calcul du LAMBDA du noeud noeud lorsqu'il a reçu tous les LAMBDA-messages de ses fils

        :param noeud: Noeud courant dont le LAMBDA doit être calculé.
        """
        if not noeud.estFeuille() and noeud.receptionLAMBDAcomplete() and not self.estEvident(noeud):
            print(noeud.lireNom(), "calcule son nouveau LAMBDA")
            etats = noeud.lireEtats()
            tablep = noeud.lireTableP()
            lrs = noeud.lireLambdasRecus()
            for etat in etats:
                for lr in lrs:
                    tablep[etat]["Lambda"] *= lrs[lr][etat]
            noeud.viderLambdasRecus()
            noeud.modifTableP(tablep)
            noeud.modifLambdaCalcule(True)

    @staticmethod
    def BEL(noeud):
        """
        Calcul de BEL(X) = λ(x).π(x)
        Puis NORMALISATION de P

        :param noeud: Noeud courant dont le BEL doit être calculé.
        """
        etats = noeud.lireEtats()
        tablep = noeud.lireTableP()
        somme = 0
        for etat in etats:
            tablep[etat]["P"] = tablep[etat]["Lambda"] * tablep[etat]["Pi"]
            somme += tablep[etat]["P"]
        for etat in etats:
            tablep[etat]["P"] /= somme
        noeud.modifTableP(tablep)

    def executer(self):
        """
        Execution de tout l'algorithme, commençant par l'initialisation suivie de la propagation
        """
        self.initialisation()
        self.propagation()

    def estEvident(self, noeud):
        """
        Indique si le noeud est une évidence ou pas

        :param noeud: noeud en question.
        :return True si ce noeud est une évidence, False sinon.
        """
        return noeud in self.evidences
