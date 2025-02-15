from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
embedding_model = OpenAIEmbeddings(api_key=openai_api_key)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
vector_store = InMemoryVectorStore(embedding_model)
prompt = hub.pull("rlm/rag-prompt")

def get_llm():
    return llm

def get_splitter():
    return text_splitter

def get_embedding_model():
    return embedding_model

def get_vector_store():
    return vector_store

def get_prompt():
    return prompt
