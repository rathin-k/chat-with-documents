def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
):

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks