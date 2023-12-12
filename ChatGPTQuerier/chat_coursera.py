#! /usr/bin/env python3

import openai
import os
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
loader = JSONLoader(
    file_path='./chat_subtitles.json',
    jq_schema='.filler[].text',
    text_content=False)

docs = loader.load()
r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,
    separators=["\n\n", "\n", "\. ", " ", ""]
)
trans_docs = r_splitter.split_documents(docs)

# print(trans_docs)
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)
vectordb.add_documents(docs)

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever())
while True:
    question = input()
    result = qa_chain({"query": question})
    print(result["result"])