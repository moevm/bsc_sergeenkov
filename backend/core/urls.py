from django.urls import path

from core.views import (
    search_similar_questions
)


urlpatterns = [
    path('api/search-similar-questions', search_similar_questions),
]
