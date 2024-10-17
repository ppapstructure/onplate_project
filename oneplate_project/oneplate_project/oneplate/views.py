from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from rest_framework import status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView)
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from oneplate.models import User,Review,Comment,Like
from oneplate.serializers import UserSerializer, ReviewSerializer, ReviewListSerializer,CommentSerializer, LikeSerializer
from rest_framework.pagination import PageNumberPagination

'''
나중에 기본적인 CRUD 작업들은 viewset을 상속받아서 리팩토링해보기
'''

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
    serializer_class = ReviewListSerializer
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
Like
'''
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        user = request.user
        content_type_id = request.data.get('content_type_id')
        object_id = request.data.get('object_id')

        # ContentType을 통해 객체 타입 가져오기 (숫자 ID로 검색)
        try:
            model_type = ContentType.objects.get(id=content_type_id)
        except ContentType.DoesNotExist:
            return Response({'detail': '잘못된 content_type ID입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 좋아요 대상 객체 가져오기 - 모델에 따라 다르게 처리
        if model_type.model == 'review':
            # Review 모델의 경우 review_id 필드를 사용
            like_object = model_type.get_object_for_this_type(review_id=object_id)
        elif model_type.model == 'comment':
            # Comment 모델의 경우 id 필드를 사용
            like_object = model_type.get_object_for_this_type(comment_id=object_id)

        # 이미 좋아요가 눌려있는지 확인
        if Like.objects.filter(user=user, content_type_id=model_type, object_id=object_id).exists():
            return Response({'deail': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 좋아요 추가
        like = Like.objects.create(user=user, content_type_id=model_type, object_id=object_id)

        # 만약 댓글에 대한 좋아요라면, 해당 댓글이 어느 리뷰에 속한 댓글인지 반환
        '''
        if model_type.model == 'comment':
            comment = Comment.objects.get(comment_id=object_id)
            review_id = comment.review.review_id  # 댓글이 달린 리뷰의 ID 가져오기

            return Response({
                'like': LikeSerializer(like).data,
                'message': f'댓글 {object_id}에 좋아요를 추가했습니다.',
                'review_id': review_id  # 댓글이 속한 리뷰의 ID 정보 추가
            }, status=status.HTTP_201_CREATED)
        '''
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        like_id = kwargs.get('pk')  # URL에서 전달된 좋아요 객체의 ID

        # Like 객체를 조회하여 삭제할 대상 찾기
        try:
            like = Like.objects.get(id=like_id, user=user)  # 사용자에 속한 좋아요만 삭제 가능
        except Like.DoesNotExist:
            return Response({'detail': '좋아요가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 좋아요 삭제
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserLikedReviewsView(ListAPIView):
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # ContentType 객체에서 리뷰 모델에 해당하는 content_type 가져오기
        review_content_type = ContentType.objects.get_for_model(Review)

        # 유저가 좋아요한 리뷰들의 ID (object_id)를 가져옴
        liked_review_ids = Like.objects.filter(
            user=user,
            content_type_id=review_content_type.id
        ).values_list('object_id', flat=True)

        # 해당 object_id에 해당하는 리뷰를 가져옴
        return Review.objects.filter(review_id__in=liked_review_ids)




# Like의 경우
# 나중에 객체로 반환받는걸로 리팩토링해야겠다

# class LikeViewSet(viewsets.ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['post', 'delete', 'get']
#
#     def create(self, request, *args, **kwargs):
#         user = request.user
#         content_type = request.data.get('content_type_id')
#         object_id = request.data.get('object_id')
#
#         # ContentType을 문자열로 받아 처리
#         if content_type not in ['review', 'comment']:
#             return Response({'detail': '잘못된 content_type입니다.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # ContentType 객체 가져오기
#         model_type = ContentType.objects.get(model=content_type)
#
#         # 좋아요 대상 객체 가져오기
#         try:
#             if content_type == 'review':
#                 like_object = Review.objects.get(review_id=object_id)
#             elif content_type == 'comment':
#                 like_object = Comment.objects.get(comment_id=object_id)
#         except (Review.DoesNotExist, Comment.DoesNotExist):
#             return Response({'detail': f'해당 {content_type}을(를) 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
#
#         # 이미 좋아요가 눌려있는지 확인
#         if Like.objects.filter(user=user, content_type=model_type, object_id=object_id).exists():
#             return Response({'detail': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # 좋아요 추가
#         like = Like.objects.create(user=user, content_type=model_type, object_id=object_id)
#
#         response_data = LikeSerializer(like).data
#         if content_type == 'comment':
#             response_data['review_id'] = like_object.review.review_id
#
#         return Response(response_data, status=status.HTTP_201_CREATED)
#
#     def destroy(self, request, *args, **kwargs):
#         user = request.user
#         like_id = kwargs.get('pk')
#
#         try:
#             like = Like.objects.get(id=like_id, user=user)
#         except Like.DoesNotExist:
#             return Response({'detail': '좋아요가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
#
#         like.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
