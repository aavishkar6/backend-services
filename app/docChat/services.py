import asyncio
from typing_extensions import TypedDict, List
from langchain_core.documents import Document
from dependencies import get_vector_store, get_llm, get_prompt
from langgraph.graph import StateGraph, START

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieval(state: State):
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(state["question"])
    return {"context": docs}

def generation(state: State):
    llm = get_llm()
    prompt = get_prompt()
    docs_content = "\n\n".join([doc.page_content for doc in state["context"]])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieval, generation])
graph_builder.add_edge(START, "retrieval")
graph = graph_builder.compile()

def chat_with_doc(question: str):
    return graph.invoke({"question": question})
