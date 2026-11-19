import fitz


def extract_text_from_pdf(pdf_file):
    """
    Extract text from one PDF.
    """

    pdf_bytes = pdf_file.read()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        if text.strip():

            pages.append(
                {
                    "page": page_number + 1,
                    "text": text
                }
            )

    document.close()

    return pages


def split_text(
    text,
    chunk_size=1000,
    overlap=200
):
    """
    Split text into overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start += chunk_size - overlap

    return chunks


def create_chunks(pages, filename):
    """
    Create chunks and keep PDF filename + page number.
    """

    chunks = []

    for page in pages:

        page_chunks = split_text(
            page["text"],
            chunk_size=1000,
            overlap=200
        )

        for chunk in page_chunks:

            chunks.append(
                {
                    "text": chunk,
                    "page": page["page"],
                    "filename": filename
                }
            )

    return chunks