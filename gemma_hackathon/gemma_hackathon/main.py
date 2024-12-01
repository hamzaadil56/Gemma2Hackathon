import os
import pandas as pd
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


# Print the current working directory
# print("Current working directory:", os.getcwd())

# # Create an absolute file path
# file_path = os.path.abspath("./gemma_hackathon/ExcelExtract_AnonymisedDealFlowList.csv")
# print("Absolute file path:", file_path)

# # Check if the file exists
# print("File exists:", os.path.exists(file_path))

llm = ChatGroq(model="gemma2-9b-it")

file_path = "./gemma_hackathon/Mandated.csv"

loader = CSVLoader(file_path=file_path)
data = loader.load_and_split()

vectorstore = Chroma.from_documents(
    documents=data,
    embedding=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"),
)
retriever = vectorstore.as_retriever()

template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, use LLM knowledge to answer the question.
        {context}

        Question: {question}

        Helpful Answer:"""

prompt = PromptTemplate.from_template(template)
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
# responses = []
stream_response = rag_chain.invoke(
    "Which deal has the highest amount in USD and has the status of Mandated?")
# print(data)
print(stream_response)
