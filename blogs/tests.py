from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore

from .models import Category, Blog
from blogs.templatetags.mark import markdown_to_html


class MarkTests(TestCase):

    def test_markdown_to_html(self):
        text = '*Hello*'
        html = markdown_to_html(text)
        self.assertEqual(html, '<p><em>Hello</em></p>')


class CategoryModelTests(TestCase):
    def test_category_title_result(self):
        result = Category(title='カテゴリー１')
        self.assertIsInstance(result.__str__(), str)


class BlogModelTests(TestCase):
    def test_blog_to_release_result(self):
        category = Category.objects.create(title='カテゴリー１')
        result = category.blog_set.create(
                title='タイトル',
                text='テキスト',
                is_publick=False
                )
        result.to_release()
        self.assertIs(result.is_publick, True)

    def test_blog_to_private_result(self):
        category = Category.objects.create(title='カテゴリー１')
        result = category.blog_set.create(
                title='タイトル',
                text='テキスト',
                is_publick=True
                )
        result.to_private()
        self.assertIs(result.is_publick, False)

