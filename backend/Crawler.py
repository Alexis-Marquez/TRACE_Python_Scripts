class Crawler:
    config = dict()
    default_config =  {
            "TargetURL": "",
            "CrawlDepth": 10,
            "PageNumberLimit": 20,
            "UserAgent": "",
            "RequestDelay": 2000
        }
    def __init__(self, config = None):
        if config is None:
            self.reset()
        elif len(config) == 0:
            self.reset()
        elif config is not None:
            self.config = config

    def crawl(self):
        pass
    def getConfig(self):
        if self.config is None:
            self.reset()
            raise ValueError("Config cannot be None, resetting to default")
        elif len(self.config) == 0:
            self.reset()
            raise ValueError("Config cannot be an empty list, resetting to default")
        elif self.config is not None:
            return self.config

    def setConfig(self, config):
        if config is None:
            self.reset()
            raise ValueError("Config cannot be None, resetting to default")
        elif len(config) == 0:
            self.reset()
            raise ValueError("Config cannot be an empty list, resetting to default")
        elif config is not None:
            self.config = config
    def reset(self):
        self.config = None
        self.config = self.default_config
    def getCrawlResults(self):
        pass
    def getTree(self):
        pass
    def getDefaultConfig(self):
        return self.default_config
