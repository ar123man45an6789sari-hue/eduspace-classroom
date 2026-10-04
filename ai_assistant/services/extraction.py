import os

from django.core.exceptions import ValidationError

from .provider import AIServiceError


class DocumentExtractionError(AIServiceError):
    pass


SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md'}
MAX_EXTRACTED_CHARS = 50000


def extract_file_text(field_file, max_chars=MAX_EXTRACTED_CHARS):
    if not field_file:
        raise DocumentExtractionError('No document was provided.')

    extension = os.path.splitext(field_file.name)[1].lower()
    if extension not in SUPPORTED_EXTENSIONS:
        supported = ', '.join(sorted(SUPPORTED_EXTENSIONS))
        raise DocumentExtractionError(f'Unsupported file type. Supported formats: {supported}.')

    try:
        field_file.open('rb')
        if extension in {'.txt', '.md'}:
            text = field_file.read().decode('utf-8', errors='replace')
        elif extension == '.pdf':
            from pypdf import PdfReader
            reader = PdfReader(field_file)
            text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        else:
            from docx import Document
            document = Document(field_file)
            text = '\n'.join(paragraph.text for paragraph in document.paragraphs)
    except ImportError as exc:
        raise DocumentExtractionError('Document processing dependencies are not installed.') from exc
    except Exception as exc:
        raise DocumentExtractionError(f'Could not read this file: {exc}') from exc
    finally:
        try:
            field_file.close()
        except Exception:
            pass

    text = text.strip()
    if not text:
        raise DocumentExtractionError('This document does not contain readable text.')
    return text[:max_chars]
