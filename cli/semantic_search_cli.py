#!/usr/bin/env python3

import argparse 
# 
# 
from lib.semantic_search import verify_model
# 
def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 
    subparsers.add_parser("verify", help="verifies that a pre-trained embedded model exists for semantic search")
    # 
    args = parser.parse_args()
    # 
    # 
    match args.command:
        case 'verify':
            print("Called verify")
            verify_model()
            print("completed verify?")
        case _:
            parser.print_help()

# 
if __name__ == "__main__":
    main()
