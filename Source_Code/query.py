import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os
import json

embeddings_folder = Path("../Vector_Embeddings")
chroma_client = chromadb.PersistentClient(embeddings_folder)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-V2")
load_dotenv(override = True)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
collection = chroma_client.get_collection(name="calcom_helpdesk")

def get_answer(query):

    encoded_query = model.encode(query)

    results = collection.query(
        query_embeddings = encoded_query,
        n_results = 3
        )
    
    sources = [chunk['file_url'] for chunk in results['metadatas'][0]]
        
    file_headings = [chunk['file_heading'] for chunk in results['metadatas'][0]]
    
    response = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content":f"""You are a helpful support assistant for Cal.com.
                            Answer the user's question using ONLY the context below.
                            If the answer is not in the context, say "I don't have information about that.
                            Context:
                            [{"\n\n".join(results["documents"][0])}]
                            """ 
            },
            {
                "role":"user",
                "content":f"{query}"
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    return({'answer': response.choices[0].message.content, 'sources': sources, 'file_headings': file_headings})