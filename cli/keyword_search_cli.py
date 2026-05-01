import argparse 
import json
import os
from pathlib import Path

# 
def get_data():
    try:
        data_file = Path(os.curdir) / "data" / "movies.json"
        with open(data_file, mode="r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: file not found...")
    except Exception as e:
        print(f"Error of '{e}' occurred")
    finally:
        file.close()
# 
def keyword_search(search_term):
    movies_data = get_data()
    all_matches = list()
    # 
    for film in movies_data["movies"]:
        title = film["title"]
        if search_term in title:
            all_matches.append(film)
    # sort by ascending id
    sorted_film_results = all_matches.sort(key=lambda x: (x['id']))
    return all_matches[:5]
# 
def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 
    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")
    # 
    args = parser.parse_args()
    # 
    match args.command:
        case "search":
            # print the search query here
            search_for = args.query
            print(f"Searching for: {search_for}")
            matches = keyword_search(search_for)
            for i in range(len(matches)):
                print(f"{i + 1}. {matches[i]["title"]}")
            pass
        case _:
            parser.print_help()

            # 
if __name__ == "__main__":
    main()


