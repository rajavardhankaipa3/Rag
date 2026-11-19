import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

from pdf_processor import (
    extract_text_from_pdf,
    create_chunks
)

from grok_api import ask_grok


class RAGSystem:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.chunks = []

        self.index = None

        self.pdf_names = []


    def process_pdfs(self, pdf_files):

        """
        Process multiple PDFs.
        """

        all_chunks = []

        self.pdf_names = []

        for pdf_file in pdf_files:

            filename = pdf_file.name

            print(
                f"Processing: {filename}"
            )

            # Extract text
            pages = extract_text_from_pdf(
                pdf_file
            )

            if not pages:

                continue

            # Create chunks
            chunks = create_chunks(
                pages,
                filename
            )

            all_chunks.extend(chunks)

            self.pdf_names.append(
                filename
            )

        if not all_chunks:

            raise ValueError(
                "No readable text was found "
                "in the uploaded PDFs."
            )

        # Store chunks
        self.chunks = all_chunks

        # Extract text
        texts = [
            chunk["text"]
            for chunk in self.chunks
        ]

        print(
            f"Creating embeddings for "
            f"{len(texts)} chunks..."
        )

        # Create embeddings
        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        embeddings = embeddings.astype(
            "float32"
        )

        # Normalize
        faiss.normalize_L2(
            embeddings
        )

        # Create FAISS index
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        # Add vectors
        self.index.add(
            embeddings
        )

        return {
            "pdf_count": len(self.pdf_names),
            "chunk_count": len(self.chunks)
        }


    def search(
        self,
        question,
        top_k=5
    ):

        if self.index is None:

            raise ValueError(
                "Please upload and process PDFs first."
            )

        # Question embedding
        query_embedding = (
            self.embedding_model.encode(
                [question],
                convert_to_numpy=True
            )
        )

        query_embedding = query_embedding.astype(
            "float32"
        )

        # Normalize
        faiss.normalize_L2(
            query_embedding
        )

        # Search
        scores, indices = self.index.search(
            query_embedding,
            min(
                top_k,
                len(self.chunks)
            )
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            result = self.chunks[index].copy()

            result["score"] = float(
                score
            )

            results.append(result)

        return results


    def answer_question(
        self,
        question,
        top_k=5
    ):

        results = self.search(
            question,
            top_k
        )

        # Build context
        context_parts = []

        for result in results:

            context_parts.append(
                f"""
SOURCE FILE: {result['filename']}
PAGE: {result['page']}

CONTENT:
{result['text']}
"""
            )

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are a document question-answering assistant.

The user uploaded multiple PDF documents.

Use ONLY the information provided in the
DOCUMENT CONTEXT below.

If the answer is found in the context,
answer clearly and accurately.

If the answer is not present in the context,
say:

"I could not find this information in the uploaded documents."

When possible, mention which PDF and page
contains the information.

DOCUMENT CONTEXT
================

{context}

================

QUESTION
========

{question}

ANSWER:
"""

        answer = ask_grok(prompt)

        return answer, results