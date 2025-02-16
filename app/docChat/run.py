# ===================
# Dummy python for changing the logic
# ==================

from services import chat_with_doc
from upload import load_and_embed_pdf
import os

def run_cli():
    print("Loading and indexing PDF...")

    base_dir = os.getcwd()
    file_path = os.path.join(base_dir,"app","docChat","attention.pdf")
    load_and_embed_pdf(file_path)

    while True:
        question = input("User >> ")
        if question.lower() in ["exit", "quit", "clear"]:
            break

        result = chat_with_doc(question)
        print(f"Chat >> {result['answer']}")


if __name__ == "__main__":
    run_cli()
