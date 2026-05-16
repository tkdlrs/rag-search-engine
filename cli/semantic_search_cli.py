#!/usr/bin/env python3

import argparse 
# 
from lib.semantic_search import (verify_model, embed_text, verify_embeddings)
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
            embed_text(query)
        case _:
            parser.print_help()

# 
if __name__ == "__main__":
    main()
