from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from backend.Crawler import Crawler
from backend.Fuzzer import Fuzzer
from mdp3 import WebScraper, nlp_subroutine, CredentialGeneratorMDP

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


crawler_data: Optional [Dict[str, Any]] = None
crawler_links: Optional[list[str]] = None

class CrawlerConfig(BaseModel):
    TargetURL: str
    CrawlDepth: int
    PageNumberLimit: int
    UserAgent: str
    RequestDelay: float


class FuzzerConfig(BaseModel):
    TargetURL: str
    HTTPMethod: str
    Cookies: str
    HideStatusCode: list
    ShowOnlyStatusCode: list
    PageLimit: int
    WordList: list

@app.post("/fuzzer")
def set_up_fuzzer(config: FuzzerConfig):
    global fuzzer_data, fuzzer_links
    try:
        fuzzer_data = None
        fuzzer_links = None

        fuzzer = Fuzzer(config.model_dump())
        print("Received config: ", config)
        fuzzer.start()
        
        fuzzer_data = fuzzer.get_data()
        fuzzer_links = fuzzer.get_links()

        return {"message": "Fuzz completed successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/fuzzer/data")
def get_fuzzer_data():
    if fuzzer_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    return fuzzer_data
    
@app.post("/crawler")
def set_up_crawler(config: CrawlerConfig):
    global crawler_data, crawler_links
    try:
        crawler_data = None
        crawler_links = None

        crawler = Crawler(config.model_dump())
        print("Received config:", config)
        if crawler.tree_creator is not None:
            print(f"Tree before crawl: {crawler.tree_creator.display_data()}")
        crawler.start_crawl()
        print(f"Tree after crawl: {crawler.tree_creator.display_pretty(crawler.tree_creator.tree.root, '    ')}")

        crawler_data = crawler.tree_creator.get_tree_map(crawler.tree_creator.tree.root)
        crawler_links = crawler.getCrawlResults()

        return {"message": "Crawl completed successfully"}
    except Exception as e:
        print(e)
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

