from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import teacher_required, student_required
from .models import Classroom, Enrollment, Announcement, Material
from .forms import ClassroomForm, AnnouncementForm, MaterialForm, JoinClassroomForm
from assignments.models import Assignment


# ─── Teacher Views ────────────────────────────────────────────────────────────

@teacher_required
def teacher_dashboard(request):
    classrooms = Classroom.objects.filter(teacher=request.user)
    total_students = sum(c.get_student_count() for c in classrooms)
    total_assignments = Assignment.objects.filter(classroom__in=classrooms).count()
    return render(request, 'classroom/teacher_dashboard.html', {
        'classrooms': classrooms,
        'total_students': total_students,
        'total_assignments': total_assignments
    })


@teacher_required
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()
            messages.success(request, f'Classroom "{classroom.name}" created! Share the code: {classroom.join_code}')
            return redirect('classroom_detail_teacher', pk=classroom.pk)
    else:
        form = ClassroomForm()
    return render(request, 'classroom/create_classroom.html', {'form': form, 'action': 'Create'})


@teacher_required
def edit_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classroom updated successfully!')
            return redirect('classroom_detail_teacher', pk=classroom.pk)
    else:
        form = ClassroomForm(instance=classroom)
    return render(request, 'classroom/create_classroom.html', {'form': form, 'classroom': classroom, 'action': 'Edit'})


@teacher_required
def delete_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    if request.method == 'POST':
        name = classroom.name
        classroom.delete()
        messages.success(request, f'Classroom "{name}" has been deleted.')
        return redirect('teacher_dashboard')
    return render(request, 'classroom/confirm_delete.html', {'object': classroom, 'type': 'Classroom'})


@teacher_required
def classroom_detail_teacher(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    announcements = classroom.announcements.all()
    materials = classroom.materials.all()
    assignments = classroom.assignments.all()
    enrollments = classroom.enrollments.select_related('student').all()
    ann_form = AnnouncementForm()
    mat_form = MaterialForm()
    return render(request, 'classroom/classroom_detail_teacher.html', {
        'classroom': classroom,
        'announcements': announcements,
        'materials': materials,
        'assignments': assignments,
        'enrollments': enrollments,
        'ann_form': ann_form,
        'mat_form': mat_form,
    })


@teacher_required
def post_announcement(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.classroom = classroom
            ann.author = request.user
            ann.save()
            messages.success(request, 'Announcement posted!')
    return redirect('classroom_detail_teacher', pk=pk)


@teacher_required
def delete_announcement(request, pk, ann_pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    ann = get_object_or_404(Announcement, pk=ann_pk, classroom=classroom)
    if request.method == 'POST':
        ann.delete()
        messages.success(request, 'Announcement deleted.')
    return redirect('classroom_detail_teacher', pk=pk)


@teacher_required
def upload_material(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.classroom = classroom
            material.uploaded_by = request.user
            material.save()
            messages.success(request, 'Material uploaded successfully!')
        else:
            messages.error(request, 'Error uploading material.')
    return redirect('classroom_detail_teacher', pk=pk)


@teacher_required
def delete_material(request, pk, mat_pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    material = get_object_or_404(Material, pk=mat_pk, classroom=classroom)
    if request.method == 'POST':
        material.file.delete(save=False)
        material.delete()
        messages.success(request, 'Material removed.')
    return redirect('classroom_detail_teacher', pk=pk)


@teacher_required
def remove_student(request, pk, student_pk):
    classroom = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    enrollment = get_object_or_404(Enrollment, classroom=classroom, student_id=student_pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Student removed from the classroom.')
    return redirect('classroom_detail_teacher', pk=pk)


# ─── Student Views ────────────────────────────────────────────────────────────

@student_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('classroom')
    from assignments.models import Submission
    classroom_ids = enrollments.values_list('classroom_id', flat=True)
    all_assignments = Assignment.objects.filter(classroom_id__in=classroom_ids)
    submitted = Submission.objects.filter(student=request.user, assignment__in=all_assignments).values_list('assignment_id', flat=True)
    pending_assignments = all_assignments.exclude(id__in=submitted).count()
    completed_assignments = len(submitted)
    return render(request, 'classroom/student_dashboard.html', {
        'enrollments': enrollments,
        'pending_assignments': pending_assignments,
        'completed_assignments': completed_assignments
    })


@student_required
def join_classroom(request):
    if request.method == 'POST':
        form = JoinClassroomForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['join_code'].strip().upper()
            try:
                classroom = Classroom.objects.get(join_code=code)
                _, created = Enrollment.objects.get_or_create(student=request.user, classroom=classroom)
                if created:
                    messages.success(request, f'You have joined "{classroom.name}"!')
                else:
                    messages.info(request, f'You are already enrolled in "{classroom.name}".')
                return redirect('classroom_detail_student', pk=classroom.pk)
            except Classroom.DoesNotExist:
                messages.error(request, 'Invalid join code. Please check and try again.')
    else:
        form = JoinClassroomForm()
    return render(request, 'classroom/join_classroom.html', {'form': form})


@student_required
def classroom_detail_student(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    enrolled = Enrollment.objects.filter(student=request.user, classroom=classroom).exists()
    if not enrolled:
        messages.error(request, 'You are not enrolled in this classroom.')
        return redirect('student_dashboard')
    announcements = classroom.announcements.all()
    materials = classroom.materials.all()
    assignments = classroom.assignments.all()
    return render(request, 'classroom/classroom_detail_student.html', {
        'classroom': classroom,
        'announcements': announcements,
        'materials': materials,
        'assignments': assignments,
    })


@student_required
def leave_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    enrollment = get_object_or_404(Enrollment, student=request.user, classroom=classroom)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, f'You left "{classroom.name}".')
        return redirect('student_dashboard')
    return render(request, 'classroom/confirm_delete.html', {
        'object': classroom, 'type': 'Leave Classroom', 'action_label': 'Leave'
    })
