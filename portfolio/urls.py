from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('lstm-algorithm', views.lstm_algorithm, name="lstm_algorithm"),
    path('web-scraping', views.web_scraping, name="web_scraping"),
    path('decision-tree', views.decision_tree, name="decision_tree"),
    path('neural-network', views.neural_network, name="neural_network"),
    path('data-manipulation', views.data_manipulation, name="data_manipulation"),
]