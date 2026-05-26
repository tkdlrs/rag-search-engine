import argparse 
# 
from lib.hybrid_search import normalize_command
#
def main() -> None: 
    parser = argparse.ArgumentParser(description="Hybrid Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    #
    normalize_parser = subparsers.add_parser("normalize", help="normalize a list of args with Min-Max Normalization")
    normalize_parser.add_argument("nargs",  nargs="*", help="list of values to normalize")
    # 
    args = parser.parse_args()
    #
    match args.command:
        case "normalize":
            values_list = [float(x) for x in args.nargs]
            print("values_list", values_list)
            results = normalize_command(values_list)
            if len(results) == 0:
                return
            for score in results:
                print(f"* {score:.4f}")
        
        case _:
            parser.print_help()
    #
if __name__ == "__main__":
    main()

# 
