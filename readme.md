# Presentation projet
## Nom du projet
	*Trouve-le*
## Logo
![Logo de trouvele](static/img/logo.png)
## Description

Trouve-le est une application qui permet de retrouver des objets perdus en les déclarents.
Vous pouvez informer la communauté lorsque vous avez perdu un objet et aussi informer si vous en avez rétrouvé.

## Fonctionnalités
1. Creation d'un compte utilisateur (Validation par e-mail)
2. Connexion à son profile
3. Recherche dans la liste des déclarations (Pertes, retrouvailles )
4. Déclaration de pertes ou de retrouvailles
5. Contacter un membre de la communauté

# Spécifications techniques

## Technologies

FrontEnd :
----------
- html
- css
- js

BackEnd:
--------
- python3 
	+ Framework : Flask
	+ Database : Deta Base
	+ Storage : Deta Drive
	
Le dévéloppement actuelle de trouve-le se fait avec la technologie du microframework python **flask**.
La base de données et la gestion de fichiers est gérer actuellemnt avec Deta


## Arboressence

```bash
.
│   .gitignore
│   main.py
│   readme.md
│   requirements.txt         : [dependences] Ensembles des packages à installer
│   trouvele.py              : Programme principale (Routings...)
│   _database.py             : [module] Fonctions et objets de base de données
│   _declaration.py          : [module] Base de données déclarations(temp)
│   _forms.py                : [module] Formulaires 
│   _validation.py           : [module] Validation de données
│
├───static
│   ├───css
│   │       animate.min.css      : [Framework] Animation
│   │       daisyui.css          : [Framework] Framework UI
│   │       session_error.css    : [style] 
│   │       signup.css           : [style]
│   │       tailwind.min.css     : [Framework]
│   │       trouvele_profil.css  : [style]
│   │       validation.css       : [style]
│   │
│   ├───img                      : [Image locale]
│   │       c1.png
│   │       c2.png
│   │       c3.png
│   │       default_pp.webp
│   │       logo.png              : logo
│   │       profile-default.png   : pp par defaut
│   │
│   └───js
│           jquery.min.js
│           tailwindcss.js
│           tailwindcss.min.js
│           validation.js
│           w3.js
│
├───templates
        accueil.html
        bottom_nav.html
        carousel.html
        header.html
        index.html
        login.html
        session_error.html
        signup.html
        validation.html
```

## Réalisés:
- Splash screen
- carousel
- signup
- validation par e-mail
- login
	+ login
	+ logout

## A faire

- validation par sms 
- validation par whatsapp
- declaration
- restauration de mot de passe
- Contacter un autre utilisateur de la communauté

# Demos

![Gif 1](demo/demo1.gif) 

![Gif 2](demo/demo2.gif) 

![Gif 3](demo/demo3.gif) 

![Gif 4](demo/demo4.gif)
