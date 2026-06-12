import os
import argparse
import mimetypes
# 
from dotenv import load_dotenv
# 
from google import genai
from google.genai import types 
# 
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")
#
client = genai.Client(api_key=api_key)
model = "gemma-4-31b-it"
#  
def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieval Augmented Generation CLI")
    # subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # 
    parser.add_argument("--query", type=str, help="A text query to rewrite based on the image")
    parser.add_argument("--image", type=str, help="The path to an image file")
    # 
    args = parser.parse_args()
    # Determine mime 
    mime, _ = mimetypes.guess_type(args.image)
    mime = mime or "image/jpeg"
    # open and read image in binary and read 
    with open(args.image, mode="rb") as file:
        image_data = file.read()
    # 
    system_prompt = f"""Given the included image and text query, rewrite the text query to improve search results from a movie database. Make sure to:
    - Synthesize visual and textual information
    - Focus on movie-specific details (actors, scenes, style, etc.)
    - Return only the rewritten query, without any additional commentary"""
    # 
    parts = [ system_prompt, 
             types.Part.from_bytes(data=image_data, mime_type=mime), 
             args.query.strip(),
            ]
    # 
    response = client.models.generate_content(model=model, contents=parts)
    # 
    print(f"Rewritten query: {response.text.strip()}")
    if response.usage_metadata is not None:
        print(f"Total tokens: {response.usage_metadata.total_token_count}")
    

    # match args.command:
    #     case "rag":
    #         result = rag_command(args.query)
    #         print("Search Results:")
    #         for document in result["search_results"]:
    #             print(f"   - {document["title"]}")
    #         print()
    #         print("RAG Response:")
    #         print(result["answer"])
    #     case _:
    #         parser.print_help()
    #
# 
if __name__ == "__main__":
    main()