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
    crawler = Crawler.Crawler({"TargetURL": "www.google.com/",
                "CrawlDepth": 100,
                "PageNumberLimit": 200,
                "UserAgent": "Mozilla/5.0",
                "RequestDelay": 20000})
    crawler.reset()
    assert crawler.getConfig() == crawler.getDefaultConfig()

def test_crawler_constructor5():
    crawler = Crawler.Crawler({})
    assert crawler.getConfig() == crawler.getDefaultConfig()

def test_crawler_reset1():
    crawler = Crawler.Crawler()
    crawler.reset()
    assert len(crawler.getConfig()) > 0

def test_crawler_reset2():
    crawler = Crawler.Crawler({"TargetURL": "www.google.com/",
                "CrawlDepth": 100,
                "PageNumberLimit": 200,
                "UserAgent": "Mozilla/5.0",
                "RequestDelay": 20000})
    crawler.reset()
    assert crawler.getConfig() == crawler.getDefaultConfig()

def test_setConfig1(setUpCrawler):
    with pytest.raises(ValueError):
        setUpCrawler.setConfig(None)

def test_setConfig2(setUpCrawler):
    with pytest.raises(ValueError):
        setUpCrawler.setConfig({})

def test_getConfig1(setUpCrawler):
    setUpCrawler.config = {}
    with pytest.raises(ValueError):
        setUpCrawler.getConfig()

def test_getConfig2(setUpCrawler):
    setUpCrawler.config = None
    with pytest.raises(ValueError):
        setUpCrawler.getConfig()