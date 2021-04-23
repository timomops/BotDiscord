# PhanttoBot
## _Bot pour la guilde Clarity_
## Fonctionnalités

- Généré un channel et un rôle pour une candidature
- Proposé des strawpolls
- Pouvoir mute et démute les participants d'un channel qui ne sont pas admin
- Pouvoir supprimer X messages d'un coup
- Pouvoir chercher le raider.io d'une personne grâce à l'API raiderio

## Les commandes avec le prefixe "+"
- Administrateurs : `purge` `strawpoll` `participant` `closestrawpoll` `mute` `demute`
- Sans rôle : `Candidature`
- Standard : `raiderio` `ping`

## Fonctionnement de la fonctionnalité majeur : 
Lors de son arrivé sur le discord, la personne qui veut candidater doit écrire "+Candidature" dans le channel "apply".
Le bot va lui créer un rôle et un channel "candidature-`pseudo`" et lui envoyer un message pour lui expliquer ce qu'il doit faire.
Ce channel est visible par les admins et le rôle "roster", mais seulement les admins et le candidat peuvent écrire dedans.

## Prérequis
- Python 3.4

## Installation 
Pour faire fonctionner ce bot il faut sauvegarder le token dans un fichier .env
Exemple du fichier .env : 
```sh
key="yourtoken"
```
Pour faire fonctionner le bot : 
```sh
pip3 install -r requirement.txt
python3 main.py
```
