import datetime

from django.test import TestCase
from django.utils import timezone

from django.urls import reverse
from .models import Question

# Create your tests here.

def create_question(question_text,days):
	t=timezone.now() +datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text,pub_date=t)

class QuestionViewTest(TestCase):

	def test_index_view_with_no_question(self):
		response=self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"No Polls Available")
		self.assertQuerysetEqual(response.context['list_question'],[])

	def test_index_view_with_a_past_question(self):
		create_question(question_text='Past Question.',days=-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['list_question'],
			['<Question: Past Question.>']
		)

	def test_index_view_with_a_future_question(self):
		create_question(question_text='Future Question.',days=30)
		response=self.client.get(reverse('polls:index'))
		self.assertContains(response,'No Polls Available')
		self.assertQuerysetEqual(response.context['list_question'],[])

	def test_index_view_with_future_and_past_question(self):
		create_question(question_text='Future Question',days=30)
		create_question(question_text='Past Question',days=-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['list_question'],['<Question: Past Question>'])

	def test_index_view_with_two_past_question(self):
		create_question(question_text='Past Question 1',days=-30)
		create_question(question_text='Past Question 2',days=-5)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['list_question'],['<Question: Past Question 2>' , '<Question: Past Question 1>'])
		

class QuestionIndexDetailTests(TestCase):

	def test_detail_view_with_a_future_question(self):
	        future_question = create_question(question_text='Future question.', days=5)
	        url = reverse('polls:detail', args=(future_question.id,))
        	response = self.client.get(url)
	        self.assertEqual(response.status_code, 404)
	
	def test_detail_view_with_a_past_question(self):
		past_question=create_question(question_text='PastQuestion',days=-5)
		url=reverse('polls:detail',args=(past_question.id,))
		response=self.client.get(url)
		self.assertContains(response,past_question.question_text)


class QuestionMethodTests(TestCase):
	
	def test_was_published_recently_with_old_question(self):
		t=timezone.now()+datetime.timedelta(days=30)
		future_date=Question(pub_date=t)
		self.assertIs(future_date.was_published_recently(),False)

	def test_was_published_with_recent_question(self):
		t=timezone.now()-datetime.timedelta(hours=1)
		recent_date=Question(pub_date=t)
		self.assertIs(recent_date.was_published_recently(),True)
