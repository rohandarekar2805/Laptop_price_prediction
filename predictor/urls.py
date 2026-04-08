from django.urls import path
from .views import PredictPriceAPI,  index_page

urlpatterns = [
    path('', index_page, name='home'),
    path('api/predict/', PredictPriceAPI.as_view(), name='predict_api'),
]