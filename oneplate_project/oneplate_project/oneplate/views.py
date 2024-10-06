from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

class IndexView(APIView):
    def get(self, request):
        return Response({"message" : "This is the index page"})


# from allauth.account.views import SignupView
# from rest_framework.response import Response
# from rest_framework import status
# from allauth.account.forms import SignupForm
#
# class CustomSignupView(SignupView):
#     def post(self, request, *args, **kwargs):
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(request)
#             return Response({"detail": "회원가입이 성공적으로 완료되었습니다."}, status=status.HTTP_201_CREATED)
#         return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

'''
우선 구현해볼 로직
회원 가입 페이지 --> 프로필 작성 페이지 -->  이메일 인증 확인 알림
회원가입
유저모델 사용, 이메일, 비밀번호만 입력 이후 프로필 작성페이지로 이동
이때 프로필 작성페이지에 다른페이지 아무곳도 못감 그 계정으로 로그인 했을 땐 그 페이지만 나와야함
'''