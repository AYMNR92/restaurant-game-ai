# -*- coding: utf-8 -*-

# Nicolas, 2024-02-09
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'restaurant-map2'
    #game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 500  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 40 # nb de pas max par episode
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nb_lignes = game.spriteBuilder.rowsize
    nb_cols = game.spriteBuilder.colsize
    assert nb_lignes == nb_cols # a priori on souhaite un plateau carre
    lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les objets)
    lMax=nb_lignes-2
    cMin=2
    cMax=nb_cols-2

    
    players = [o for o in game.layers['joueur']]
    nb_players = len(players)

    pos_restaurants = [(3,4),(3,7),(3,10),(3,13),(3,16)] # 5 restaurants positionnes
    nb_restos = len(pos_restaurants)
    capacity = [1]*nb_restos

    coupe_files = [o for o in game.layers["ramassable"]] # a utiliser dans le cas de la variante coupe-file
    nb_coupe_files= len(coupe_files)

    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets ou de joueurs
    #-------------------------------
    
    def item_states(items):
        # donne la liste des coordonnees des items
        return [o.get_rowcol() for o in items]
    
    def player_states(players):
        # donne la liste des coordonnees des joueurs
        return [p.get_rowcol() for p in players]
    

    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    print("lecture carte")
    print("-------------------------------------------")
    print('joueurs:', nb_players)
    print("restaurants:",nb_restos)
    print("lignes:", nb_lignes)
    print("colonnes:", nb_cols)
    print("coup_files:",nb_coupe_files)
    print("-------------------------------------------")

    #-------------------------------
    # Carte demo 
    # 8 joueurs
    # 5 restos
    #-------------------------------
    
        
    #-------------------------------

    #-------------------------------
    # Fonctions definissant les positions legales et placement aléatoire
    #-------------------------------

    
    def legal_position(pos):
        row,col = pos
        # une position legale est dans la carte et pas sur un objet deja pose ni sur un joueur ni sur un resto
        return ((pos not in item_states(coupe_files)) and (pos not in player_states(players)) and (pos not in pos_restaurants) and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    def draw_random_location():
        # tire au hasard un couple de positions permettant de placer un item
        while True:
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            if legal_position(random_loc):
                return(random_loc)

    def players_in_resto(r):
        """
        :param r: id of the resto
        :return: id of players in resto
        """
        are_here = []
        pos = pos_restaurants[r]
        for i in range(0,nb_players):
            if players[i].get_rowcol() == pos:
                are_here.append(i)
        return are_here

    def nb_players_in_resto(r):
        """
        :param r: id of resto
        :return: int number of players currently here
        """
        return len(players_in_resto(r))

    def calcul_points_iter(points):    
        for r in range(0,nb_restos):
            cr = capacity[r]
            in_resto = players_in_resto(r)
            choose_from = []
            
            for p in in_resto:
                if has_coupe_file[p]:
                    choose_from.append(p)
                    has_coupe_file[p] = False        

            if choose_from == [] : 
                choose_from = in_resto

            if choose_from:
                choices = np.random.choice(choose_from, cr)
            else:
                choices = []
                    
            for p in choices:
                points[p] += 1

            # print(in_resto)
            # print(choose_from)
            # print(choices)
            # print('---')

    nb_jour =  100
    print(f"NbJours : {nb_jour}")
    
    points = [0]*nb_players
    has_coupe_file = [False]*nb_players

    for i in range(nb_jour):
        #-------------------------------
        # On place tous les coupe_files du bord au hasard
        #-------------------------------
                        
        for o in coupe_files:
            (x1,y1) = draw_random_location()
            o.set_rowcol(x1,y1)
            game.mainiteration()

        #-------------------------------
        # On place tous les joueurs au hasard sur la ligne du bas
        #-------------------------------

        y_init = [3,5,7,9,11,13,15,17]
        x_init = 18
        random.shuffle(y_init)
        for i in range(0,nb_players):
            players[i].set_rowcol(x_init,y_init[i])
            game.mainiteration()


        # -------------------------------
        # Strategie aleatoire
        # -------------------------------

        choix_resto=[]
        path = []
        for p in range(0,nb_players):
            print("Player ", p)
            choix_resto.append(pos_restaurants[random.randint(0, nb_restos-1)])
            print("Going to ", choix_resto[p])
            pos_player = (x_init,y_init[p])
            print("Starting from ", pos_player)

        # -------------------------------
        # calcul A* pour chaque joueur
        # -------------------------------

            g = np.ones((nb_lignes, nb_cols), dtype=bool)  # une matrice remplie par defaut a True

            for i in range(nb_lignes):  # on exclut aussi les bordures du plateau
                g[0][i] = False
                g[1][i] = False
                g[nb_lignes - 1][i] = False
                g[nb_lignes - 2][i] = False
                g[i][0] = False
                g[i][1] = False
                g[i][nb_lignes - 1] = False
                g[i][nb_lignes - 2] = False
            prob = ProblemeGrid2D(pos_player, choix_resto[p], g, 'manhattan')
            path.append(probleme.astar(prob, verbose=False))
            print("Chemin trouvé:", path[p])


        #-------------------------------
        # Boucle principale de déplacements 
        #-------------------------------

        for i in range(iterations):
            
            for j in range(0,nb_players):

                # on fait bouger chaque joueur jusqu'à son but
                # en suivant le chemin trouve avec A*

                if i<len(path[j]): # si le joueur n'est pas deja arrive
                    (row,col) = path[j][i]
                    players[j].set_rowcol(row, col)
                    print("pos joueur:", j,  row, col)
                    
                    for id, (item_row, item_col) in enumerate(item_states(coupe_files)):
                        if (item_row == row and item_col == col):
                            if not has_coupe_file[j]:
                                has_coupe_file[j] = True
                                coupe_files.pop(id)
                                players[j].ramasse(game.layers)
                                print("has_coupe_file:", j,  row, col)

                                  
                            

                # mise à jour du pleateau de jeu
                #game.mainiteration()



            # mise à jour du pleateau de jeu
            game.mainiteration()

        # -------------------------------
        # Calcul des scores
        # -------------------------------


        # calcul du nombre de joueurs sur chaque resto

        attendance = [0]*nb_restos
        for r in range(0,nb_restos):
            attendance[r]=nb_players_in_resto(r)

        print(attendance)

        # calcul du service et points
        
        calcul_points_iter(points)

        #depose les coupes-files
        for i in range(nb_players):
            # on n'utilise pas depose car elle met l'item a la position du player 
            # players[i].depose(game.layers)
            
            
            candidats = [o for o in players[i].inventory]
            
            if candidats:
                obj = candidats[0]
                players[i].inventory.remove()
                game.layers['ramassable'].add( obj )
                coupe_files = [o for o in game.layers["ramassable"]]
                nb_coupe_files= len(coupe_files)
    
        print(points)
                
    pygame.quit()

    #-------------------------------

if __name__ == '__main__':
    main()