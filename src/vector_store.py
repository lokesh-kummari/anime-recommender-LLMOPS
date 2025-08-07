from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import csv_loader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from utils.custom_exception import CustomException
from utils.logger import logging
from typing import List, Dict
load_dotenv()

class VectorStoreBuilder:
    def __init__(self, csv_path: str, persist_dir: str = "chroma_db"):
        """
        Initializes the VectorStoreBuilder with the path to the CSV file and the directory to persist the vector store.
        :param csv_path: Path to the CSV file containing the data.
        :param persist_dir: Directory where the vector store will be persisted.
        """
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2",
        )
    def build_and_save_vectorstore(self):
        loader = csv_loader(
            file_path = self.csv_path,
            encoding='utf-8',
            error_bad_lines=False
        )
        data = loader.load()
        if not data:
            raise CustomException("No data found in the CSV file.", None)
        logging.info(f"Loaded {len(data)} documents from the CSV file.")
        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        texts = splitter.split_documents(data)
        logging.info(f"Split documents into {len(texts)} chunks.")
        
        db = Chroma.from_documents(
            texts=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        db.persist()
        logging.info(f"Vector store saved to {self.persist_dir}.")
        
    def load_vector_store(self) -> Chroma:
        """
        Loads the vector store from the specified directory.
        :return: An instance of the Chroma vector store.
        """
        if not os.path.exists(self.persist_dir):
            raise CustomException(f"Persist directory {self.persist_dir} does not exist.", None)
        logging.info(f"Loading vector store from {self.persist_dir}.")
        return Chroma(persist_directory=self.persist_dir, embedding=self.embeddings)