import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is
        older than one day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is
        within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                    seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):

    def test_response_status_code(self):
        """
        Check that the response status_code is 200
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question('what is this past question?', -10)
        # call the index page
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                ['<Question: what is this past question?>'])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't dislayed on
        the index page.
        """
        # create a question with future pub_date
        create_question('future question.', 10)
        # request the page
        response = self.client.get(reverse('polls:index'))
        # check that the question isn't in the queryset
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question('future question.', 10)
        create_question('past question.', -1)
        response = self.client.get(reverse('polls:index'))
        # check that only the past question is displayed
        self.assertQuerysetEqual(response.context['latest_question_list'],
                ['<Question: past question.>'])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question('Past question 1.', -3)
        create_question('Past question 2.', -5)
        response = self.client.get(reverse('polls:index'))
        # check that both questions are displayed
        self.assertQuerysetEqual(response.context['latest_question_list'],
                ['<Question: Past question 1.>',
                '<Question: Past question 2.>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with pub_date in the future returns
        a 404 not found response from the server.
        """
        future_question = create_question('Future question.', 1)
        url = reverse('polls:detail', args = (future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the detail view of a question with a pub_date in the past returns
        a 200 status code from the server and displays the question's text.
        """
        # setup
        past_question = create_question('Past question.', -1)
        url = reverse('polls:detail', args = (past_question.id, ))
        response = self.client.get(url)
        # tests
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    """
    Tests for the Results view of my django tutorial site
    """
    def test_future_question(self):
        """
        The results view of a question with pub_date in the future should
        return a 404 not found status code.
        """
        future_question = create_question('Future question.', 1)
        url = reverse('polls:results', args = (future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with pub_date in the past should
        return a 200 status code and contain the question text
        """
        # setup
        past_question = create_question('Past question.', -1)
        url = reverse('polls:results', args = (past_question.id, ))
        response = self.client.get(url)
        # tests
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
