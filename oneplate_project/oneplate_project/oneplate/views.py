from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView)
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from oneplate.models import User,Review,Comment
from oneplate.serializers import UserSerializer, ReviewSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination

class ReviewPageNumberPagination(PageNumberPagination):
    page_size = 8

class IndexView(APIView):
    def get(self, request):
        return Response({"message" : "This is the index page"})

'''
Review
'''

class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPageNumberPagination

class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # 리뷰 생성 시 author를 현재 로그인한 사용자로 설정
        serializer.save(author=self.request.user)

class ReviewDetailView(RetrieveAPIView):
    queryset = Review.objects.all()  # 모든 리뷰를 쿼리셋으로 가져옴
    serializer_class = ReviewSerializer  # 리뷰 데이터를 직렬화하는 시리얼라이저
    lookup_field = 'review_id'  # URL에서 review_id를 사용
    permission_classes = [IsAuthenticatedOrReadOnly]  # 로그인하지 않은 사용자도 읽기만 가능

class ReviewUpdateView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'review_id'
    http_method_names = ['put']
    def perform_update(self, serializer):
        # 현재 로그인한 사용자가 작성자인지 확인
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You are not the author of this review.")
        serializer.save()

class ReviewDeleteView(DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'review_id'
    def perform_destroy(self, instance):
        # 현재 로그인한 사용자가 작성자인지 확인
        if self.request.user != instance.author:
            raise PermissionDenied("You are not the author of this review.")
        instance.delete()

'''
Comment
'''
class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated] # 댓글 생성은 로그인한 사용자만 가능

    def perform_create(self, serializer):
        # 리뷰 ID를 URL에서 가져와서 해당 리뷰에 댓글을 달도록 설정
        review_id = self.kwargs.get('review_id')
        review = Review.objects.get(review_id=review_id)

        # 댓글 작성자와 연결된 리뷰를 설정하고 저장
        serializer.save(author=self.request.user,review=review)

class CommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'comment_id'
    http_method_names = ['put']

    def perform_update(self, serializer):
        # 현재 로그인한 사용자가 댓글의 작성자인지 확인
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You are not the author of this review.")
        serializer.save()

class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'comment_id'

    def perform_destroy(self, instance):
        # 현재 로그인한 사용자가 댓글의 작성자인지 확인
        if self.request.user != instance.author:
            raise PermissionDenied("You are not the author of this review.")
        instance.delete()

'''
Profile
'''
class ProfileView(RetrieveAPIView):
    queryset = User.objects.all()  # 모든 사용자 쿼리셋
    serializer_class = UserSerializer   # 사용자 정보를 위한 시리얼라이저
    lookup_url_kwarg = 'user_id'  # URL에서 user_id 키로 기본 키 추출

    def get(self, request, *args, **kwargs):
        user = request.user
        profile_user_id = self.kwargs.get('user_id')
        profile_user = self.get_object()

        # 현재 사용자가 프로필의 사용자를 팔로우하는지 여부 확인
        '''
        is_following = False
        if user.is_authenticated:
            is_following = user.following.filter(id=profile_user_id).exists()
        '''

        # 프로필 사용자가 작성한 최신 리뷰 4개
        user_reviews = Review.objects.filter(author__id=profile_user_id)[:4]
        user_reviews_data = ReviewSerializer(user_reviews, many=True).data

        # 응답데이터 구성
        response_data = {
            'profile_user': UserSerializer(profile_user).data,  # 프로필 사용자 정보
            #'is_following': is_following,  # 팔로우 여부
            'user_reviews': user_reviews_data  # 리뷰 정보
        }
        return Response(response_data)


'''
이후 Profilesetmiddleware 만들어서 회원가입후 프로필 페이지에서 프로필 작성 완료전까지 못벗어나게하는 작업이 필요
상태코드 어떻게 처리할지가 고민 답글, 라이크, 팔로우 구현예정
'''
class UserProfileSetView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # 프로필 업데이트 처리
        response = super().update(request, *args, **kwargs)
        # 리다이렉트할 URL 생성 (index URL로 리다이렉트)
        redirect_url = reverse('index')  # 'index'는 URL name입니다.
        # 리다이렉트 응답 반환
        return Response({'redirect_url': redirect_url}, status=status.HTTP_302_FOUND)


class UserProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # 멀티파트 폼 데이터 파서 추가
    http_method_names = ['put']  # PATCH 메소드를 비활성화
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        success_url = reverse('profile', kwargs={'user_id': request.user.id})
        return Response({'detail': 'Profile updated successfully', 'success_url': success_url}, status=200)
    def get_object(self):
        return self.request.user

'''
우선 구현해볼 로직
회원 가입 페이지 --> 프로필 작성 페이지 -->  이메일 인증 확인 알림
회원가입
유저모델 사용, 이메일, 비밀번호만 입력 이후 프로필 작성페이지로 이동
이때 프로필 작성페이지에 다른페이지 아무곳도 못감 그 계정으로 로그인 했을 땐 그 페이지만 나와야함
'''