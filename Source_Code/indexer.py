from sentence_transformers import SentenceTransformer
from chunker import chunk_documents
from pathlib import Path
import chromadb

folder_path = Path("../Raw_text")
embeddings_folder = Path("../Vector_Embeddings")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-V2")

chunks_list= chunk_documents(folder_path)

sentences = [chunk["raw_chunk"] for chunk in chunks_list]

embeddings = model.encode(sentences)

chunk_ids = []
docs = []
extra = []

client = chromadb.PersistentClient(embeddings_folder)
try:
    client.delete_collection(name="calcom_helpdesk")
except Exception:
    pass

collection = client.create_collection(name="calcom_helpdesk")

for chunk in chunks_list:
    chunk_ids.append(chunk["file_name"] + "_" + str(chunk["chunk_index"]))
    docs.append(chunk["raw_chunk"])
    extra.append({"file_name": chunk["file_name"], "chunk_index": chunk["chunk_index"]})


collection.add(
    ids = chunk_ids,
    embeddings = embeddings,
    documents = docs,
    metadatas = extra
)

print(collection.count())

# print(embeddings.shape)