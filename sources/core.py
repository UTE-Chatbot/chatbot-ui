import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import ollama

import warnings
warnings.filterwarnings("ignore")
import os

df = pd.read_csv("./sources/update_data.csv", header=None, names=["chunk"])


EMBEDDING_MODEL = "BAAI/bge-m3"
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
INDEX_FILE = "./sources/faiss_index_v1.bin"

if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
    print("FAISS index loaded successfully.")
else:
    print("Embedding again")
    embeddings = np.array(embedding_model.encode(df["chunk"].tolist(), normalize_embeddings=True))
    d, n = embeddings.shape
    index = faiss.IndexFlatIP(n)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)
    print("New FAISS index created and saved.")

def retrieve_similar(query, top_k=3):
    query_embedding = embedding_model.encode([query], normalize_embeddings=True)
    _, indices = index.search(query_embedding, top_k)
    return [df.iloc[i]["chunk"] for i in indices[0]]

def generate_answer(query):
    retrieved_docs = retrieve_similar(query, 4)

    context = "\n".join( retrieved_docs)

    print(context)
    #print('retrieved_context: \n: ', context)
    #print('\n\n\ --- \n\n')
    
    prompt = f"\Câu hỏi: {query}\nCâu trả lời:"
    response = ollama.chat(model='hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF', messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

