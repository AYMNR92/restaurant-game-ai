# 🥗 Restaurant Game AI - Systèmes Multi-Agents

Ce projet explore l'application de la **Théorie des Jeux** dans un environnement de simulation multi-agents. L'objectif est de développer et comparer différentes stratégies d'Intelligence Artificielle (IA) dans un jeu compétitif de collecte de ressources.

Des agents autonomes (cuisiniers) doivent naviguer dans un restaurant, collecter des ingrédients et préparer des plats tout en optimisant leurs déplacements et en anticipant les actions de leurs adversaires.

---

## 🧠 Stratégies Implémentées

Le cœur du projet réside dans l'implémentation et l'analyse comparative de plusieurs algorithmes de prise de décision :

- **Aléatoire (Random)** : Sert de baseline. L'agent agit sans logique précise.
- **Glouton (Greedy)** : Cherche à maximiser son gain immédiat (le plat le plus proche/rentable) sans considérer les autres.
- **Têtu (Stubborn)** : Choisit une stratégie fixe et s'y tient, peu importe l'évolution de la partie.
- **Stochastique** : Introduit une part de probabilité pondérée pour varier les approches.
- **Fictitious Play (Jeu Fictif)** : Apprend des actions passées de l'adversaire pour prédire son prochain coup et agir en conséquence.
- **Regret Matching** : Cherche à minimiser le "regret" d'avoir choisi une action plutôt qu'une autre par le passé, tendant vers un Équilibre de Nash.

---

## 🛠 Stack Technique

- **Langage :** Python 3
- **Moteur Graphique :** Pygame (pySpriteWorld)
- **Analyse de Données :** Matplotlib (génération de courbes de convergence et de regret)
- **Algorithmes :** Pathfinding (A*), Nash Equilibrium, Regret Minimization

---

## 🚀 Installation et Lancement

### Prérequis
Assurez-vous d'avoir Python installé sur votre machine.

### 1. Installation des dépendances

Installez les bibliothèques nécessaires via pip :

```bash
pip install -r requirements.txt
```

---

### 2. Lancer une simulation (Jeu)

Pour voir les agents s'affronter en temps réel dans l'interface graphique :

```bash
cd src
python main.py
```

Vous pouvez modifier les variables `iterations` ou les types d'agents directement dans le `main.py` pour tester différents matchups (ex : Glouton vs Fictitious Play).

---

### 3. Générer les graphiques d'analyse

Pour lancer une batterie de tests et générer les courbes de performance (comparaison des scores, convergence du regret) :

```bash
cd src
python create_graphs.py
```

Les résultats seront sauvegardés dans le dossier `graphs/`.

---

## 📊 Résultats et Analyse

Les simulations montrent la supériorité des stratégies adaptatives (comme le Fictitious Play) sur les stratégies statiques (Glouton) sur le long terme. Les courbes générées permettent de visualiser :

- Le score cumulé moyen
- La convergence vers l'équilibre de Nash
- L'évolution du regret au fil des itérations

Exemple de résultat (Fictitious Play vs Random) :

---

## 📂 Structure du Projet

```
.
├── docs/               # Rapport détaillé du projet et analyse théorique
├── graphs/             # Visualisation des résultats (courbes générées)
├── src/
│   ├── main.py         # Point d'entrée de la simulation visuelle
│   ├── create_graphs.py # Script de génération des statistiques
│   ├── search/         # Algorithmes de recherche de chemin (A*)
│   ├── pySpriteWorld/  # Framework graphique (moteur de jeu)
│   └── ...
├── requirements.txt    # Liste des dépendances
└── README.md
```
