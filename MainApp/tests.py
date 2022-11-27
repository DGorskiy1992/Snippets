from django.test import TestCase
from MainApp.models import Snippet


class SnippetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Snippet.objects.create(name='Test', lang='python', code='print("Hello World!")')

    def test_name_label(self):
        snippet = Snippet.objects.get(id=1)
        field_label = snippet._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_language_label(self):
        snippet = Snippet.objects.get(id=1)
        field_label = snippet._meta.get_field('lang').verbose_name
        self.assertEquals(field_label, 'lang')

    def test_code_label(self):
        snippet = Snippet.objects.get(id=1)
        field_label = snippet._meta.get_field('code').verbose_name
        self.assertEquals(field_label, 'code')

    def test_is_public_label(self):
        snippet = Snippet.objects.get(id=1)
        field_label = snippet._meta.get_field('is_public').default
        print(field_label)
        self.assertTrue(field_label)



# Create your tests here.
