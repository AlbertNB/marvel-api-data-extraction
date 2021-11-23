from marvelConnector import MarvelConnector
import json
import os


if __name__ == "__main__":
    # Keys
    PUBLIC_KEY = os.environ['MARVEL_PUBLIC_KEY']
    PRIVATE_KEY = os.environ['MARVEL_PRIVATE_KEY']

    # Variables
    characters_id = [1009368,1009652] # Iron man e Thanos
    result_dataset = list()

    # Connector Class
    m = MarvelConnector(PUBLIC_KEY,PRIVATE_KEY)

    # Data Extraction
    for character_id in characters_id:
        character_dataset = m.get_stories_by_character_id(character_id)
        if character_dataset:
            result_dataset += character_dataset

    with open("dataset.json",'w') as file: 
        file.write(json.dumps(result_dataset))
