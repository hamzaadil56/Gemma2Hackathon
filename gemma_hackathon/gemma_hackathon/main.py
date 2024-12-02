# import os
# import pandas as pd
# from langchain_community.document_loaders import UnstructuredExcelLoader
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS

# from dotenv import load_dotenv
# load_dotenv()


# # Print the current working directory
# # print("Current working directory:", os.getcwd())

# # # Create an absolute file path
# # file_path = os.path.abspath("./gemma_hackathon/ExcelExtract_AnonymisedDealFlowList.csv")
# # print("Absolute file path:", file_path)

# # # Check if the file exists
# # print("File exists:", os.path.exists(file_path))

# llm = ChatOpenAI(model="gpt-4o-mini")

# file_path = "./gemma_hackathon/Mandated.csv"

# loader = CSVLoader(file_path=file_path)
# data = loader.load_and_split()

# vectorstore = FAISS.from_documents(data, OpenAIEmbeddings())
# retriever = vectorstore.as_retriever()
# print(retriever)

# template = """Use the following pieces of context to answer the question at the end.
#         If you don't know the answer, just say "I don't know".
#         {context}

#         Question: {question}

#         Helpful Answer:"""

# prompt = PromptTemplate.from_template(template)
# rag_chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )
# # responses = []
# stream_response = rag_chain.invoke(
#     "Which deal has the highest amount with status Mandated?")
# # print(data)
# print(stream_response)


import os
import pandas as pd
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()


def perform_rag_query(file_path, query, model="gemma2-9b-it", embedding_model="sentence-transformers/all-mpnet-base-v2"):
    """
    Perform Retrieval-Augmented Generation (RAG) on a CSV file.

    Args:
        file_path (str): Path to the CSV file to be processed
        query (str): The question to be answered
        model (str, optional): Groq LLM model to use. Defaults to "gemma2-9b-it"
        embedding_model (str, optional): Embedding model to use. Defaults to "sentence-transformers/all-mpnet-base-v2"

    Returns:
        str: The generated response to the query
    """
    # Initialize LLM
    llm = ChatGroq(model=model)

    # Load CSV data
    loader = CSVLoader(file_path=file_path)
    data = loader.load_and_split()

    # Create vector store
    vectorstore = FAISS.from_documents(
        data, HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))
    retriever = vectorstore.as_retriever()

    # Define RAG template
    template = """Use the following pieces of context to answer the question at the end.
            If you don't know the answer, use LLM knowledge to answer the question.
            {context}

            Question: {question}

            Helpful Answer:"""

    # Create RAG chain
    prompt = PromptTemplate.from_template(template)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Invoke the RAG chain and return the response
    return rag_chain.invoke(query)


# Example usage

# file_path = "./gemma_hackathon/AllStatus.csv"
# query = "Which deal has the highest amount in USD and has the status of Mandated?"

# response = perform_rag_query(file_path, query)
# print(response)
