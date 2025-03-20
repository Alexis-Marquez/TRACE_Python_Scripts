from typing import Dict, Any
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

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

        #Store raw responses as {path:response}
        self.op_results: Dict[str, Any] = {}
        #Track visited URLs to prevent duplicate crawling
        self.visited_urls = set()
        #Track how many pages have been crawled
        self.page_count = 0
        #Tree creator instance to handle the tree structure
        self.tree_creator = DirectoryTreeCreator()


    def startCrawl(self):
        """
        Handles the initial request to the root node, sends the first HTTP request.
        Calls processResponse() to process the root node.
        """
        #Get the starting URL from the config
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


    def processResponse(self, curr_dir: str, response: str, parent_node = None):
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
            "path": curr_dir.split('/')[-1],
            "children": []
        }

        #If a parent node exists, add node to parent-child relationship (ensures every new URL crawled becomes part of the tree, linked to the parent node)
        if parent_node is not None:
            parent_node["children"].append(node)
            #Send node relationship to the tree creator using add_edge()
            parent = (parent_node["url"], parent_node["path"])
            child = (node["url"], node["path"])
            #Update the tree
            self.tree_creator.add_edge(parent, child)
        #If parent_node is None this is treated as the root node

        #End crawling if page limit is reached
        if self.page_count >= self.config['PageNumberLimit']:
            print("NOTE: Page limit has been reached, ending crawl.")
            return 
        
        #Extract only discovered valid links from the HTML content
        soup = BeautifulSoup(response, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]

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
    def getCrawlResults(self):
        pass
        #Return dictionary of crawled paths and responses
        #return self.op_results if self.op_results else {}
    def getTree(self):
        pass
    def getDefaultConfig(self):
        return self.default_config
