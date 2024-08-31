import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Q
from django.urls import reverse
from selenium import webdriver
from apps.authentication.models import User


class RegistrationViewTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        self.url = self.live_server_url + reverse("register")

    def tearDown(self):
        self.driver.quit()

    def test_registration_form_succeded(self):
        valid_data = {
            "username": "newuser",
            "email": "newuser@email.com",
            "password": "strong-password123",
        }

        self.assertFalse(
            User.objects.filter(
                Q(username=valid_data["username"]) | Q(email=valid_data["email"])
            ).exists()
        )

        self.driver.get(self.url)

        self.driver.find_element(value="id_username").send_keys(valid_data["username"])
        self.driver.find_element(value="id_email").send_keys(valid_data["email"])
        self.driver.find_element(value="id_password1").send_keys(valid_data["password"])
        self.driver.find_element(value="id_password2").send_keys(valid_data["password"])

        self.driver.find_element(value="submit_button").click()

        time.sleep(3)

        self.assertIn(reverse("login"), self.driver.current_url)

        is_user_created = User.objects.filter(username=valid_data["username"]).exists()

        self.assertTrue(is_user_created)

    def test_registration_form_has_errors(self):
        invalid_data = {
            "username": "new user",
            "email": "newuser@email",
            "password1": "strong-password123",
            "password2": "different-password123",
        }

        self.driver.get(self.url)

        self.driver.find_element(value="id_username").send_keys(invalid_data["username"])
        self.driver.find_element(value="id_email").send_keys(invalid_data["email"])
        self.driver.find_element(value="id_password1").send_keys(invalid_data["password1"])
        self.driver.find_element(value="id_password2").send_keys(invalid_data["password2"])

        self.driver.find_element(value="submit_button").click()

        time.sleep(3)

        self.assertIn(reverse("register"), self.driver.current_url)


class LoginViewTestCase(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_user(
            username="user1", password="strong-password123", email="user1@email.com"
        )

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.url = self.live_server_url + reverse("login")

    def tearDown(self):
        self.driver.quit()

    def test_login_form_succeded(self):
        valid_data = {
            "username": "user1",
            "password": "strong-password123",
            "email": "user1@email.com",
        }

        self.assertTrue(
            User.objects.filter(username=valid_data["username"], email=valid_data["email"])
        )

        self.driver.get(self.url)

        self.driver.find_element(value="id_username").send_keys(valid_data["username"])
        self.driver.find_element(value="id_password").send_keys(valid_data["password"])

        self.driver.find_element(value="submit_button").click()

        time.sleep(3)

        self.assertIn(reverse("home"), self.driver.current_url)

    def test_login_form_has_errors(self):
        invalid_data = {
            "username": "user2",
            "password": "different-password123",
        }

        self.driver.get(self.url)

        self.driver.find_element(value="id_username").send_keys(invalid_data["username"])
        self.driver.find_element(value="id_password").send_keys(invalid_data["password"])

        self.driver.find_element(value="submit_button").click()

        time.sleep(3)

        self.assertIn(reverse("login"), self.driver.current_url)


class LogoutViewTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1", password="strong-password123", email="user1@email.com"
        )

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.url = self.live_server_url + reverse("logout")
        self.login_url = self.live_server_url + reverse("login")

    def tearDown(self):
        self.driver.quit()

    def test_logout_succeded(self):
        valid_data = {
            "username": "user1",
            "password": "strong-password123",
        }

        self.assertTrue(User.objects.filter(username=self.user.username).exists())

        self.driver.get(self.login_url)

        self.driver.find_element(value="id_username").send_keys(valid_data["username"])
        self.driver.find_element(value="id_password").send_keys(valid_data["password"])

        self.driver.find_element(value="submit_button").click()

        time.sleep(3)

        self.driver.find_element(value="user-menu-button").click()

        time.sleep(1)

        self.driver.find_element(value="logout_button").click()

        time.sleep(3)

        self.assertIn(reverse("login"), self.driver.current_url)

    def test_get_request_unauthorized(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
