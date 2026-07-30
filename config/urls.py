from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("environment.urls")),
]

handler404 = "environment.views.custom_404"
handler500 = "environment.views.custom_500"