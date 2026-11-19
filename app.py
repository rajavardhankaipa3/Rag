import streamlit as st

from rag import RAGSystem


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Multi-PDF RAG Chatbot",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title(
    "📚 Multi-PDF RAG Chatbot"
)

st.write(
    "Upload multiple PDF documents and ask "
    "questions across all of them using "
    "FAISS + Sentence Transformers + Groq."
)


# ==========================================
# CREATE RAG SYSTEM
# ==========================================

if "rag_system" not in st.session_state:

    st.session_state.rag_system = RAGSystem()


rag = st.session_state.rag_system


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header(
        "📄 Upload PDF Documents"
    )

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )


    # --------------------------------------
    # Show uploaded files
    # --------------------------------------

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} PDF(s) selected"
        )

        st.write(
            "Selected documents:"
        )

        for pdf in uploaded_files:

            st.write(
                f"📄 {pdf.name}"
            )


    # --------------------------------------
    # Process button
    # --------------------------------------

    if uploaded_files:

        if st.button(
            "🔍 Process All PDFs",
            use_container_width=True
        ):

            with st.spinner(
                "Processing all PDFs..."
            ):

                try:

                    result = (
                        rag.process_pdfs(
                            uploaded_files
                        )
                    )

                    st.session_state.pdf_processed = True

                    st.session_state.pdf_count = (
                        result["pdf_count"]
                    )

                    st.session_state.chunk_count = (
                        result["chunk_count"]
                    )

                    st.success(
                        "All PDFs processed successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


# ==========================================
# SHOW PROCESSING INFORMATION
# ==========================================

if st.session_state.get(
    "pdf_processed",
    False
):

    st.success(
        f"Processed "
        f"{st.session_state.pdf_count} PDFs "
        f"with "
        f"{st.session_state.chunk_count} "
        f"text chunks."
    )


# ==========================================
# QUESTION AREA
# ==========================================

if st.session_state.get(
    "pdf_processed",
    False
):

    st.subheader(
        "💬 Ask Questions"
    )

    question = st.text_input(
        "Enter your question",
        placeholder=(
            "Example: What is the main "
            "objective of these documents?"
        )
    )


    if st.button(
        "🚀 Ask Groq",
        type="primary"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching documents and "
                "generating answer..."
            ):

                try:

                    answer, results = (
                        rag.answer_question(
                            question
                        )
                    )


                    # ======================
                    # ANSWER
                    # ======================

                    st.subheader(
                        "🤖 Answer"
                    )

                    st.write(
                        answer
                    )


                    # ======================
                    # SOURCES
                    # ======================

                    st.subheader(
                        "📖 Sources"
                    )

                    for i, result in enumerate(
                        results,
                        start=1
                    ):

                        filename = (
                            result["filename"]
                        )

                        page = (
                            result["page"]
                        )

                        score = (
                            result["score"]
                        )

                        with st.expander(
                            f"Source {i}: "
                            f"{filename} "
                            f"(Page {page})"
                        ):

                            st.write(
                                result["text"]
                            )

                            st.caption(
                                f"Similarity score: "
                                f"{score:.4f}"
                            )

                except Exception as e:

                    st.error(
                        f"Error while answering: "
                        f"{e}"
                    )


else:

    st.info(
        "👈 Upload one or more PDFs "
        "from the sidebar to begin."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Multi-PDF RAG • "
    "PyMuPDF • "
    "Sentence Transformers • "
    "FAISS • "
    "Groq"
)