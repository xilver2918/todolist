from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import TodoForm
from .models import Todo


def _todo_list_url(params=None):
    url = reverse("todo_list")
    if params:
        url = f"{url}?{urlencode(params)}"
    return url


def _section_for(todo):
    if todo.completed:
        return "completed"
    if todo.is_expired:
        return "expired"
    return "active"


def _find_requested_todo(request, key):
    todo_id = request.GET.get(key)
    if not todo_id:
        return None

    try:
        todo_id = int(todo_id)
    except (TypeError, ValueError):
        return None

    return Todo.objects.filter(id=todo_id, user=request.user).first()


def _build_list_context(request, form=None, form_mode=None, form_todo=None):
    todos = list(
        Todo.objects.filter(user=request.user).order_by("due_date", "-created_at")
    )

    active_todos = []
    completed_todos = []
    expired_todos = []

    for todo in todos:
        section = _section_for(todo)
        if section == "completed":
            completed_todos.append(todo)
        elif section == "expired":
            expired_todos.append(todo)
        else:
            active_todos.append(todo)

    selected_todo = _find_requested_todo(request, "selected")
    edit_todo = _find_requested_todo(request, "edit")
    delete_todo = _find_requested_todo(request, "delete")
    status_todo = _find_requested_todo(request, "status")

    if form_mode is None and request.GET.get("action") == "create":
        form_mode = "create"
        form = TodoForm()

    if form_mode is None and edit_todo is not None:
        form_mode = "edit"
        form_todo = edit_todo
        form = TodoForm(instance=edit_todo)

    if selected_todo is None:
        selected_todo = form_todo or delete_todo

    selected_section = _section_for(selected_todo) if selected_todo else "active"

    status_target = "to do" if status_todo and status_todo.completed else "end to do"

    return {
        "page_title": "To Do List",
        "todos": todos,
        "active_todos": active_todos,
        "completed_todos": completed_todos,
        "expired_todos": expired_todos,
        "selected_todo": selected_todo,
        "selected_section": selected_section,
        "delete_todo": delete_todo,
        "status_todo": status_todo,
        "status_target": status_target,
        "form": form,
        "form_mode": form_mode,
        "form_todo": form_todo,
    }


@login_required
def todo_list(request):
    return render(request, "todos/todo_list.html", _build_list_context(request))


@login_required
def todo_create(request):
    if request.method != "POST":
        return redirect(_todo_list_url({"action": "create"}))

    form = TodoForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect("todo_list")

    return render(
        request,
        "todos/todo_list.html",
        _build_list_context(request, form=form, form_mode="create"),
    )


@login_required
def todo_edit(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if request.method != "POST":
        return redirect(_todo_list_url({"edit": todo.id}))

    form = TodoForm(request.POST, instance=todo)
    if form.is_valid():
        form.save()
        return redirect("todo_list")

    return render(
        request,
        "todos/todo_list.html",
        _build_list_context(request, form=form, form_mode="edit", form_todo=todo),
    )


@login_required
@require_POST
def todo_toggle(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save(update_fields=["completed"])
    return redirect("todo_list")


@login_required
@require_POST
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect("todo_list")