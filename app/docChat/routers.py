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
