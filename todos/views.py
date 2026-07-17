from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo


#Django가 HTML Template을 완성해서 응답으로 만들어주는 render를 가져온다.
@login_required
@require_POST
def todo_toggle(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id,
    user=request.user,)
    #user 정보까지 포함, 객체가 있으면 반환 없으면 404

    todo.completed = not todo.completed
    todo.save()

    return redirect("todo_list")
# URL 에서 todo_id를 받아서 Todo를 DB에서 찾고 completed값을 반대로 변경 
# save에 값 업데이트 하고 redirect 즉 다음에 갈 주소 목록으로 이동
# 버튼을 누르면 상태가 바뀌게 하는 코드 
@login_required
#로그인한 사람인가 
@require_POST
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id,
    user = request.user,)#todo의 소유장니가 
    todo.delete()

    return redirect("todo_list")
# 삭제할 ID 받아서 delete로 삭제하고 목록으로 redirect

@login_required
def todo_list(request): #request는 사용자의 요청 정보
    todos = Todo.objects.filter(
        user=request.user,
    ).order_by("-created_at")
    #이게 filter를 로그인된 사용자를 기준으로 하는 거 

    context = {
        "page_title": "Todo List",
        "description": "오늘 할 일을 관리하는 페이지입니다.",
        "todos": todos,
    } # template 에서 사용할 이름 : 실제로 전달할 python 값

    return render(
        request,
        "todos/todo_list.html",
        context,
    )
# request, html파일, context 를 django에 연결한다.
# 이 render를 실행하면 Django가 해당 데이터를 HTML에 연결한다.   
# render의 세번째 인자에 딕셔너리 형태의 데이터가 들어간다. 
@login_required
def todo_create(request):
    if request.method =="POST":
        form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save(commit=False) 
            # 임시 todo 객체 만들고 = 이게 아직 저장하지 않은 model 객체를 반환함
            todo.user=request.user
            # 사용자와 연결
            form.save() # 즉시 db에 저장

            return redirect("todo_list")

    else:
        form = TodoForm()

    context = {
        "form": form,
    }
    return render(
        request,
        "todos/todo_form.html",
        context,
    )
