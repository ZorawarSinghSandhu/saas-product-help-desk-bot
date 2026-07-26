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
    
    # query = "What is the refund policy for annual plans?"

    encoded_query = model.encode(query)

    results = collection.query(
        query_embeddings = encoded_query,
        n_results = 3
        )

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

    return(response.choices[0].message.content)

query = "What is the refund policy for annual plans?"

answer = get_answer(query)

print(answer)