class Crawler:
    config = dict()

    def __init__(self, config = None):
        self.starting_URL = None
        if config is not None:
            self.config = config
        if config is None:
            self.config = {
                "TargetURL": "",
                "CrawlDepth": 10,
                "PageNumberLimit": 20,
                "UserAgent": "",
                "RequestDelay": 2000
            }
    def crawl(self):
        pass
    def getConfig(self):
        return self.config
    def setConfig(self, config):
        if config is not None:
            self.config = config
    def reset(self):
        self.config = {
            "TargetURL": "",
            "CrawlDepth": 10,
            "PageNumberLimit": 20,
            "UserAgent": "",
            "RequestDelay": 2000
        }
    def getCrawlResults(self):
        pass
    def getTree(self):
        pass
