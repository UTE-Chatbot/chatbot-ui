import os
import faiss
import ollama
import warnings
import numpy as np
import pandas as pd
import google.generativeai as genai
from sentence_transformers import SentenceTransformer



warnings.filterwarnings("ignore")


GOOGLE_API_KEY = "AIzaSyBNMDBIw8EgbJdVSR8_io747BJn-JssUiU"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name = "gemini-1.5-pro")
model

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

    #print(context)
    print('retrieved_context: \n: ', context)
    print('\n\n\ --- \n\n')
    
    prompt = f"Đây là một trợ lí tư vấn tuyển sinh cho trường Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE), trả lời các câu hỏi về ngành nghề, thắc mắc về trường cho học sinh, trả lời đầy đủ ý, chính xác, logic, ngắn gọn \Câu hỏi: {query}\nCâu trả lời:"
    #response = ollama.chat(model='mistral', messages=[{"role": "user", "content": prompt}])
    #return response["message"]["content"]

    response = model.generate_content(prompt)
    return response.text

