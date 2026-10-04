from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import teacher_required, student_required
from classroom.models import Classroom, Enrollment
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm, GradeForm


# ─── Teacher Views ────────────────────────────────────────────────────────────

@teacher_required
def create_assignment(request, classroom_pk):
    classroom = get_object_or_404(Classroom, pk=classroom_pk, teacher=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.classroom = classroom
            assignment.save()
            messages.success(request, f'Assignment "{assignment.title}" created!')
            return redirect('classroom_detail_teacher', pk=classroom_pk)
    else:
        form = AssignmentForm()
    return render(request, 'assignments/create_assignment.html', {
        'form': form, 'classroom': classroom, 'action': 'Create'
    })


@teacher_required
def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, classroom__teacher=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated!')
            return redirect('classroom_detail_teacher', pk=assignment.classroom.pk)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/create_assignment.html', {
        'form': form, 'classroom': assignment.classroom, 'assignment': assignment, 'action': 'Edit'
    })


@teacher_required
def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, classroom__teacher=request.user)
    classroom_pk = assignment.classroom.pk
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted.')
        return redirect('classroom_detail_teacher', pk=classroom_pk)
    return render(request, 'classroom/confirm_delete.html', {'object': assignment, 'type': 'Assignment'})


@teacher_required
def view_submissions(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, classroom__teacher=request.user)
    submissions = assignment.submissions.select_related('student').all()
    enrolled_count = assignment.classroom.enrollments.count()
    return render(request, 'assignments/view_submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
        'enrolled_count': enrolled_count,
    })


@teacher_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk, assignment__classroom__teacher=request.user)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            graded = form.save(commit=False)
            graded.status = 'graded'
            graded.save()
            messages.success(request, f'Submission graded: {graded.marks}/{submission.assignment.max_marks}')
            return redirect('view_submissions', pk=submission.assignment.pk)
    else:
        form = GradeForm(instance=submission)
    return render(request, 'assignments/grade_submission.html', {
        'form': form, 'submission': submission
    })


# ─── Student Views ────────────────────────────────────────────────────────────

@student_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    enrolled = Enrollment.objects.filter(student=request.user, classroom=assignment.classroom).exists()
    if not enrolled:
        messages.error(request, 'You are not enrolled in this classroom.')
        return redirect('student_dashboard')
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment, 'submission': submission
    })


@student_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    enrolled = Enrollment.objects.filter(student=request.user, classroom=assignment.classroom).exists()
    if not enrolled:
        messages.error(request, 'You are not enrolled in this classroom.')
        return redirect('student_dashboard')

    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
    if existing:
        messages.info(request, 'You have already submitted this assignment.')
        return redirect('assignment_detail', pk=pk)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            if assignment.is_overdue():
                submission.status = 'late'
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('assignment_detail', pk=pk)
    else:
        form = SubmissionForm()
    return render(request, 'assignments/submit_assignment.html', {
        'form': form, 'assignment': assignment
    })


@student_required
def my_submissions(request):
    submissions = Submission.objects.filter(student=request.user).select_related(
        'assignment', 'assignment__classroom'
    )
    return render(request, 'assignments/my_submissions.html', {'submissions': submissions})
