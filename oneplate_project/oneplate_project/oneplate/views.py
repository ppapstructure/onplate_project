from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from oneplate.models import User,Review
from oneplate.serializers import UserSerializer, ReviewSerializer
from rest_framework.pagination import PageNumberPagination

class ReviewPageNumberPagination(PageNumberPagination):
    page_size = 8

class IndexView(APIView):
    def get(self, request):
        return Response({"message" : "This is the index page"})


# Review 작성
class ReviewList(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPageNumberPagination
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # 리뷰 생성 시 author를 현재 로그인한 사용자로 설정
        serializer.save(author=self.request.user)


class UserProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # 멀티파트 폼 데이터 파서 추가
    http_method_names = ['put']  # PATCH 메소드를 비활성화
    def get_object(self):
        return self.request.user




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