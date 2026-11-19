import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.index = None
        self.chunks = []

    def create_index(self, chunks):

        self.chunks = chunks

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        print("Creating embeddings...")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        print(
            f"Vector database created with {len(chunks)} chunks."
        )

    def search(self, query, top_k=4):

        if self.index is None:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        query_embedding = query_embedding.astype(
            "float32"
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index < len(self.chunks):

                result = self.chunks[index].copy()

                result["distance"] = float(distance)

                results.append(result)

        return results