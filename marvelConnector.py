import hashlib
import time
import json
from typing import Optional
import requests


PAGE_LIMIT = 100 # Max allowed for Marvel API

class MarvelConnector():

    def __init__(self,public_key,private_key) -> None:
        # Constructor Method
        self.public_key = public_key
        self.private_key = private_key

    def get_hash(self,ts_str) -> str:
        # Get Hash for Marvel API
        return hashlib.md5(bytes(ts_str+self.private_key+self.public_key, encoding='utf8')).hexdigest()

    def get_stories_by_character_id(self,character_id) -> Optional[list]:
        """It fetches lists of comic stories featuring a specific character.

        Input
        ----------
        character_id : int | str
            Character ID to retrives stories in witch it participates
        
        Output
        ----------
        results : list optional
            list of stories in witch the character participates
        """
        print("Starting Extraction for Character ID {}".format(character_id))

        # Variables
        url = "https://gateway.marvel.com/v1/public/characters/{character_id}/stories?ts={ts}&apikey={public_key}&hash={hash}&limit={limit}&offset={offset}"
        offset = 0
        total = 0
        init = True 
        results = list()
        
        # Pagination Handler
        while offset < total or init:
            init = False

            # URL Preparation
            ts = str(time.time())
            hash = self.get_hash(ts)
            url_formated = url.format(character_id = character_id,
                                      ts = ts,
                                      public_key = self.public_key,
                                      hash = hash,
                                      limit = PAGE_LIMIT,
                                      offset = offset
                                    )
                                    
            # API Request
            try:
                res = requests.get(url_formated)
                if res.status_code == 200:
                    response_data = json.loads(res.text)
                    offset += response_data['data']['count']
                    total = response_data['data']['total']
                    results += response_data['data']['results']
                    print("Character Id {} -> {}/{} Stories".format(character_id,offset,total))
                else:
                    print("Unexpected response from API, code: ",res.status_code)
                    print(res.text)
                    return None
            # Exceptions Handles
            except requests.exceptions.HTTPError as http_error:
                print("HTTP error has occurred: ",http_error)
                return None
            except requests.exceptions.ConnectionError as connection_error:
                print("Connection error has occurred: ",connection_error)
                return None
            except requests.exceptions.Timeout as timeout_error:
                print("Timeout error has occurred: ",timeout_error)
                return None
            except requests.exceptions.RequestException as general_exception:
                print("Some unidentified error has occurred on API request: ",general_exception)
                return None

        return results
