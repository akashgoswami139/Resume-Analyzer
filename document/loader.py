from pypdf import PdfReader


def pdf_to_text(uploaded_file) -> str:

    reader = PdfReader(uploaded_file)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text).strip()


def docx_to_text(uploaded_file) -> str:

    from unstructured.partition.docx import partition_docx

    elements = partition_docx(file=uploaded_file)

    text = "\n".join([str(el) for el in elements])

    return text.strip()