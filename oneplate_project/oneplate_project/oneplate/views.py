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
from oneplate.serializers import (
    UserSerializer,
    ReviewSerializer,
    ReviewListSerializer,
    CommentSerializer,
    LikeSerializer,
    GenerateRecipeSerializer)
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from deep_translator import GoogleTranslator
import requests
import openai
'''
나중에 기본적인 CRUD 작업들은 viewset을 상속받아서 리팩토링해보기
'''

class ReviewPageNumberPagination(PageNumberPagination):
    page_size = 8

class IndexView(APIView):
    def get(self, request):
        # 최신 리뷰 4개 가져오기
        latest_reviews = Review.objects.all().order_by('-dt_created')[:4]
        serializer = ReviewListSerializer(latest_reviews, many=True)
        # JSON 응답으로 최신 리뷰 목록 반환
        return Response({"reviews": serializer.data})

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
            return Response({'detail': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 좋아요 추가
        like = Like.objects.create(user=user, content_type_id=model_type, object_id=object_id)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        like_id = kwargs.get('id')  # URL에서 전달된 좋아요 객체의 ID

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

# Generate-recipe
import base64
from django.conf import settings
from rest_framework.decorators import api_view
# OpenAI API 키 설정
openai.api_key = settings.OPENAI_API_KEY
@swagger_auto_schema(
    method='post',
    request_body=GenerateRecipeSerializer,
    responses={
        200: openapi.Response("Recipe generated successfully"),
        400: openapi.Response("Bad request"),
    },
)

@api_view(['POST'])
def GenerateRecipeAPIView(request):
    serializer = GenerateRecipeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ingredients = serializer.validated_data.get('ingredients', [])
    if not ingredients:
        return Response({"error": "재료가 제공되지 않았습니다."}, status=400)

    # GPT로 레시피 생성
    system_prompt = """
    Generate a creative recipe including a catchy title, based on the ingredients provided by the user. 
    Ensure the recipe is practical and the title reflects the dish's essence. 
    The recipe should begin with 'Title: ' followed by the recipe title
    """
    recipe_prompt = "Ingredients: " + ", ".join(ingredients)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": recipe_prompt},
        ]
    )

    recipe_text = response.choices[0].message["content"].strip()
    recipe_title = recipe_text.split('\n', 1)[0].strip()

    # DALL-E로 이미지 생성
    def create_visualization_prompt(recipe_title):
        clean_title = recipe_title.replace("Title: ", "")
        prompt = (f"'{clean_title}'라는 이름의 요리의 맛있고 현실감 있는 이미지를 만들어 주세요. "
                  "스튜디오 조명, 프로페셔널한 음식 사진 촬영 스타일로.")
        return prompt

    image_response = openai.Image.create(
        prompt=create_visualization_prompt(recipe_title),
        size="1024x1024",
    )
    image_url = image_response["data"][0]["url"]

    # 레시피 한글 번역
    translator = GoogleTranslator(source='auto', target='ko')
    translated_recipe = translator.translate(recipe_text)

    response = requests.get(image_url)
    base64EncodedImage = ''
    if response.status_code == 200:
        base64EncodedImage = ('data:' + response.headers["Content-Type"] + ';' +
                              "base64," + str(base64.b64encode(response.content).decode("utf-8")))

    return Response({
        "translated_recipe": translated_recipe,
        "image_url": image_url,
        'img_encoded': base64EncodedImage
    })
