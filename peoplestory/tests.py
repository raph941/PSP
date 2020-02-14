from django.test import TestCase
from django.urls import reverse, resolve
from .views import home


class HomeTests(TestCase):
    # def test_home_view_status_code(self):
    #     url = reverse('home')
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        #test if the home view is the actual view beign served from the url
        view = resolve('/')
        self.assertEquals(view.func, home)