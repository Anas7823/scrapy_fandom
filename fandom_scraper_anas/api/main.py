from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
import os

def append_json_to_array(filepath, new_entry):
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([new_entry], f, ensure_ascii=False, indent=2)
        return

    with open(filepath, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Le fichier JSON ne contient pas un tableau.")
        except json.JSONDecodeError:
            data = []

        data.append(new_entry)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()


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
        # Ajout dans le fichier JSON principal
        append_json_to_array("../../data/fandom_data.json", {
            data
        })
        

        return {"status": "success", "message": f"Scraping de {data.url} lancé."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
