#!/usr/bin/env python3

import argparse 
# 
from lib.semantic_search import (
    embed_query_text,
    embed_text,
    semantic_search,
    verify_embeddings,
    verify_model, 
    )
# 
def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 
    subparsers.add_parser("verify", help="Verify that the embedded model is loaded")
    # 
    single_embed_parser = subparsers.add_parser("embed_text", help="Generate an embedding for a single text")
    single_embed_parser.add_argument("text", type=str, help="Text to embed")
    # 
    subparsers.add_parser("verify_embeddings", help="Verify embeddings for the movie dataset")
    # 
    embed_query_parser = subparsers.add_parser("embed_query", help="Generate an embedding for a search query")
    embed_query_parser.add_argument("query", type=str, help="Query to embed")
    # 
    search_parser = subparsers.add_parser("search", help="Search for movies using semantic search")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--limit", type=int, default=5, help="Number of results to return")
    #
    args = parser.parse_args()
    # 
    match args.command:
        case 'verify':
            verify_model()
        case 'embed_text':
            text = args.text
            embed_text(text)
        case 'verify_embeddings':
            verify_embeddings()
        case 'embed_query':
            query = args.query
            embed_query_text(query)
        case 'search':
            query = args.query
            limit = args.limit
            semantic_search(query, limit)
        case _:
            parser.print_help()

# 
if __name__ == "__main__":
    main()
