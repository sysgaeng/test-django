import datetime
from pathlib import Path

from dotenv import load_dotenv
from gunicorn.http import wsgi

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


PROJECT_NAME = "#{PROJECT_NAME}"
SITE_NAME = "#{PROJECT_NAME}"
SITE_LOGO = "img/logo.png"  # app/staticfiles/static/img/logo.png 변경
DOMAIN = "domain.com"


class Response(wsgi.Response):
    def __init__(self, req, sock, cfg):
        super(Response, self).__init__(req, sock, cfg)
        self.version = PROJECT_NAME


wsgi.Response = Response


LOCAL_APPS = [
    "app.staticfile",
    "app.common.apps.CommonConfig",
    "app.chat.apps.ChatConfig",
    "app.message.apps.MessageConfig",
    "app.device.apps.DeviceConfig",
    "app.user.apps.UserConfig",
    "app.withdrawal_user.apps.WithdrawalUserConfig",
    "app.verifier.apps.VerifierConfig",
    "app.alarmtalk_log.apps.AlarmTalkLogConfig",
    "app.email_log.apps.EmailLogConfig",
    "app.push_log.apps.PushLogConfig",
    "app.sms_log.apps.SmsLogConfig",
    "app.celery_log.apps.CeleryLogConfig",
    "app.presigned_url.apps.PreSignedUrlConfig",
    "app.websocket_connection.apps.WebsocketConnectionConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_filters",
    "django_hosts",
    "drf_spectacular",
    "storages",
    "ckeditor",
    "ckeditor_uploader",
    "safedelete",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS

MIDDLEWARE = [
    "config.middleware.SwaggerLoginMiddleware",
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.RequestLogMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ko"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


# APPEND_SLASH
APPEND_SLASH = False

# AUTH_USER_MODEL
AUTH_USER_MODEL = "user.User"

# APPLICATION
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# HOST
DEFAULT_HOST = "api"
ROOT_HOSTCONF = "config.hosts"
ROOT_URLCONF = "config.urls.api"


# MODEL ID
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DATABASE ROUTER
DATABASE_ROUTERS = ["config.router.Router"]


# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}
SIMPLE_JWT_ALGORITHM = "HS256"


# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "app.common.authentication.Authentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "app.common.pagination.LimitOffsetPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "app.common.filter_backends.FilterBackend",
        "app.common.filter_backends.OrderingFilter",
    ],
    "EXCEPTION_HANDLER": "app.common.views.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "app.common.openapi.CustomAutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "NON_FIELD_ERRORS_KEY": "non_field",
    "ENABLE_LIST_MECHANICS_ON_NON_2XX": [400],
}


# SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": f"{SITE_NAME} API",
    "DESCRIPTION": f"""개발: [api.dev.{DOMAIN}](https://api.dev.{DOMAIN})<br/>운영: [api.{DOMAIN}](https://api.{DOMAIN})""",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/v[0-9]",
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "SORT_OPERATIONS": False,
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",
        "defaultModelRendering": "model",
        "defaultModelsExpandDepth": 0,
        "deepLinking": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
        "syntaxHighlight.activate": True,
        "syntaxHighlight.theme": "agate",
        "showExtensions": True,
        "filter": True,
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "Bearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": "/v1/user/login/",
                    },
                },
            },
        },
    },
    "SECURITY": [
        {
            "Bearer": [],
        }
    ],
    "PREPROCESSING_HOOKS": [
        "app.common.spectacular_hooks.api_ordering",
    ],
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    "COMPONENT_SPLIT_REQUEST": True,
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
}


# COOLSMS
COOLSMS_API_KEY = "**"
COOLSMS_API_SECRET = "**"
COOLSMS_FROM_PHONE = "**"


# MAILGUN
MAILGUN_API_KEY = "**"
MAILGUN_DOMAIN = "**"
MAILGUN_FROM_EMAIL = "**"


# ALARMTALK
ALARMTALK_PLUS_ID = "**"
ALARMTALK_ID = "**"
ALARMTALK_CLIENT_ID = "**"
ALARMTALK_CLIENT_SECRET = "**"


# CKEDITOR
CKEDITOR_UPLOAD_PATH = "ckeditor/"
CKEDITOR_CONFIGS = {
    "default": {
        "width": "100%",
    },
}


# CELERY
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = "Asia/Seoul"
CELERYD_SOFT_TIME_LIMIT = 300
CELERYD_TIME_LIMIT = CELERYD_SOFT_TIME_LIMIT + 60
CELERY_TASK_IGNORE_RESULT = True


# KAKAO
KAKAO_CLIENT_ID = "**"
KAKAO_CLIENT_SECRET = "**"
KAKAO_LOGIN_URL = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={kakao_client_id}&redirect_uri={SOCIAL_REDIRECT_URL}&state=kakao"

# NAVER
NAVER_CLIENT_ID = "**"
NAVER_CLIENT_SECRET = "**"
NAVER_LOGIN_URL = "https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={naver_client_id}&redirect_uri={SOCIAL_REDIRECT_URL}&state=naver"

# FACEBOOK
FACEBOOK_CLIENT_ID = "**"
FACEBOOK_CLIENT_SECRET = "**"
FACEBOOK_LOGIN_URL = "https://www.facebook.com/v9.0/dialog/oauth?response_type=code&client_id={facebook_client_id}&redirect_uri={SOCIAL_REDIRECT_URL}&state=facebook"

# GOOGLE
GOOGLE_CLIENT_ID = "**"
GOOGLE_CLIENT_SECRET = "**"
GOOGLE_LOGIN_URL = "https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&client_id={google_client_id}&redirect_uri={SOCIAL_REDIRECT_URL}&state=google&scope=openid"

# APPLE
APPLE_CLIENT_ID = "**"
APPLE_CLIENT_SECRET = """-----BEGIN PRIVATE KEY-----
**
-----END PRIVATE KEY-----"""
APPLE_KEY_ID = "**"
APPLE_TEAM_ID = "**"
APPLE_LOGIN_URL = "https://appleid.apple.com/auth/authorize?response_type=code&client_id={apple_client_id}&redirect_uri={SOCIAL_REDIRECT_URL}&state=apple"
