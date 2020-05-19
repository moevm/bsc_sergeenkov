from django.urls import path

from core.views import (
    search_similar_questions,
    search_course_materials
)


urlpatterns = [
    path('api/search-similar-questions', search_similar_questions),
    path('api/search-course-materials', search_course_materials)
]
