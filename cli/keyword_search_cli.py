#!/usr/bin/env python3
# 
import argparse 
# 
from lib.keyword_search import search_command
# 
from lib.inverted_index import build_command, tf_command
# 
def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 
    subparsers.add_parser("build", help="Build the inverted index")
    # 
    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")
    # 
    term_freq = subparsers.add_parser("tf", help="Get a term frequency for a given term")
    term_freq.add_argument("doc_id", type=str, help="Document ID")
    term_freq.add_argument("term", type=str, help="Term")
    # 
    args = parser.parse_args()
    # 
    match args.command:
        case "build":
            print("Building inverted index...")
            build_command()           
            print("Inverted index build successfully.")
            # 
        case "search":
            # print the search query here
            search_for = args.query
            print(f"Searching for: {search_for}")
            results = search_command(search_for)
            for i, res in enumerate(results, 1):
                print(f"{i}. ({res['id']}) {res['title']}")
            # 
        case "tf":
            doc_id = args.doc_id
            term = args.term
            print(f"looking up term frequency for \"{term}\" in Document with id number: {doc_id}")
            tf_command(doc_id, term)
            # 
        case _:
            parser.print_help()

# 
if __name__ == "__main__":
    main()


