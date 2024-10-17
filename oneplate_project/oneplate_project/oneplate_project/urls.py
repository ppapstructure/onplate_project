from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from dj_rest_auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import UserDetailsView
from drf_yasg.utils import swagger_auto_schema

# UserDetailsView의 특정 메소드를 숨기는 데코레이터 적용
hidden_methods = swagger_auto_schema(auto_schema=None)
# UserDetailsView.get = hidden_methods(UserDetailsView.get)
UserDetailsView.put = hidden_methods(UserDetailsView.put)
UserDetailsView.patch = hidden_methods(UserDetailsView.patch)

schema_view = get_schema_view(
   settings.SWAGGER_SETTINGS['DEFAULT_INFO'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Django FAQ에서 권유해준 방식
from dj_rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
            PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # admin
    path('admin/', admin.site.urls),
    # oneplage
    path('', include('oneplate.urls')),
    # # alluath
    # path('', include('allauth.urls')),

    # dj_rest_auth 기본 설정
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/signup/', include('dj_rest_auth.registration.urls')),  # 회원가입 엔드포인트
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# swggerui & redoc
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),]
