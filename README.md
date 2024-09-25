# Rendu Noté
Nom : Jules Poissonnet
Vous trouverez le jupyter notebook sous la forme du fichier rendu.ipynb.

# L'application

Il faut lancer trois choses pour que l'application fonctionne :
- Le serveur de l'API en python pour le ML
- Le serveur de l'API en bun pour écrire et lire dans la base de données csv
- Le serveur de l'application en vue

## API en python

Il faut lancer le fichier server/app.py avec python

## API en bun

Il faut d'abord installer bun https://bun.sh/docs/installation/
Ensuite, dans le dossier server, lancer la commande `bun install` puis `bun dev`

## Application en vue
Il vous faudra installer pnpm pour lancer l'application. https://pnpm.io/fr/installation
Depuis la racine du projet, lancer la commande `pnpm install` puis `pnpm dev`

# Fonctionnalités

Rendez-vous sur http://localhost:5173/ pour accéder à l'application.
Les prédicitions sont lancés quand les valeurs surfaces et prix sont rentrées et que les inputs changent.
Si vous remplissez les 3 inputs et que vous clickez en dehors des inputs, les valeurs des prédictions devraient s'afficher.

