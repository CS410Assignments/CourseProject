#! /usr/bin/env python3

import openai
import os
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain import Query


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ[""]

loader = JSONLoader(
    file_path='./chat_subtitles.json',
    jq_schema='.introduction-to-text-mining-and-analytics[].content',
    text_content=False)

docs = loader.load()
trans_docs = r_splitter.split_documents(docs)

# print(trans_docs)

from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.retrievers.self_query.base import SelfQueryRetriever


from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)

# qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
while True:
    question = input()
    docs = retriever.get_relevant_documents(question)
    for d in docs:
        print(d.metadata)
    # print(len(docs))
    # print(docs)
    # result = qa_chain({"query": question})
    # print(result["result"])