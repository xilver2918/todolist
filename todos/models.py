from django.db import models
from django.conf import settings

class Todo(models.Model): # 데이터 구조 만들기
# models.Model 상속받음 즉 Model 기능 상속받아서 사용할거임
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="todos",
    ) # 사용자 한명에게 todo 여러개가 연결됨 
    title = models.CharField(max_length=200)
    #문자열 최대길이 200이라는
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #생성 시각 로그 
    def __str__(self):
        return self.title
