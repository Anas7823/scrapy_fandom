- Avoir un node v 22 min

Pour lancer le back il faut aller dans > cd .\fandom_scraper_anas\api
Puis executer la commande > uvicorn main:app --reload --port 8000


Pour le front il faut aller dans > cd .\frontend\GameScrapy
Puis executer la commande > npm install
Et la commande > npm run dev


Problème rencontrer :

Au lieu de scrapper en + le lien fandom mis dans la barre de recherche front, notre scraper re scrap les liens définis en dur.