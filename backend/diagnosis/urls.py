from django.urls import path
from .views import DiagnoseView, OpenAIView, SymptomSuggestionView

urlpatterns = [
    path('diagnose/', DiagnoseView.as_view(), name='diagnose'),
    path('symptoms/', SymptomSuggestionView.as_view(), name='symptoms'),
    path('openai/', OpenAIView.as_view(), name='openai'),
]
