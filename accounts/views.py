from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

def home(request):
    if request.user.is_authenticated:
        return redirect("todo_list")
    #이게 이미 로그인된 상태라면~ 이거구나 
    return render(request, "accounts/home.html")
    #홈화면 제작

def signup(request):
    if request.user.is_authenticated:
        return redirect("todo_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        #사용자가 입력한 아이디와 비밀번호를Form에 넣는다

        if form.is_valid():#아이디 중복여부, 일치여부 규칙충족
            form.save()
            #DB에 저장하고 Django는 원문 저장않고 해시된 값을 저장
            return redirect("login")
            #가입 성공후 로그인페이지로 이동 
    else:
        form = UserCreationForm()
        #빈 회원가입 Form을 만든다

    return render(
        request,
        "registration/signup.html",
        {"form": form},
    )
