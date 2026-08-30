import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_groq import ChatGroq

load_dotenv()


def build_index():
    pages = PyPDFLoader("docs/resume.pdf").load()
    print(f"Loaded {len(pages)} page(s)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(pages)
    print(f"Split into {len(chunks)} chunk(s)")

    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local("index")
    print("Index saved to ./index/")

# build_index()

PROMPT = """You answer questions about ONE specific document.

RULES
1. Use ONLY the CONTEXT below. No outside knowledge.
2. If the CONTEXT does not contain the answer, your answer must be exactly:
   NOT IN DOCUMENT
3. Never guess or fill gaps with what is "usually" true.

CONTEXT
{context}

QUESTION
{question}

ANSWER"""


def ask(question):
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    store = FAISS.load_local("index", embeddings,
                             allow_dangerous_deserialization=True)

    hits = store.similarity_search(question, k=4)
    context = "\n\n".join(h.page_content for h in hits)

    llm = ChatGroq(model=os.getenv("GROQ_MODEL"), temperature=0)
    answer = llm.invoke(PROMPT.format(context=context, question=question))

    print("Q:", question)
    print("A:", answer.content)

def ask_plain(question):
    llm = ChatGroq(model=os.getenv("GROQ_MODEL"), temperature=0)
    answer = llm.invoke(question)

    print("Q (no document):", question)
    print("A:", answer.content)
ask("List every bachelor thesis supervised, with the student year ranges.")
