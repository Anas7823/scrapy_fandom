✍️ Justification des choix techniques

1. FastAPI pour le backend
FastAPI a été choisi pour développer l’API backend grâce à sa rapidité, sa simplicité et sa capacité à gérer des requêtes asynchrones efficacement. Sa compatibilité avec Python permet une intégration facile avec les outils existants, comme Scrapy pour le scraping. De plus, FastAPI génère automatiquement une documentation interactive (Swagger), facilitant ainsi les tests et la maintenance.

2. Scrapy pour le scraping
Scrapy est un framework Python spécialisé dans le web scraping, permettant de gérer efficacement la navigation sur les pages, l’extraction des données, et la gestion des requêtes asynchrones. Son intégration dans le projet permet d’automatiser la récupération des données sur des sites complexes comme Fandom.

3. Communication via subprocess
Le choix d’appeler Scrapy via un subprocess depuis FastAPI permet de découpler le processus de scraping du serveur API. Cette approche assure que les opérations lourdes ou bloquantes ne ralentissent pas la gestion des requêtes HTTP, tout en gardant une architecture simple.

4. Stockage des résultats dans un fichier JSON
Le format JSON a été retenu pour stocker les résultats du scraping de manière structurée, facilement exploitable par le frontend. L’écriture en mode append permet de conserver un historique des URLs scrappées tout en évitant la perte de données.

5. Frontend Vue.js
Vue.js est utilisé pour construire l’interface utilisateur grâce à sa simplicité, sa réactivité et sa courbe d’apprentissage douce. La liaison des données dynamiques avec des directives comme v-if et la gestion des erreurs d’affichage d’image assurent une expérience utilisateur fluide.

6. Gestion des CORS avec FastAPI
L’ajout du middleware CORS dans FastAPI permet de sécuriser les échanges entre le frontend et le backend tout en autorisant les requêtes provenant de différentes origines lors du développement.

⚙️ Instructions pour exécuter le scraper + le front

- Avoir un node v 22 min

Pour lancer le back il faut aller dans > cd .\fandom_scraper_anas\api
Puis executer la commande > uvicorn main:app --reload --port 8000


Pour le front il faut aller dans > cd .\frontend\GameScrapy
Puis executer la commande > npm install
Et la commande > npm run dev

Problème rencontrer :

Le resultat inclus dans le json n'entre pas correctement dans le tableau et génère une erreur de syntaxe