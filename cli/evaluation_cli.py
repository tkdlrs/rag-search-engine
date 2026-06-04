import argparse
# 
from lib.search_utils import load_golden_dataset
from lib.hybrid_search import rrf_search_command

# 
def main() -> None:
    parser = argparse.ArgumentParser(description="Search Evaluation CLI")
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of results to evaluate (k for precision@k, recall@k)",
    )
    # 
    args = parser.parse_args()
    limit = args.limit 

    #
    golden_dataset = load_golden_dataset()
    # 
    print(f"k={limit}")
    for test_case in golden_dataset['test_cases']:
        print(f"- Query: {test_case['query']}")
        result = rrf_search_command( test_case['query'], 60, limit=limit)
        retrieved_titles = ""
        for i, res in enumerate(result['results'], 1):
            if i == len(result['results']):
                retrieved_titles += f"{res['title']}"
            else:
                retrieved_titles += f"{res['title']}, "
        # 
        # print(f" wtc is result? {result}")
        print(f"   - Precision@{limit}: { ( len(test_case['relevant_docs']) / len(result['results']) ):.4f}")
        print(f"   - Retrieved: {retrieved_titles}")
        print(f"   - Relevant: {", ".join(test_case['relevant_docs'])}")
        
    
# 
if __name__ == "__main__":
    main()
# 
