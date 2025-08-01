from urllib import request
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import asyncio
import os
import json
from datetime import datetime
from typing import Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fandom Scraper API", version="1.0.0")

# Configuration CORS pour votre frontend Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class ScrapingRequest(BaseModel):
    command: str = "scrapy crawl fandom"
    path: str = r"C:\Users\willi\Documents\Ecole_ipssi_MIA4\juillet_aout_2025\fandom_scrape_tp\scrapy_fandom\fandom_scraper_anas"
    options: Optional[dict] = None

class ScrapingResponse(BaseModel):
    success: bool
    message: str
    process_id: Optional[str] = None
    itemsScraped: Optional[int] = None
    error: Optional[str] = None

# Variables globales pour le suivi des processus
active_processes = {}
scraping_status = {
    "is_running": False,
    "progress": 0,
    "status": "Idle",
    "start_time": None,
    "items_scraped": 0
}

@app.get("/")
async def root():
    return {"message": "Fandom Scraper API is running"}

@app.get("/api/scraping/status")
async def get_scraping_status():
    """Obtenir le statut actuel du scraping"""
    return scraping_status

@app.post("/api/start-scraping", response_model=ScrapingResponse)
async def start_scraping(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """Lancer le processus de scraping en arrière-plan"""
    
    # Vérifier si un scraping est déjà en cours
    if scraping_status["is_running"]:
        raise HTTPException(
            status_code=409, 
            detail="Un processus de scraping est déjà en cours"
        )
    
    # Vérifier que le chemin existe
    if not os.path.exists(request.path):
        raise HTTPException(
            status_code=400,
            detail=f"Le chemin spécifié n'existe pas: {request.path}"
        )
    
    try:
        # Initialiser le statut
        scraping_status.update({
            "is_running": True,
            "progress": 0,
            "status": "Démarrage...",
            "start_time": datetime.now().isoformat(),
            "items_scraped": 0
        })
        
        # Lancer le scraping en arrière-plan
        background_tasks.add_task(run_scraping_process, request)
        
        return ScrapingResponse(
            success=True,
            message="Processus de scraping démarré avec succès",
            process_id="scraping_001"
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du scraping: {str(e)}")
        scraping_status["is_running"] = False
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du démarrage du scraping: {str(e)}"
        )

async def run_scraping_process(request: ScrapingRequest):
    """Exécuter le processus de scraping"""
    try:
        # Changer vers le répertoire de travail
        original_cwd = os.getcwd()
        os.chdir(request.path)
        
        logger.info(f"Démarrage du scraping dans: {request.path}")
        logger.info(f"Commande: {request.command}")
        
        # Mise à jour du statut
        scraping_status.update({
            "progress": 10,
            "status": "Initialisation du spider..."
        })
        
        # Créer le processus avec capture de sortie
        process = await asyncio.create_subprocess_shell(
            request.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=request.path
        )
        
        # Simuler la progression (vous pouvez l'adapter selon votre spider)
        progress_updates = [
            (20, "Connexion à Fandom..."),
            (35, "Exploration des pages..."),
            (50, "Extraction des données..."),
            (70, "Traitement des éléments..."),
            (85, "Sauvegarde en cours..."),
            (95, "Finalisation...")
        ]
        
        # Lancer les mises à jour de progression
        asyncio.create_task(update_progress(progress_updates, process))
        
        # Attendre la fin du processus
        stdout, stderr = await process.communicate()
        
        # Restaurer le répertoire original
        os.chdir(original_cwd)
        
        if process.returncode == 0:
            # Analyser les résultats
            items_scraped = await analyze_scraping_results(stdout.decode())
            
            scraping_status.update({
                "is_running": False,
                "progress": 100,
                "status": "Terminé avec succès",
                "items_scraped": items_scraped
            })
            
            logger.info(f"Scraping terminé avec succès. {items_scraped} éléments traités")
            
        else:
            error_msg = stderr.decode() if stderr else "Erreur inconnue"
            logger.error(f"Erreur lors du scraping: {error_msg}")
            
            scraping_status.update({
                "is_running": False,
                "progress": 0,
                "status": f"Erreur: {error_msg[:100]}...",
                "items_scraped": 0
            })
            
    except Exception as e:
        logger.error(f"Exception lors du scraping: {str(e)}")
        scraping_status.update({
            "is_running": False,
            "progress": 0,
            "status": f"Erreur: {str(e)}",
            "items_scraped": 0
        })
    finally:
        # Assurer que le répertoire est restauré
        try:
            os.chdir(original_cwd)
        except:
            pass

async def update_progress(progress_updates, process):
    """Mettre à jour la progression pendant l'exécution"""
    for progress, status in progress_updates:
        if process.returncode is None:  # Le processus est toujours en cours
            scraping_status.update({
                "progress": progress,
                "status": status
            })
            await asyncio.sleep(2)  # Attendre 2 secondes entre les mises à jour
        else:
            break

async def analyze_scraping_results(stdout_content: str) -> int:
    """Analyser les résultats du scraping pour compter les éléments"""
    try:
        # Rechercher les patterns dans la sortie Scrapy
        lines = stdout_content.split('\n')
        items_scraped = 0
        
        for line in lines:
            # Chercher les lignes qui indiquent le nombre d'items scrapés
            if 'item_scraped_count' in line.lower():
                # Extraire le nombre
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.isdigit():
                        items_scraped = int(part)
                        break
            elif 'scraped' in line.lower() and 'items' in line.lower():
                # Pattern alternatif
                import re
                numbers = re.findall(r'\d+', line)
                if numbers:
                    items_scraped = int(numbers[-1])
        
        return items_scraped
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse des résultats: {str(e)}")
        return 0

@app.post("/api/stop-scraping")
async def stop_scraping():
    """Arrêter le processus de scraping en cours"""
    if not scraping_status["is_running"]:
        raise HTTPException(
            status_code=400,
            detail="Aucun processus de scraping en cours"
        )
    
    try:
        # Ici vous pourriez arrêter le processus si nécessaire
        # Pour l'instant, on se contente de marquer comme arrêté
        scraping_status.update({
            "is_running": False,
            "progress": 0,
            "status": "Arrêté par l'utilisateur"
        })
        
        return {"success": True, "message": "Scraping arrêté"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'arrêt: {str(e)}"
        )

@app.get("/api/scraping/logs")
async def get_scraping_logs():
    """Obtenir les logs du dernier scraping"""
    # Ici vous pouvez implémenter la lecture des fichiers de logs
    return {"logs": "Logs non disponibles pour le moment"}

@app.get("/api/scraped-data/refresh")
async def refresh_scraped_data():
    """Recharger les données scrapées depuis le fichier JSON"""
    try:
        # Chemin vers votre fichier de données
        data_path = os.path.join(request.path, "data", "scrapedData.json")
        
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                "success": True,
                "count": len(data),
                "last_updated": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Fichier de données introuvable"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du rechargement: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )