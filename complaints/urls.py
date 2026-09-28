from django.urls import path

from .views import complaint_detail, complaint_list, health_check, predict_category


urlpatterns = [
    path("health/", health_check),
    path("predict/", predict_category),
    path("complaints/", complaint_list),
    path("complaints/<int:complaint_id>/", complaint_detail),
]