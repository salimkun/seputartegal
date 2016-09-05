import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import *

def create_question(title, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Informasi.objects.create(title=title, date=time)

class InformasiMethodTests(TestCase):
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('webku:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['info'], [])

		def test_index_view_with_a_past_question(self):
			create_informasi(title="Past question.", days=-30)
			response = self.client.get(reverse('webku:index'))
			self.assertQuerysetEqual(
			response.context['info'],
			['<Informasi: Past question.>']
			)

			def test_index_view_with_a_future_question(self):
				create_informasi(title="Future question.", days=30)
				response = self.client.get(reverse('webku:index'))
				self.assertContains(response, "No polls are available.")
				self.assertQuerysetEqual(response.context['info'], [])

				def test_index_view_with_future_question_and_past_question(self):
					create_informasi(title="Past question.", days=-30)
					create_informasi(title="Future question.", days=30)
					response = self.client.get(reverse('webku:index'))
					self.assertQuerysetEqual( response.context['info'],
					['<Informasi: Past question.>'])

					def test_index_view_with_two_past_questions(self):
						create_informasi(title="Past question 1.", days=-30)
						create_informasi(title="Past question 2.", days=-5)
						response = self.client.get(reverse('webku:index'))
						self.assertQuerysetEqual(
						response.context['info'],
						['<Informasi: Past question 2.>', '<Informasi: Past question 1.>']
						)