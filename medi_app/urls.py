from django.urls import path
from .views import (
    upload_product_image,
    create_rental_request,
    approve_rental_request,
    create_sub_rental_request,
    approve_sub_rental_request,
    get_dashboard,
    home,
    dash
)

urlpatterns = [
    path("",home,name="home"),
    path("dashboard/",dash,name="dash"),
    path("upload_product_image/", upload_product_image, name="upload_product_image"),
    path("create_rental_request/", create_rental_request, name="create_rental_request"),
    path("approve_rental_request/", approve_rental_request, name="approve_rental_request"),
    path("create_sub_rental_request/", create_sub_rental_request, name="create_sub_rental_request"),
    path("approve_sub_rental_request/", approve_sub_rental_request, name="approve_sub_rental_request"),
    path("get_dashboard/", get_dashboard, name="get_dashboard"),
]
