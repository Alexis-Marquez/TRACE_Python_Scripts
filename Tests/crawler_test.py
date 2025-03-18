import pytest
from backend import Crawler


@pytest.fixture
def setUpCrawler():
    crawler = Crawler.Crawler()
    yield crawler

# def test_crawl_result(setUpCrawler):
#     result = setUpCrawler.crawl()
#     assert isinstance(result, dict)

def test_crawler_constructor1(setUpCrawler):
    assert setUpCrawler.getConfig() is not None

def test_crawler_constructor2(setUpCrawler):
    assert len(setUpCrawler.getConfig()) > 0

def test_crawler_constructor3(setUpCrawler):
    setUpCrawler.setConfig({"TargetURL": "www.google.com/",
                "CrawlDepth": 100,
                "PageNumberLimit": 200,
                "UserAgent": "Mozilla/5.0",
                "RequestDelay": 20000})

    assert setUpCrawler.getConfig() == {"TargetURL": "www.google.com/",
                "CrawlDepth": 100,
                "PageNumberLimit": 200,
                "UserAgent": "Mozilla/5.0",
                "RequestDelay": 20000}

def test_crawler_constructor4():
    crawler = Crawler.Crawler({
        "TargetURL": "",
        "CrawlDepth": 10,
        "PageNumberLimit": 20,
        "UserAgent": "",
        "RequestDelay": 2000
    })
    assert crawler.getConfig() == {
        "TargetURL": "",
        "CrawlDepth": 10,
        "PageNumberLimit": 20,
        "UserAgent": "",
        "RequestDelay": 2000
    }
def test_crawler_reset():
    crawler = Crawler.Crawler({
            "TargetURL": "",
            "CrawlDepth": 10,
            "PageNumberLimit": 20,
            "UserAgent": "",
            "RequestDelay": 2000
        })
    crawler.reset()
    assert len(crawler.getConfig()) > 0