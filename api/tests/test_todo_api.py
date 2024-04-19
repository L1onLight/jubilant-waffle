import datetime

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.tests.conftest import create_test_user, create_test_todo, assert_time, format_time
from core.models import Todo

TODO_URL = reverse("todo-list")


def get_detail(todo_id: int):
    return reverse('todo-detail', args=[todo_id])


def get_detail_state(todo_id: int):
    return reverse("todo-change-state", args=[todo_id])


class PublicTodoApiTests(TestCase):
    """Test unauthenticated API request."""

    def setUp(self):
        self.client = APIClient()
        self.test_user = create_test_user(email="testus@mail.ex")

        self.initial_payload = {"title": "Test Todo Title", "until": timezone.now().date()}
        self.todo = Todo.objects.create(user=self.test_user, title=self.initial_payload["title"],
                                        until=self.initial_payload["until"])
        self.payload = {
            "title": "TestTodo",
            "until": "2024-04-12T12:26:42.569Z"
        }

    def test_retrieve_todos_failed(self):
        """Test to retrieve all to-do unauthorized. Scenario negative: unauthorized"""
        # Given

        # When
        response = self.client.get(TODO_URL)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_todo_failed(self):
        """Test to retrieve specific to-do unauthorized. Scenario negative: unauthorized"""
        # Given

        # When
        response = self.client.get(get_detail(self.todo.id))

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_todo_failed(self):
        """Test to create to-do unauthorized. Scenario negative: unauthorized"""
        # Given
        payload = self.payload

        # When
        response = self.client.post(TODO_URL, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        todos = Todo.objects.all()
        self.assertEqual(len(todos), 1)

    def test_edit_todo_failed(self):
        """Test to edit to-do unauthorized. Scenario negative: unauthorized"""
        # Given
        payload = self.payload

        # When
        response = self.client.post(get_detail(self.todo.id), payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        todo = Todo.objects.get(pk=self.todo.id)
        todo.refresh_from_db()
        self.assertEqual(todo.title, self.initial_payload["title"])
        self.assertEqual(todo.until, self.initial_payload["until"])

    def test_partial_edit_todo_failed(self):
        """Test to partial edit to-do unauthorized. Scenario negative: unauthorized"""
        # Given
        payload = self.payload

        # When
        response = self.client.patch(get_detail(self.todo.id), payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        todo = Todo.objects.get(pk=self.todo.id)
        todo.refresh_from_db()
        self.assertEqual(todo.title, self.initial_payload["title"])
        # self.assertEqual(*assert_time(self.initial_payload["until"], todo.until))
        self.assertEqual(todo.until, self.initial_payload["until"])

    def test_delete_todo_failed(self):
        """Test to delete to-do unauthorized. Scenario negative: unauthorized"""
        # Given

        # When
        response = self.client.delete(get_detail(self.todo.id))

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        todo = Todo.objects.get(pk=self.todo.id)
        todo.refresh_from_db()
        self.assertTrue(todo)

    def test_change_state_todo_failed(self):
        """Test to change state of to-do unauthorized. Scenario negative: unauthorized"""
        # Given
        payload = {
            "state": True
        }

        # When
        response = self.client.patch(get_detail_state(self.todo.id), payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        todo = Todo.objects.get(pk=self.todo.id)
        self.assertFalse(todo.is_completed)
        self.assertIsNone(todo.completed_at)


class PrivateTodoApiTests(TestCase):
    """Test authenticated API request."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.test_user = create_test_user(email="testus@mail.ex")

        self.initial_payload = {"title": "Test Todo Title", "until": timezone.now().date()}
        self.test_todo = Todo.objects.create(user=self.test_user, title=self.initial_payload["title"],
                                             until=self.initial_payload["until"])
        self.payload = {
            "title": "TestTodo",
            "until": (timezone.now() + datetime.timedelta(days=10)).date()
        }

    def test_retrieve_todos_success(self):
        """Test to retrieve all to-do. Scenario success"""
        # Given

        # When
        response = self.client.get(TODO_URL)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_create_todo_success(self):
        """Test create to-do. Scenario success"""
        # Given

        # When
        response = self.client.post(TODO_URL, self.payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json_data = response.data
        self.assertEqual(json_data.get("title"), self.payload["title"])
        self.assertEqual(datetime.datetime.fromisoformat(json_data.get("until")).date(),
                         self.payload["until"])

        self.assertTrue(json_data.get("id"))
        self.assertTrue(json_data.get("updated_at"))
        self.assertTrue(json_data.get("created_at"))
        self.assertFalse(json_data.get("is_completed"))
        self.assertIsNone(json_data.get("completed_at"))

    def test_retrieve_todo_success(self):
        """Test retrieve specific to-do. Scenario success"""
        # Given
        todo = create_test_todo(self.user)

        # When
        response = self.client.get(get_detail(todo.id))

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = response.data

        self.assertEqual(json_data.get("id"), todo.id)
        self.assertEqual(json_data.get("title"), todo.title)
        self.assertEqual(json_data.get("is_completed"), todo.is_completed)
        self.assertEqual(json_data.get("completed_at"), todo.completed_at)
        self.assertEqual(json_data.get("until"), todo.until)

    def test_retrieve_todo_failed(self):
        """Test to retrieve specific to-do authored by someone else. Scenario success: Not found"""
        # Given
        url = get_detail(self.test_todo.id)
        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_todo_success(self):
        """Test update specific to-do. Scenario success"""
        # Given
        todo = create_test_todo(self.user)
        new_payload = {
            "title": "NewTodoTitle",
            "until": (timezone.now() + datetime.timedelta(days=100)).date(),
            "is_completed": True
        }
        # When
        response = self.client.patch(get_detail(todo.id), new_payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = response.data
        todo = Todo.objects.get(pk=todo.id)
        self.assertEqual(json_data.get("title"), todo.title)
        self.assertEqual(*assert_time(json_data.get("until"), todo.until))

        self.assertFalse(todo.is_completed)
        self.assertIsNone(todo.completed_at)

    def test_update_todo_failed(self):
        """Test update specific to-do authored by someone else. Scenario negative: Not found"""
        # Given
        todo = self.test_todo
        new_payload = {
            "title": "NewTodoTitle",
            "until": timezone.now() + datetime.timedelta(days=100),
            "is_completed": True
        }
        # When
        response = self.client.patch(get_detail(todo.id), new_payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        todo = Todo.objects.get(pk=todo.id)
        self.assertEqual(todo.title, self.initial_payload.get("title"))
        self.assertEqual(todo.until, self.initial_payload.get("until"))

        self.assertFalse(todo.is_completed)
        self.assertIsNone(todo.completed_at)

    def test_change_state_todo_success(self):
        """Test change state of specific to-do. Scenario success"""
        # Given
        todo = create_test_todo(self.user)
        new_payload = {
            "title": "NewTodoTitle",
            "until": timezone.now() + datetime.timedelta(days=100),
            "state": True
        }

        # When
        response = self.client.patch(get_detail_state(todo.id), new_payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = response.data
        todo = Todo.objects.get(pk=todo.id)
        self.assertEqual(json_data.get("title"), self.payload.get("title"))

        self.assertTrue(todo.is_completed)
        self.assertTrue(todo.completed_at)

    def test_change_state_foreign_todo_failed(self):
        """Test change state of specific to-do authored by someone else. Scenario negative: Not found"""
        # Given
        todo = self.test_todo
        new_payload = {
            "title": "NewTodoTitle",
            "until": timezone.now() + datetime.timedelta(days=100),
            "state": True
        }

        # When
        response = self.client.patch(get_detail_state(todo.id), new_payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        todo = Todo.objects.get(pk=todo.id)
        self.assertEqual(todo.title, self.initial_payload.get("title"))

        self.assertFalse(todo.is_completed)
        self.assertIsNone(todo.completed_at)

    def test_delete_todo_success(self):
        """Test delete specific to-do. Scenario success."""
        # Given
        todo = create_test_todo(self.user)

        # When
        response = self.client.delete(get_detail(todo.id))

        # Then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        todo = Todo.objects.filter(pk=todo.id)
        self.assertEqual(len(todo), 0)

    def test_delete_foreign_todo_failed(self):
        """Test delete to-do authored by someone else. Scenario negative: Not found"""
        # Given
        todo = self.test_todo

        # When
        response = self.client.delete(get_detail(todo.id))

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        todo = Todo.objects.filter(pk=todo.id)
        self.assertEqual(len(todo), 1)

    def test_filter_todo_success_1(self):
        """Test retrieve to-do with filters. Scenario success"""
        # Given
        create_test_todo(self.user, is_completed=True)
        create_test_todo(self.user)
        filter_query_1 = "?completed=true"
        filter_query_2 = "?completed=false"

        # When
        response_1 = self.client.get(TODO_URL + filter_query_1)
        response_2 = self.client.get(TODO_URL + filter_query_2)

        # Then
        self.assertNotEqual(
            response_1.data["results"][0],
            response_2.data["results"][0]
        )
        self.assertTrue(
            response_1.data["results"][0]["is_completed"],
        )
        self.assertFalse(
            response_2.data["results"][0]["is_completed"],
        )

    def test_filter_todo_success_2(self):
        """Test retrieve to-do with filters. Scenario success"""
        # Given
        initial_time = timezone.now()
        until_1 = initial_time + datetime.timedelta(days=5)
        until_2 = initial_time - datetime.timedelta(days=15)

        create_test_todo(self.user, is_completed=True, until=format_time(until_1))
        create_test_todo(self.user, until=format_time(until_2))
        filter_query_1 = f"?end_date={format_time(until_1)}"
        filter_query_2 = f"?end_date={format_time(until_2)}"
        # When
        response_1 = self.client.get(TODO_URL + filter_query_1)
        response_2 = self.client.get(TODO_URL + filter_query_2)
        # Then
        self.assertNotEqual(
            response_1.data["results"][0],
            response_2.data["results"][0]
        )
