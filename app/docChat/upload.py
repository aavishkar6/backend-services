from dependencies import get_splitter, get_vector_store
from langchain_community.document_loaders import PyPDFLoader
import asyncio


async def load_document_async(path: str):
    loader = PyPDFLoader(path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

def load_and_embed_pdf(path: str):
    pages = asyncio.run(load_document_async(path))
    splitter = get_splitter()
    vector_store = get_vector_store()

    chunks = splitter.split_documents(pages)
    vector_store.add_documents(chunks)
