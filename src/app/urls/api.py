from django.urls import include, path

urlpatterns = [
    path("v1/", include("app.user.v1.urls")),
    path("v1/", include("app.presigned_url.v1.urls")),
    path("v1/", include("app.verifier.v1.urls")),
    path("v1/", include("app.chat.v1.urls")),
    path("v1/", include("app.message.v1.urls")),
    path("v1/", include("app.websocket_connection.v1.urls")),
]
