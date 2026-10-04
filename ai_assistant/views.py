import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import student_required, teacher_required
from assignments.forms import GradeForm
from assignments.models import Submission
from classroom.models import Classroom, Enrollment, Material

from .forms import AssignmentGeneratorForm, MaterialSummarizerForm, QuizGeneratorForm, StudyAssistantForm
from .services.audit import record_interaction
from .services.orchestration import (
    answer_question,
    evaluate_submission as evaluate_submission_service,
    generate_assignment,
    generate_quiz,
    summarize_material,
)
from .services.provider import AIServiceError, AIProvider


def _run_ai(request, feature, service_call, **relations):
    try:
        result, raw = service_call()
        record_interaction(
            request.user,
            feature,
            'completed',
            output_text=raw,
            model_name=AIProvider().model,
            **relations,
        )
        return result
    except AIServiceError as exc:
        record_interaction(
            request.user,
            feature,
            'failed',
            error_message=str(exc),
            model_name=AIProvider().model,
            **relations,
        )
        messages.error(request, str(exc))
    return None


@student_required
def study_assistant(request):
    classrooms = Classroom.objects.filter(enrollments__student=request.user).distinct()
    form = StudyAssistantForm(request.POST or None)
    form.fields['classroom'].queryset = classrooms
    result = None
    if request.method == 'POST' and form.is_valid():
        classroom = form.cleaned_data['classroom']
        result = _run_ai(
            request,
            'study_assistant',
            lambda: answer_question(form.cleaned_data['question'], classroom.materials.all()),
            classroom=classroom,
        )
    return render(request, 'ai_assistant/study_assistant.html', {'form': form, 'result': result})


@teacher_required
def assignment_generator(request):
    classrooms = Classroom.objects.filter(teacher=request.user)
    form = AssignmentGeneratorForm(request.POST or None)
    form.fields['classroom'].queryset = classrooms
    result = None
    selected_classroom = None
    if request.method == 'POST' and form.is_valid():
        classroom = form.cleaned_data['classroom']
        selected_classroom = classroom
        result = _run_ai(
            request,
            'assignment_generator',
            lambda: generate_assignment(
                form.cleaned_data['topic'],
                form.cleaned_data['difficulty'],
                form.cleaned_data['max_marks'],
                classroom.materials.all(),
            ),
            classroom=classroom,
        )
    return render(request, 'ai_assistant/assignment_generator.html', {
        'form': form, 'result': result, 'selected_classroom': selected_classroom,
    })


@teacher_required
def material_summarizer(request):
    materials = Material.objects.filter(classroom__teacher=request.user).select_related('classroom')
    form = MaterialSummarizerForm(request.POST or None)
    form.fields['material'].queryset = materials
    result = None
    selected_material = None
    if request.method == 'POST' and form.is_valid():
        selected_material = form.cleaned_data['material']
        result = _run_ai(
            request,
            'material_summarizer',
            lambda: summarize_material(selected_material),
            classroom=selected_material.classroom,
            material=selected_material,
        )
    return render(request, 'ai_assistant/material_summarizer.html', {
        'form': form, 'result': result, 'selected_material': selected_material,
    })


@teacher_required
def quiz_generator(request):
    materials = Material.objects.filter(classroom__teacher=request.user).select_related('classroom')
    form = QuizGeneratorForm(request.POST or None)
    form.fields['material'].queryset = materials
    result = None
    selected_material = None
    if request.method == 'POST' and form.is_valid():
        selected_material = form.cleaned_data['material']
        result = _run_ai(
            request,
            'quiz_generator',
            lambda: generate_quiz(selected_material, form.cleaned_data['number_questions']),
            classroom=selected_material.classroom,
            material=selected_material,
        )
    return render(request, 'ai_assistant/quiz_generator.html', {
        'form': form, 'result': result, 'selected_material': selected_material,
    })


@teacher_required
def evaluate_submission(request, pk):
    submission = get_object_or_404(
        Submission.objects.select_related('assignment', 'assignment__classroom', 'student'),
        pk=pk,
        assignment__classroom__teacher=request.user,
    )
    result = None
    review_form = None
    if request.method == 'POST':
        result = _run_ai(
            request,
            'assignment_evaluation',
            lambda: evaluate_submission_service(submission.assignment, submission),
            classroom=submission.assignment.classroom,
            assignment=submission.assignment,
            submission=submission,
        )
        if result:
            review_form = GradeForm(initial={
                'marks': result.get('suggested_marks'),
                'feedback': result.get('feedback', ''),
                'status': 'submitted',
            })
    return render(request, 'ai_assistant/evaluate_submission.html', {
        'submission': submission,
        'result': result,
        'review_form': review_form,
    })
