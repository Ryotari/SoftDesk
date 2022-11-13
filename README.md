# SoftDesk
Ce projet est une API REST réalisée pour la société (fictive) SoftDesk.
L'application permet de remonter et suivre des problèmes techniques (issue tracking system). 

## Documentation

Tout les endpoints, leurs détails ainsi que des exemples d'utilisation sont décrits dans la [documentation](https://documenter.getpostman.com/view/20066472/2s8YRmHsHE). 

## Installation & lancement

Lancez la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/Ryotari/SoftDesk.git
```
Placez vous dans le dossier adéquat, puis créez un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, activez-le.
Windows:
```
env\scripts\activate.bat
```
Linux:
```
source env/bin/activate
```
Installez ensuite les packages requis:
```
pip install -r requirements.txt
```
Placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations avec les commandes suivantes:
```
python manage.py makemigrations
```
Puis: 
```
python manage.py migrate
```
Il ne vous reste plus qu'à lancer le serveur: 
```
python manage.py runserver
```
Vous pouvez ensuite utiliser l'applicaton via Postman, avec les différents endpoints décrits dans la documentation. 
