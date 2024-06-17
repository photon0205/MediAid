from django.urls import path
from .views import DiagnoseView, SymptomSuggestionView

urlpatterns = [
    path('diagnose/', DiagnoseView.as_view(), name='diagnose'),
    path('symptoms/', SymptomSuggestionView.as_view(), name='symptoms'),
]
