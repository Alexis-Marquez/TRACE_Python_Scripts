from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from backend.Crawler import Crawler
from mdp3 import WebScraper, nlp_subroutine, CredentialGeneratorMDP

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crawler_data: Optional[Dict[str, Any]] = None
crawler_links: Optional[list[str]] = None

class CrawlerConfig(BaseModel):
    TargetURL: str
    CrawlDepth: int
    PageNumberLimit: int
    UserAgent: str
    RequestDelay: float

@app.post("/crawler")
def set_up_crawler(config: CrawlerConfig):
    global crawler_data, crawler_links
    try:
        crawler_data = None
        crawler_links = None

        crawler = Crawler(config.model_dump())
        print("Received config:", config)

        crawler.startCrawl()
        crawler_data = crawler.tree_creator.get_tree_map(crawler.tree_creator.tree.root)
        crawler_links = crawler.getCrawlResults()

        return {"message": "Crawl completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/crawler/data")
def get_crawler_data():
    if crawler_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    return crawler_data

@app.get("/webscraper")
def get_webscraper_data():
    if crawler_data is None or crawler_links is None:
        raise HTTPException(status_code=400, detail="No data available")

    csv_path = "web_text.csv"
    wordlist_path = "wordlist.txt"

    scraper = WebScraper(crawler_links)
    scraper.generate_csv(csv_path)
    nlp_subroutine(csv_path)

    try:
        generator = CredentialGeneratorMDP(csv_path, wordlist_path)
        credentials = generator.generate_credentials(15)
        return {"credentials": credentials}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating credentials: {e}")

