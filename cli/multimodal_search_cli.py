import argparse
import os
# 
from lib.multimodal_search import verify_image_embedding
#  
#  
def main() -> None:
    parser = argparse.ArgumentParser(description="Image + text -> rewritten query")
    # 
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 
    verify_image_parser = subparsers.add_parser("verify_image_embedding", help="Verify that the embedded model is loaded")
    verify_image_parser.add_argument("image", type=str, help="Path to image file")
    # 
    args = parser.parse_args()
    # 
    #
    match args.command:
        case 'verify_image_embedding':
            if not os.path.exists(args.image):
                raise FileNotFoundError(f"Image file not found: {args.image}")
            verify_image_embedding(args.image)
        # 
        case _:
            parser.print_help()
   #
# 
if __name__ == "__main__":
    main()
    