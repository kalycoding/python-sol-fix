from django.urls import path

from . import api, views

urlpatterns = [
    path('', views.candidates_list, name='candidate_list'),
    path('interviews/ics/<int:pk>/', views.candidate_ics_view, name='candidate_ics'),
    path('api/candidates', api.CandidateListAPI.as_view()),
]
