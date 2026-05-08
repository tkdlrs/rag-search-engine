#!/usr/bin/env python3
# 
import argparse 
# 
from lib.keyword_search import search_command
# 
from lib.inverted_index import (
    build_command, 
    tf_command, 
    idf_command,
    tfidf_command,
    bm25_idf_command
)
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
    tf_parser = subparsers.add_parser("tf", help="Get a term frequency for a given document ID and term")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to get frequency for")
    # 
    idf_parser = subparsers.add_parser("idf", help="Get inverse document frequency for a given term")
    idf_parser.add_argument("term", type=str, help="Term to get IDF for" )
    # 
    tf_idf_parser = subparsers.add_parser("tfidf", help="Get TF-IDF score for a given document ID and term") 
    tf_idf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_idf_parser.add_argument("term", type=str, help="Term to get TF-IDF score for")
    # 
    bm25_idf_parser = subparsers.add_parser("bm25idf", help="Get BM25 IDF score for a given term")
    bm25_idf_parser.add_argument("term", type=str, help="Term to get BM25 IDF score for")
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
            tf = tf_command(doc_id, term)
            print(f"Term frequency of '{term}' in document '{doc_id}': {tf}")
            # 
        case "idf":
            term = args.term
            idf = idf_command(term)
            print(f"Inverse document frequency of '{term}': {idf:.2f}")
            #
        case "tfidf":
            doc_id = args.doc_id
            term = args.term
            tf_idf = tfidf_command(doc_id, term)
            print(f"TF-IDF score of '{term}' in document '{doc_id}': {tf_idf:.2f}")
            # 
        case "bm25idf":
            term = args.term
            bm25_idf = bm25_idf_command(term)
            print(f"BM25 IDF score of '{term}': {bm25_idf:.2f}")
            # 
        case _:
            parser.print_help()

# 
if __name__ == "__main__":
    main()


