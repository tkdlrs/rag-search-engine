import json
import os
#
DEFAULT_SEARCH_LIMIT = 5
# 
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")
#  
def load_movies() -> list[dict]:
    with open(DATA_PATH, mode="r") as file:
        data = json.load(file)
    return data["movies"]
#
def load_stop_words() -> list[dict]:
    with open(STOPWORDS_PATH, mode="r")as file:
        data = file.read()
        return data.splitlines()
# 