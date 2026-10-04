from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserProfile
from assignments.models import Assignment, Submission
from classroom.models import Classroom, Enrollment, Material


class AIAuthorizationTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user('teacher', password='pass12345')
        UserProfile.objects.create(user=self.teacher, role='teacher')
        self.student = User.objects.create_user('student', password='pass12345')
        UserProfile.objects.create(user=self.student, role='student')
        self.classroom = Classroom.objects.create(
            name='Science', subject='Biology', teacher=self.teacher,
        )
        Enrollment.objects.create(student=self.student, classroom=self.classroom)

    def test_student_can_open_study_assistant(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('ai_assistant:study_assistant'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_cannot_open_student_study_assistant(self):
        self.client.force_login(self.teacher)
        response = self.client.get(reverse('ai_assistant:study_assistant'))
        self.assertRedirects(response, reverse('teacher_dashboard'))

    def test_teacher_can_open_assignment_generator(self):
        self.client.force_login(self.teacher)
        response = self.client.get(reverse('ai_assistant:assignment_generator'))
        self.assertEqual(response.status_code, 200)

    def test_student_cannot_open_teacher_tools(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('ai_assistant:quiz_generator'))
        self.assertRedirects(response, reverse('student_dashboard'))

    @patch('ai_assistant.views.answer_question')
    def test_student_question_is_scoped_to_enrolled_classroom(self, answer_question):
        answer_question.return_value = ({'answer': 'Plants use light.'}, '{"answer":"Plants use light."}')
        material = Material.objects.create(
            classroom=self.classroom,
            title='Notes',
            file=SimpleUploadedFile('notes.txt', b'Plants use light.'),
            uploaded_by=self.teacher,
        )
        self.client.force_login(self.student)
        response = self.client.post(reverse('ai_assistant:study_assistant'), {
            'classroom': self.classroom.pk,
            'question': 'What do plants use?',
        })
        self.assertEqual(response.status_code, 200)
        answer_question.assert_called_once()
        self.assertEqual(answer_question.call_args.args[0], 'What do plants use?')
        self.assertEqual(list(answer_question.call_args.args[1]), [material])


class AIEvaluationTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user('teacher', password='pass12345')
        UserProfile.objects.create(user=self.teacher, role='teacher')
        self.student = User.objects.create_user('student', password='pass12345')
        UserProfile.objects.create(user=self.student, role='student')
        classroom = Classroom.objects.create(name='History', subject='History', teacher=self.teacher)
        self.assignment = Assignment.objects.create(
            classroom=classroom,
            title='Essay',
            description='Explain the causes of the event.',
            due_date='2030-01-01T12:00:00Z',
            max_marks=20,
        )
        self.submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file=SimpleUploadedFile('essay.txt', b'The event happened because...'),
        )

    @patch('ai_assistant.views.evaluate_submission_service')
    def test_evaluation_suggests_review_without_saving_grade(self, evaluate):
        evaluate.return_value = ({
            'suggested_marks': 16,
            'strengths': ['Clear explanation'],
            'weaknesses': ['Add evidence'],
            'feedback': 'Good start.',
        }, '{"suggested_marks":16}')
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('ai_assistant:evaluate_submission', args=[self.submission.pk]))
        self.assertEqual(response.status_code, 200)
        self.submission.refresh_from_db()
        self.assertIsNone(self.submission.marks)
        self.assertContains(response, 'Teacher approval required')
        self.assertContains(response, 'Save final grade')

    def test_student_cannot_evaluate_submission(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('ai_assistant:evaluate_submission', args=[self.submission.pk]))
        self.assertRedirects(response, reverse('student_dashboard'))
