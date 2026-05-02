#!/usr/bin/env python3

import argparse 

from lib.keyword_search import search_command
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
            results = search_command(search_for)
            for i, res in enumerate(results, 1):
                print(f"{i}. {res['title']}")
            pass
        case _:
            parser.print_help()

# 
if __name__ == "__main__":
    main()


