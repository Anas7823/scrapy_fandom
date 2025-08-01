from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess

app = FastAPI()

# Autoriser les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
def scrape_url(data: ScrapeRequest):
    try:
        subprocess.run(["scrapy", "crawl", "fandom", "-a", f"url={data.url}"], cwd="../fandom_scraper_anas")
        # Ajouter le résultat au fichier JSON
        with open("../fandom_scraper_anas/data/fandom_data.json", "a") as f:
            f.write(f'\n{{"url": "{data.url}", "status": "scraped"}}\n')
            
        return {"status": "success", "message": f"Scraping de {data.url} lancé."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
