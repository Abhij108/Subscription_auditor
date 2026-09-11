from django.urls import path
from .views import AnalyzeCSVView

urlpatterns = [
    path("analyze/", AnalyzeCSVView.as_view(), name="analyze-csv"),
]