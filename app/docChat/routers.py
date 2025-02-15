from fastapi import APIRouter, UploadFile, File
# from .schemas import ChatRequest, ChatResponse
# from .services import chat_with_doc, upload_doc

router = APIRouter()

# @router.post("/chat", response_model=ChatResponse)
# def chat_endpoint(request: ChatRequest):
#     # return chat_with_doc(request.query)

# @router.post("/upload")
# def upload_file(file: UploadFile = File(...)):
#     return upload_doc(file)

@router.get("/status")
def health_check():
    return {"status": "docChat API is running"}


# ===================
# For testing the logic
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
