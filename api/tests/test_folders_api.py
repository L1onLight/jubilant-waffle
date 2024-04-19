from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.tests.conftest import create_test_user, create_test_folder, create_test_todo
from core.models import TodoFolders, Todo

FOLDER_MANAGE_URL = reverse("folder_manage-list")
FOLDER_RETRIEVE_URL = reverse("folder_retrieve-list")


def get_detail(slug: int, todo_id: int = None, mode="r", ):
    if mode == "r":
        return reverse("folder_retrieve-detail", args=[slug])
    if mode == "rf":
        # Remove from folder
        return reverse("folder_manage-manage-todo-in-folder", args=[slug, todo_id])
    if mode == "af":
        # Add to folder
        return reverse("folder_manage-manage-todo-in-folder", args=[slug, todo_id])
    return reverse('folder_manage-detail', args=[slug])


class PublicFolderApiTests(TestCase):
    """Test unauthenticated API request."""

    def setUp(self):
        self.client = APIClient()
        self.test_user = create_test_user(email="testus@mail.ex")

        self.initial_folder_title = "Fixture TodoFolders Folder Title"
        self.folder = create_test_folder(user=self.test_user, folder_title=self.initial_folder_title)
        self.payload = {
            "folder_title": "TestTodoFolder",
        }

    def test_retrieve_folders_failed(self):
        """Test to retrieve all to-do folders unauthorized. Scenario negative: unauthorized"""
        # Given

        # When
        response = self.client.get(FOLDER_RETRIEVE_URL)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_folder_failed(self):
        """Test to retrieve specific to-do folder unauthorized. Scenario negative: unauthorized"""
        # Given

        # When
        response = self.client.get(get_detail(self.folder.slug))

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_folder_failed(self):
        """Test to create to-do folder unauthorized. Scenario negative: unauthorized"""
        # Given
        payload = self.payload

        # When
        response = self.client.post(FOLDER_RETRIEVE_URL, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        todos = TodoFolders.objects.all()
        self.assertEqual(len(todos), 1)

    def test_edit_folder_failed(self):
        """Test to edit to-do folders unauthorized. Scenario negative: unauthorized"""
        # Given
        payload = self.payload

        # When
        response = self.client.post(get_detail(self.folder.slug), payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        folder = TodoFolders.objects.get(pk=self.folder.id)
        folder.refresh_from_db()
        self.assertEqual(folder.folder_title, self.initial_folder_title)

    def test_partial_edit_folder_failed(self):
        """Test to partial edit to-do unauthorized. Scenario negative: unauthorized"""
        # Given
        payload = self.payload

        # When
        response = self.client.patch(get_detail(self.folder.slug), payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        folder = TodoFolders.objects.get(pk=self.folder.id)
        folder.refresh_from_db()
        self.assertEqual(folder.folder_title, self.initial_folder_title)

    def test_delete_folder_failed(self):
        """Test to delete to-do unauthorized. Scenario negative: unauthorized"""
        # Given

        # When
        response = self.client.delete(get_detail(self.folder.slug))

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        folder = TodoFolders.objects.get(pk=self.folder.id)
        folder.refresh_from_db()
        self.assertTrue(folder)

    def test_manage_todo_in_folder_failed(self):
        """Test to add/remove to-do to folder unauthorized. Scenario negative: unauthorized"""
        # Given
        todo_id = 999

        # When
        response_1 = self.client.put(get_detail(self.folder.slug, todo_id, "af"))
        response_2 = self.client.delete(get_detail(self.folder.slug, todo_id, "rf"))

        # Then
        self.assertEqual(response_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_2.status_code, status.HTTP_403_FORBIDDEN)


class PrivateFoldersApiTests(TestCase):
    """Test authenticated API request."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.test_user = create_test_user(email="testus@mail.ex")

        self.initial_folder_title = "Fixture TodoFolders Folder Title"
        self.test_folder = create_test_folder(self.test_user, folder_title=self.initial_folder_title)
        self.test_todo = create_test_todo(self.test_user)
        self.test_folder.todo_list.add(self.test_todo)

        self.payload = {
            "folder_title": "TestTodo",
        }

    def test_retrieve_todos_success(self):
        """Test to retrieve all to-do. Scenario success"""
        # Given

        # When
        response = self.client.get(FOLDER_RETRIEVE_URL)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_create_folder_success(self):
        """Test create folder. Scenario success"""
        # Given

        # When
        response = self.client.post(FOLDER_MANAGE_URL, self.payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_data = response.data
        self.assertGreater(json_data.get("id"), 0)
        self.assertEqual(json_data.get("folder_title"), self.payload["folder_title"])

    def test_add_todo_success(self):
        """Test add to-do to created folder. Scenario negative: Not found"""
        # Given
        todo = create_test_todo(self.user)
        folder = create_test_folder(self.user)

        # When
        response = self.client.put(get_detail(slug=folder.slug, todo_id=todo.id, mode="af"))

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        found = TodoFolders.objects.get(pk=folder.pk)
        self.assertEqual(found.todo_list.first().id, todo.id)
        self.assertEqual(len(found.todo_list.all()), 1)

    def test_remove_todo_success(self):
        """Test remove to-do from created folder. Scenario success"""
        # Given
        todo = create_test_todo(self.user)
        folder = create_test_folder(self.user)
        folder.todo_list.add(todo)

        # When
        response = self.client.delete(get_detail(slug=folder.slug, todo_id=todo.id, mode="rf"))

        # Then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        found = TodoFolders.objects.get(pk=folder.pk)
        self.assertEqual(len(found.todo_list.all()), 0)
        # Ensure that to-do still exists
        self.assertTrue(Todo.objects.filter(pk=todo.id).exists())

    def test_add_todo_failed(self):
        """Test add to-do to created folder. Scenario negative: Not found"""
        # Given
        todo = self.test_todo
        folder = create_test_folder(self.user)

        # When
        response = self.client.put(get_detail(slug=folder.slug, todo_id=todo.id, mode="af"))

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_folder_success(self):
        """Test retrieve specific to-do folder. Scenario success"""
        # Given
        folder = create_test_folder(self.user)

        # When
        response = self.client.get(get_detail(folder.slug))

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = response.data
        self.assertEqual(json_data["id"], folder.id)
        self.assertEqual(json_data["folder_title"], folder.folder_title)
        self.assertEqual(json_data["slug"], folder.slug)
        self.assertEqual(len(json_data["todo_list"]), len(folder.todo_list.all()))

    def test_retrieve_folder_failed(self):
        """Test to retrieve specific to-do folder authored by someone else. Scenario success: Not found"""
        # Given
        url = get_detail(self.test_folder.id)
        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_folder_success(self):
        """Test update specific to-do folder. Scenario success"""
        # Given
        folder = create_test_folder(self.user)
        new_payload = {
            "folder_title": "NewFolderTitle",
        }
        # When
        response = self.client.patch(get_detail(folder.slug, mode="m"), new_payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = response.data
        folder = TodoFolders.objects.get(pk=folder.id)
        self.assertEqual(json_data.get("folder_title"), folder.folder_title)

    def test_update_folder_failed(self):
        """Test update specific to-do folder authored by someone else. Scenario negative: Not found"""
        # Given
        folder = self.test_folder
        new_payload = {
            "folder_title": "NewFolderTitle",
        }
        # When
        response = self.client.patch(get_detail(folder.slug, mode="m"), new_payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        folder = TodoFolders.objects.get(pk=folder.id)
        self.assertEqual(folder.folder_title, self.initial_folder_title)

    def test_delete_folder_success(self):
        """Test delete specific to-do folder. Scenario success."""
        # Given
        folder = create_test_folder(self.user)

        # When
        response = self.client.delete(get_detail(folder.slug, mode="m"))

        # Then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        folder = TodoFolders.objects.filter(pk=folder.id)
        self.assertEqual(len(folder), 0)

    def test_delete_foreign_folder_failed(self):
        """Test delete to-do folder authored by someone else. Scenario negative: Not found"""
        # Given
        folder = self.test_folder

        # When
        response = self.client.delete(get_detail(folder.slug, mode='m'))

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        folder = TodoFolders.objects.filter(pk=folder.id)
        self.assertEqual(len(folder), 1)
