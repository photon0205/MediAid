from django.contrib import admin
from django.urls import path
from diagnosis.views import DiagnoseAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/diagnose/', DiagnoseAPIView.as_view(), name='diagnose-api'),
]
