import random
from typing import Dict, Any
import json

from backend.utils import send_get_request, send_post_request, send_put_request

class Fuzzer:
    config = dict()
    default_config =  {
            "TargetURL": "www.example.com",
            "HTTPMethod": "GET",
            "Cookies": [],
            "HideStatusCode": [],
            "ShowOnlyStatusCode": [],
            "FilterContentLength": 1000,
            "PageLimit": 1000,
            "WordList": ["username", "password", "search", "admin"]
        }
    def __init__(self, config=None):
        if config is None:
            self.reset()
            return
        elif len(config) == 0:
            self.reset()
            return
        for key in self.default_config.keys():
            if key not in config:
                print(key)
                raise KeyError("Invalid config dictionary")
        try:
            self.config = {
                "TargetURL": config["TargetURL"],
                "HTTPMethod": config["HTTPMethod"],
                "Cookies": config["Cookies"],
                "HideStatusCode": config["HideStatusCode"],
                "ShowOnlyStatusCode": config["ShowOnlyStatusCode"],
                "FilterContentLength": int(config["FilterContentLength"]),
                "PageLimit": int(config["PageLimit"]),
                "WordList": config["WordList"]
            }
        except ValueError as e:
            raise ValueError(f"Invalid config values: {e}")
         #Store raw responses as {path:response}
        self.op_results: Dict[str, Any] = {}
        #Track visited URLs to prevent duplicate crawling
        self.visited_urls = set()
        #Track how many pages have been crawled
        self.page_count = int(0)

    def start(self):
        if self.config['HTTPMethod'] == "GET":
            self.start_fuzzer_get()
        elif self.config['HTTPMethod'] == "POST":
            self.start_fuzzer_post()
        elif self.config['HTTPMethod'] == "PUT":
            self.start_fuzzer_put()
       

    def generate_fuzzing_params(self, max_length: int = 100, char_start: int = 32, char_range: int = 32) ->str:
        
        string_length = random.randrange(0, max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(random.randrange(char_start, char_start+char_range))
        return out

    def start_fuzzer_get(self):
        fuzzed_string = self.generate_fuzzing_params()  
        self.fuzz("", "GET", fuzzed_string)
        for i in range(0, self.config['PageLimit']):
            for word in self.config['WordList']: 
                fuzzed_string = self.generate_fuzzing_params()  
                self.fuzz(word, "GET" , fuzzed_string)

    def fuzz(self, word, mode, fuzzed_string=None, json_string=None):
        
        curr_dir = self.config['TargetURL']+word+fuzzed_string
        # www.google.com/akjlsdhf www.google.com/search/alkdsjfh
        if mode == "GET":
            response, status_code = send_get_request(curr_dir, 0, self.page_count, self.config['PageLimit'], "", self.config['Cookies'])
        elif mode =="POST":
            response, status_code = send_post_request(curr_dir, 0, json_string, self.page_count, self.config['PageLimit'], "", self.config['Cookies'])
        elif mode == "PUT":
            response, status_code = send_put_request(curr_dir, 0, json_string, self.page_count, self.config['PageLimit'], "", self.config['Cookies'])
        else:
            raise TypeError("Invalid mode")
        self.op_results[curr_dir] = response, status_code
        self.visited_urls.add(curr_dir)
        self.page_count+=1

    def start_fuzzer_put(self):
         for i in range(0, self.config['PageLimit']):
            for word in self.config['WordList']: 
                fuzzed_string = self.generate_fuzzing_params()   
                json_string = {word:fuzzed_string} 
                json_string = json.dumps(json_string)
                self.fuzz(word, "PUT", fuzzed_string, json_string)

    def start_fuzzer_post(self):
        for i in range(0, self.config['PageLimit']):
            for word in self.config['WordList']: 
                fuzzed_string = self.generate_fuzzing_params()   
                json_string = {word:fuzzed_string} 
                json_string = json.dumps(json_string)
                self.fuzz(word, "POST", fuzzed_string, json_string)

    def get_data(self):
        return self.op_results
    
    def get_links(self):
        return self.visited_urls
            
    def reset(self):
        self.config = None
        self.config = self.default_config
        self.op_results = {} #reset operation results
        self.visited_urls = set() #reset curr list of visited urls
        self.page_count = 0 #reset pages count