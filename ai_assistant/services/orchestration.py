from .extraction import extract_file_text
from .provider import AIProvider, parse_json_response


SYSTEM_PROMPT = (
    'You are EduSpace AI, an educational assistant. Be accurate, clear, constructive, and age-appropriate. '
    'Use only the supplied classroom context when answering material-based questions. State when the context is insufficient.'
)


def _context(materials):
    sections = []
    for material in materials:
        try:
            text = extract_file_text(material.file)
        except Exception as exc:
            sections.append(f'[{material.title}] Unreadable: {exc}')
            continue
        sections.append(f'[{material.title}]\n{text}')
    return '\n\n'.join(sections) or 'No readable classroom materials were supplied.'


def _json_result(provider, instruction, context=''):
    response = provider.generate(
        SYSTEM_PROMPT + ' Return valid JSON only when a JSON schema is requested.',
        f'{instruction}\n\nCLASSROOM CONTEXT:\n{context}',
        json_mode=True,
    )
    return parse_json_response(response), response


def answer_question(question, materials, provider=None):
    provider = provider or AIProvider()
    result, raw = _json_result(
        provider,
        'Answer the student question. Return JSON with keys answer, sources (array of material titles), and follow_up (string).\n'
        f'STUDENT QUESTION: {question}',
        _context(materials),
    )
    return result, raw


def generate_assignment(topic, difficulty, max_marks, materials=None, provider=None):
    provider = provider or AIProvider()
    result, raw = _json_result(
        provider,
        'Create a classroom assignment. Return JSON with keys title, description, learning_objectives (array), '
        'questions (array of strings), and marking_criteria (array of objects with criterion and marks). '
        f'Topic: {topic}\nDifficulty: {difficulty}\nMaximum marks: {max_marks}',
        _context(materials or []),
    )
    return result, raw


def summarize_material(material, provider=None):
    provider = provider or AIProvider()
    text = extract_file_text(material.file)
    result, raw = _json_result(
        provider,
        'Summarize the supplied study material. Return JSON with keys summary, key_concepts (array), important_terms (array of objects with term and meaning), and exam_questions (array).',
        f'[{material.title}]\n{text}',
    )
    return result, raw


def generate_quiz(material, number_questions, provider=None):
    provider = provider or AIProvider()
    text = extract_file_text(material.file)
    result, raw = _json_result(
        provider,
        f'Create {number_questions} questions from the supplied material. Return JSON with key questions, an array of objects containing question, options (array of four strings), answer, explanation, and difficulty. Use MCQs suitable for revision.',
        f'[{material.title}]\n{text}',
    )
    return result, raw


def evaluate_submission(assignment, submission, provider=None):
    provider = provider or AIProvider()
    submission_text = extract_file_text(submission.file)
    result, raw = _json_result(
        provider,
        'Evaluate the student submission against the assignment. Return JSON with keys suggested_marks (integer), strengths (array), weaknesses (array), feedback (string), and rubric_notes (array). This is only a recommendation for a teacher; do not claim that a grade was finalized.\n'
        f'ASSIGNMENT TITLE: {assignment.title}\nASSIGNMENT REQUIREMENTS:\n{assignment.description}\nMAXIMUM MARKS: {assignment.max_marks}\nSTUDENT NOTE:\n{submission.note or "None"}',
        f'STUDENT SUBMISSION:\n{submission_text}',
    )
    return result, raw
