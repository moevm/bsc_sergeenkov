from django.urls import path

from core.views import (
    search_similar_questions,
    search_course_materials,
    mark_material_as_answer,
    ask_question_manual
)


urlpatterns = [
    path('api/search-similar-questions', search_similar_questions),
    path('api/search-course-materials', search_course_materials),
    path('api/mark-material-as-answer', mark_material_as_answer),
    path('api/ask-question-manual', ask_question_manual)
]
