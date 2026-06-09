import argparse
from lib.rag import rag_command 
# 
def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieval Augmented Generation CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 
    rag_parser = subparsers.add_parser(
        "rag", help="Perform RAG (search + generate answer)"
    )
    rag_parser.add_argument("query", type=str, help="Search query for RAG")
    # 
    args = parser.parse_args()
    # 
    match args.command:
        case "rag":
            query = args.query
            results = rag_command(query)
            print("Search Results")
            for result in results["results"]:
                print(f"   - {result["title"]}")
            print("RAG Response")
            print(f"< {results["response"]} >")
        case _:
            parser.print_help()
    # 
# 
if __name__ == "__main__":
    main()