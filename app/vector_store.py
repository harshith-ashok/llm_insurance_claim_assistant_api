import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index_path = "storage/index.faiss"
chunks = []
files = []

if os.path.exists(index_path):
    index = faiss.read_index(index_path)
    chunks = np.load("storage/chunks.npy", allow_pickle=True).tolist()
    files = np.load("storage/files.npy", allow_pickle=True).tolist()
else:
    index = faiss.IndexFlatL2(384)


def add_to_vector_store(text, filename):
    global index, chunks, files
    lines = [line for line in text.split("\n") if len(line) > 50]
    embeddings = model.encode(lines)
    index.add(np.array(embeddings, dtype="float32"))
    chunks.extend(lines)
    files.extend([filename] * len(lines))
    faiss.write_index(index, index_path)
    np.save("storage/chunks.npy", np.array(chunks))
    np.save("storage/files.npy", np.array(files))


def retrieve_relevant_chunks(csv_string, k=5):
    embedding = model.encode([csv_string])[0].astype("float32")
    D, I = index.search(np.array([embedding]), k)
    return [{"text": chunks[i], "source": files[i]} for i in I[0]]
