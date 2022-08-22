import datetime
from http import client
from django.utils import timezone

from django.test import TestCase

from .models import Question, Choice

from django.urls import reverse

from django.db.models import F

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text):
    """Create a test choice with the given 'question' and 'choice_text'"""
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, milliseconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now()-datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        choice_question = create_choice(question=question, choice_text='choice1')

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question]
        )
    
    def test_future_question(self):
        """
        Questions with a pub_date in the future are no displayed on the index page.
        """
        create_question(question_text="Future question.", days=30)

        response = self.client.get(reverse('polls:index'))
        
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [],)

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        past_choice = create_choice(question=question, choice_text='future-choice') 

        future_question = create_question(question_text="Future question.", days=30)
        future_choice = create_choice(question=future_question, choice_text='Future-choice') 

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        choice_question1 = create_choice(question1, choice_text='choice_question1')


        question2 = create_question(question_text="Past question 2.", days=-5)
        choice_question2 = create_choice(question2, choice_text='choice_question2')


        response = self.client.get(reverse('polls:index'))

        queryset = response.context['latest_question_list']
        self.assertQuerysetEqual(
            list(queryset),
            [question1, question2]
        )


    def test_question_no_choices(self):
        """The questions with no choices are displayed in the index page """

        question1 = create_question(question_text='No choices question', days=-5)

        question2 = create_question(question_text='With choices question', days=-5)
        choice1 = create_choice(question=question2, choice_text='choice1')
        choice2 = create_choice(question=question2, choice_text='choice2')

        url = reverse('polls:index')
        response = self.client.get(url)
        
        queryset = response.context['latest_question_list']

        self.assertListEqual(list(queryset), [question1, question2])

    def test_question_with_choices(self):
        """The questions with choices are displayed in the index page"""

        question1 = create_question(question_text='With choices question 1', days=-5)
        choice1 = create_choice(question=question1, choice_text='choice1')
        choice2 = create_choice(question=question1, choice_text='choice2')

        question2 = create_question(question_text='With choices question 2', days=-6)
        choice1 = create_choice(question=question2, choice_text='choice1')
        choice2 = create_choice(question=question2, choice_text='choice2')
        
        url = reverse('polls:index')
        response = self.client.get(url)

        queryset = response.context['latest_question_list']

        self.assertQuerysetEqual(list(queryset), [question1, question2])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):

        """
        The detail view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionChoiceRaceConditionTest(TestCase):
    def test_race_condition(self):
        """
        Test the race condition if the system attempts to perform two or more operation at the same time
        """
        question = create_question(question_text='race_condition', days=-5)
        choice =  create_choice(question, 'choice1')

        first_vote = question.choice_set.get(id=choice.id)
        second_vote = question.choice_set.get(id=choice.id)
        another_vote = question.choice_set.get(id=choice.id)

        first_vote.votes = F('votes') + 1
        second_vote.votes = F('votes') + 1

        
        second_vote.save()
        first_vote.save()

        another_vote.votes = F('votes') + 1

        another_vote.save()

        self.assertEqual(question.choice_set.get(pk=choice.id).votes, 3)