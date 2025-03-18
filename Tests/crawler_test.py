import pytest
from backend import Crawler


@pytest.fixture
def setUpCrawler():
    crawler = Crawler.Crawler()
    yield crawler

def test_crawl(setUpCrawler):
    result = setUpCrawler.crawl()
    assert isinstance(result, dict)
