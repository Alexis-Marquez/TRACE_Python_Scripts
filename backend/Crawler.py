import socket
from typing import Dict, Any
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from backend.DirectoryTreeCreator import DirectoryTreeCreator

class Crawler:
    config = dict()
    default_config =  {
            "TargetURL": "www.example.com",
            "CrawlDepth": 10,
            "PageNumberLimit": int(20),
            "UserAgent": "",
            "RequestDelay": 2000
        }
    def __init__(self, config = None):
        if config is None:
            self.reset()
            return
        elif len(config) == 0:
            self.reset()
            return
        for key in self.default_config.keys():
            if key not in config:
                raise KeyError("Invalid config dictionary")
        try:
            self.config = {
                "TargetURL": config["TargetURL"],
                "CrawlDepth": int(config["CrawlDepth"]),
                "PageNumberLimit": int(config["PageNumberLimit"]),
                "UserAgent": config["UserAgent"],
                "RequestDelay": float(config["RequestDelay"]),
            }
        except ValueError as e:
            raise ValueError(f"Invalid config values: {e}")

        #Store raw responses as {path:response}
        self.op_results: Dict[str, Any] = {}
        #Track visited URLs to prevent duplicate crawling
        self.visited_urls = set()
        #Track how many pages have been crawled
        self.page_count = int(0)
        #Tree creator instance to handle the tree structure
        self.tree_creator = DirectoryTreeCreator()


    def startCrawl(self):
        """
        Handles the initial request to the root node, sends the first HTTP request.
        Calls processResponse() to process the root node.
        """
        #Get the starting URL from the config
        self.tree_creator = DirectoryTreeCreator()
        curr_dir = self.config["TargetURL"]  
        try:
            #Make the first request to the root URL
            req = requests.get(curr_dir, headers={'User-Agent': self.config['UserAgent']})
            if req.status_code == 200:
                #First call to processResponse() happens here
                self.processResponse(curr_dir, req.text)
            else:
                print(f"[ERROR] Failed to access target URL: {req.status_code}")
        except Exception as e:
            print(f"[ERROR] Connection error: {e}")


    def processResponse(self, curr_dir: str, response:str, parent_node = None):
        """
        Executes the crawl and handles the HTTP response. Process:
        1. Stores the response.
        2. Creates a node for the current URL.
        3. If parent_node exists it appends current node as a child.
        4. Sends the parent-child relationship to the DirectoryTreeCreator.
        5. Extracts links and recursively processes them as children.

        Arguments:
        curr_dir (str): The current URL being processed.
        response (str): HTTP response content.
        parent_node (dict): Parent node, set to None when first initiating the crawl.

        Returns: None
        """
        #Skip already visited urls, prevents duplicate crawling
        if curr_dir in self.visited_urls:
            return
        #Print statement for testing purposes
        print(f"Currently crawling: {curr_dir}")

        #Store response in op_results (dict storing the crawled path and its response)
        self.op_results[curr_dir] = response
        #Add URL to visited urls
        self.visited_urls.add(curr_dir)
        #Update page count
        self.page_count += 1

        #Node represeting the current URL, path is the last part of the URL (ex. /search)
        node = {
            "url": curr_dir,
            "ip": socket.gethostbyname(curr_dir.split('/')[2]),
            "children": []
        }

        #If a parent node exists, add node to parent-child relationship (ensures every new URL crawled becomes part of the tree, linked to the parent node)
        if parent_node is not None:
            if node not in parent_node["children"]:
                parent_node["children"].append(node)

                parent = (parent_node["url"], parent_node["ip"])
                child = (node["url"], node["ip"])

                # Prevent duplicate edges in tree_creator
                if child not in self.tree_creator.tree.dir_tree.get(parent, []):
                    self.tree_creator.add_edge(parent, child)

        #End crawling if page limit is reached
        if self.page_count >= self.config['PageNumberLimit']:
            print("NOTE: Page limit has been reached, ending crawl.")
            return 
        
        #Extract only discovered valid links from the HTML content
        soup = BeautifulSoup(response, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        links = [link for link in links if not link.startswith("#")]
        links = [link for link in links if not ':' in link.split('/')]
        #Recursively crawl and process every discovered and valid link
        for link in links:
            #Convert relative URLs to absolute URLs
            next_url = urljoin(curr_dir, link)

            #Process links that have not been crawled yet and only if depth has not been exceeded
            if next_url not in self.visited_urls and len(self.visited_urls) < self.config['CrawlDepth']:
                #Avoid overloading the server by delaying between requests
                time.sleep(self.config['RequestDelay'] / 1000) #convert to secs

                try:
                    req = requests.get(next_url, headers={'User-Agent': self.config['UserAgent']})

                    #Recursively call processResponse() for the next URL, this creates a flowing parent-child relationship
                    if req.status_code == 200:
                        self.processResponse(next_url, req.text, node)
                    else:
                        #Indicate if HTTP response fails
                        print(f"NOTE: Failed to crawl {next_url}: {req.status_code}")
                except Exception as e:
                    #Handle network issues
                    print(f"Error: Failed to crawl {next_url}: {e}")
        
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
        self.op_results = {} #reset operation results
        self.visited_urls = set() #reset curr list of visited urls
        self.page_count = 0 #reset pages count
        self.tree_creator = DirectoryTreeCreator() #reset tree
        
    def getCrawlResults(self) -> list[str]:
        #Return a list of URLs that have been crawled
        #Sample usage (urls = crawler.getCrawlResults())
        return list(self.op_results.keys())
    
    def getTree(self):
        return self.visited_urls
    def getDefaultConfig(self):
        return self.default_config
