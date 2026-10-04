from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import (
    Classroom, Enrollment, Post, Comment,
    Assignment, Submission, Meeting, Attachment
)
from .forms import (
    ClassroomForm, JoinClassroomForm, PostForm, CommentForm,
    AssignmentForm, SubmissionForm, GradeForm, MeetingForm, AttachmentForm
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_classroom_or_403(classroom_id, user):
    classroom = get_object_or_404(Classroom, pk=classroom_id, is_active=True)
    is_member = (classroom.teacher == user) or classroom.students.filter(pk=user.pk).exists()
    if not is_member:
        return None, HttpResponseForbidden("You are not a member of this classroom.")
    return classroom, None


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.is_teacher:
        classrooms = Classroom.objects.filter(teacher=request.user, is_active=True)
    else:
        classrooms = request.user.enrolled_classrooms.filter(is_active=True)

    return render(request, 'classroom/dashboard.html', {
        'classrooms': classrooms,
        'profile': profile,
    })


# ─── Classroom CRUD ───────────────────────────────────────────────────────────

@login_required
def classroom_create(request):
    if not request.user.profile.is_teacher:
        messages.error(request, "Only teachers can create classrooms.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()
            messages.success(request, f'Classroom "{classroom.name}" created! Code: {classroom.code}')
            return redirect('classroom_detail', pk=classroom.pk)
    else:
        form = ClassroomForm()

    return render(request, 'classroom/classroom_form.html', {'form': form, 'action': 'Create'})


@login_required
def classroom_edit(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Classroom updated.")
            return redirect('classroom_detail', pk=classroom.pk)
    else:
        form = ClassroomForm(instance=classroom)

    return render(request, 'classroom/classroom_form.html', {'form': form, 'action': 'Edit', 'classroom': classroom})


@login_required
def classroom_delete(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        classroom.is_active = False
        classroom.save()
        messages.success(request, f'Classroom "{classroom.name}" deleted.')
        return redirect('dashboard')

    return render(request, 'classroom/classroom_confirm_delete.html', {'classroom': classroom})


@login_required
def classroom_detail(request, pk):
    classroom, err = get_classroom_or_403(pk, request.user)
    if err:
        return err

    posts        = classroom.posts.prefetch_related('comments', 'attachments', 'author__profile').all()
    post_form    = PostForm()
    comment_form = CommentForm()

    return render(request, 'classroom/classroom_detail.html', {
        'classroom':    classroom,
        'posts':        posts,
        'post_form':    post_form,
        'comment_form': comment_form,
        'is_teacher':   classroom.teacher == request.user,
    })


@login_required
def classroom_join(request):
    if not request.user.profile.is_student:
        messages.error(request, "Only students can join classrooms.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = JoinClassroomForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                classroom = Classroom.objects.get(code=code, is_active=True)
            except Classroom.DoesNotExist:
                messages.error(request, "No classroom found with that code.")
                return render(request, 'classroom/classroom_join.html', {'form': form})

            if classroom.students.filter(pk=request.user.pk).exists():
                messages.warning(request, "You are already enrolled in this classroom.")
            else:
                Enrollment.objects.create(student=request.user, classroom=classroom)
                messages.success(request, f'Joined "{classroom.name}" successfully! 🎉')

            return redirect('classroom_detail', pk=classroom.pk)
    else:
        form = JoinClassroomForm()

    return render(request, 'classroom/classroom_join.html', {'form': form})


@login_required
def classroom_leave(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    enrollment = get_object_or_404(Enrollment, student=request.user, classroom=classroom)

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, f'You have left "{classroom.name}".')
        return redirect('dashboard')

    return render(request, 'classroom/classroom_leave_confirm.html', {'classroom': classroom})


@login_required
def classroom_members(request, pk):
    classroom, err = get_classroom_or_403(pk, request.user)
    if err:
        return err

    enrollments = Enrollment.objects.filter(classroom=classroom).select_related('student__profile')
    return render(request, 'classroom/classroom_members.html', {
        'classroom':   classroom,
        'enrollments': enrollments,
        'is_teacher':  classroom.teacher == request.user,
    })


@login_required
def remove_student(request, pk, student_id):
    classroom = get_object_or_404(Classroom, pk=pk)
    if classroom.teacher != request.user:
        return HttpResponseForbidden()

    enrollment = get_object_or_404(Enrollment, classroom=classroom, student_id=student_id)
    if request.method == 'POST':
        student_name = enrollment.student.username
        enrollment.delete()
        messages.success(request, f'Removed {student_name} from the classroom.')

    return redirect('classroom_members', pk=pk)


# ─── Posts ────────────────────────────────────────────────────────────────────

@login_required
def post_create(request, classroom_pk):
    classroom, err = get_classroom_or_403(classroom_pk, request.user)
    if err:
        return err

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.classroom = classroom
            post.author    = request.user
            post.save()

            # Handle file attachment
            if request.FILES.get('attachment'):
                f = request.FILES['attachment']
                Attachment.objects.create(
                    post=post, file=f, name=f.name, uploaded_by=request.user
                )
            messages.success(request, "Posted!")
    else:
        messages.error(request, "Invalid post.")

    return redirect('classroom_detail', pk=classroom_pk)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    classroom_pk = post.classroom.pk

    if post.author != request.user and post.classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted.")

    return redirect('classroom_detail', pk=classroom_pk)


@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    classroom, err = get_classroom_or_403(post.classroom.pk, request.user)
    if err:
        return err

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post   = post
            comment.author = request.user
            comment.save()

    return redirect('classroom_detail', pk=post.classroom.pk)


# ─── Assignments ──────────────────────────────────────────────────────────────

@login_required
def assignment_list(request, classroom_pk):
    classroom, err = get_classroom_or_403(classroom_pk, request.user)
    if err:
        return err

    assignments = classroom.assignments.all()
    is_teacher  = classroom.teacher == request.user

    # Annotate with submission status for students
    if not is_teacher:
        for a in assignments:
            a.my_submission = a.submission_for(request.user)

    return render(request, 'classroom/assignment_list.html', {
        'classroom':   classroom,
        'assignments': assignments,
        'is_teacher':  is_teacher,
    })


@login_required
def assignment_create(request, classroom_pk):
    classroom = get_object_or_404(Classroom, pk=classroom_pk)
    if classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.classroom = classroom
            assignment.save()

            # Handle attachments
            for f in request.FILES.getlist('attachments'):
                Attachment.objects.create(
                    assignment=assignment, file=f, name=f.name, uploaded_by=request.user
                )

            messages.success(request, f'Assignment "{assignment.title}" created.')
            return redirect('assignment_list', classroom_pk=classroom_pk)
    else:
        form = AssignmentForm()

    return render(request, 'classroom/assignment_form.html', {
        'form': form, 'classroom': classroom, 'action': 'Create'
    })


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    classroom, err = get_classroom_or_403(assignment.classroom.pk, request.user)
    if err:
        return err

    is_teacher     = classroom.teacher == request.user
    my_submission  = None
    all_submissions = None
    submit_form    = None
    grade_forms    = {}

    if is_teacher:
        all_submissions = assignment.submissions.select_related('student__profile').all()
        for sub in all_submissions:
            grade_forms[sub.pk] = GradeForm(instance=sub, prefix=str(sub.pk))
    else:
        my_submission = assignment.submission_for(request.user)
        if not my_submission:
            submit_form = SubmissionForm()

    return render(request, 'classroom/assignment_detail.html', {
        'assignment':       assignment,
        'classroom':        classroom,
        'is_teacher':       is_teacher,
        'my_submission':    my_submission,
        'submit_form':      submit_form,
        'all_submissions':  all_submissions,
        'grade_forms':      grade_forms,
    })


@login_required
def assignment_submit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    classroom, err = get_classroom_or_403(assignment.classroom.pk, request.user)
    if err:
        return err

    if request.user.profile.is_teacher:
        messages.error(request, "Teachers cannot submit assignments.")
        return redirect('assignment_detail', pk=pk)

    if assignment.submission_for(request.user):
        messages.warning(request, "You already submitted this assignment.")
        return redirect('assignment_detail', pk=pk)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.assignment = assignment
            sub.student    = request.user
            sub.status     = 'late' if assignment.is_overdue() else 'submitted'
            sub.save()
            messages.success(request, "Assignment submitted! ✅")
            return redirect('assignment_detail', pk=pk)

    return redirect('assignment_detail', pk=pk)


@login_required
def assignment_grade(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    classroom  = submission.assignment.classroom

    if classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission, prefix=str(submission.pk))
        if form.is_valid():
            sub = form.save(commit=False)
            sub.status    = 'graded'
            sub.graded_at = timezone.now()
            sub.save()
            messages.success(request, f"Graded {submission.student.username}'s submission.")

    return redirect('assignment_detail', pk=submission.assignment.pk)


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if assignment.classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        classroom_pk = assignment.classroom.pk
        assignment.delete()
        messages.success(request, "Assignment deleted.")
        return redirect('assignment_list', classroom_pk=classroom_pk)

    return render(request, 'classroom/assignment_confirm_delete.html', {'assignment': assignment})


# ─── Meetings ─────────────────────────────────────────────────────────────────

@login_required
def meeting_list(request, classroom_pk):
    classroom, err = get_classroom_or_403(classroom_pk, request.user)
    if err:
        return err

    meetings   = classroom.meetings.all()
    is_teacher = classroom.teacher == request.user

    return render(request, 'classroom/meeting_list.html', {
        'classroom': classroom,
        'meetings':  meetings,
        'is_teacher': is_teacher,
    })


@login_required
def meeting_create(request, classroom_pk):
    classroom = get_object_or_404(Classroom, pk=classroom_pk)
    if classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.classroom  = classroom
            meeting.created_by = request.user
            meeting.save()
            messages.success(request, f'Meeting "{meeting.title}" scheduled.')
            return redirect('meeting_list', classroom_pk=classroom_pk)
    else:
        form = MeetingForm()

    return render(request, 'classroom/meeting_form.html', {
        'form': form, 'classroom': classroom
    })


@login_required
def meeting_delete(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if meeting.classroom.teacher != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        classroom_pk = meeting.classroom.pk
        meeting.delete()
        messages.success(request, "Meeting deleted.")
        return redirect('meeting_list', classroom_pk=classroom_pk)

    return render(request, 'classroom/meeting_confirm_delete.html', {'meeting': meeting})
