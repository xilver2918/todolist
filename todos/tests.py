from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Todo


class TodoWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_list_splits_todos_by_state(self):
        today = timezone.localdate()
        active = Todo.objects.create(
            user=self.user,
            title="active todo",
            due_date=today + timedelta(days=1),
        )
        completed = Todo.objects.create(
            user=self.user,
            title="completed todo",
            due_date=today + timedelta(days=1),
            completed=True,
        )
        expired = Todo.objects.create(
            user=self.user,
            title="expired todo",
            due_date=today - timedelta(days=1),
        )

        response = self.client.get(reverse("todo_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["active_todos"]), [active])
        self.assertEqual(list(response.context["completed_todos"]), [completed])
        self.assertEqual(list(response.context["expired_todos"]), [expired])

    def test_create_edit_toggle_and_delete(self):
        create_response = self.client.post(
            reverse("todo_create"),
            {"title": "new todo", "due_date": "2026-07-20"},
        )
        self.assertRedirects(create_response, reverse("todo_list"))

        todo = Todo.objects.get(user=self.user, title="new todo")
        self.assertEqual(todo.due_date.isoformat(), "2026-07-20")

        edit_response = self.client.post(
            reverse("todo_edit", args=[todo.id]),
            {"title": "edited todo", "due_date": "2026-07-21"},
        )
        self.assertRedirects(edit_response, reverse("todo_list"))

        todo.refresh_from_db()
        self.assertEqual(todo.title, "edited todo")
        self.assertEqual(todo.due_date.isoformat(), "2026-07-21")

        toggle_response = self.client.post(reverse("todo_toggle", args=[todo.id]))
        self.assertRedirects(toggle_response, reverse("todo_list"))
        todo.refresh_from_db()
        self.assertTrue(todo.completed)

        delete_response = self.client.post(reverse("todo_delete", args=[todo.id]))
        self.assertRedirects(delete_response, reverse("todo_list"))
        self.assertFalse(Todo.objects.filter(id=todo.id).exists())