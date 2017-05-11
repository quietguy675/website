import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question
# Create your tests here

class QuestiomMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose pub_date was more than one day in the past
        """
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose pub_date was within 1 day old
        """
        time = timezone.now() - datetime.timedelta(hours=12)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Creates a question with the given 'question_text' and published
    the given number of 'days' offset to now (negative for questions
    published in the past, positive for questions which are
    yet to be published.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
        pub_date = time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be
        displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed
        on the index page
        """
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])


     
    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed
        on the index page
        """
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

     
    def test_index_view_with_a_past_and_future_question(self):
        """
        Questions with a pub_date in the past should be displayed
        on the index page
        """
        create_question(question_text="Future question", days=30)
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

     
    def test_index_view_with_two_past_questions(self):
        """
        Questions with a pub_date in the past should be displayed
        on the index page
        """
        create_question(question_text="Past question1", days=-2)
        create_question(question_text="Past question2", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question1>','<Question: Past question2>'])

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the
        future should return a 404 not found
        """
        future_question = create_question(question_text="future question",
        days = 5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        should display the question's text.
        """
        past_question = create_question(question_text='Past Question',
        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)













