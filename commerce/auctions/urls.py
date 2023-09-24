from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:pk>/", views.listing, name="listing"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("category/<str:category_req>",views.view_category, name="category"),
    path("wishlist/<int:pk>",views.wishlist_listing, name="wishlist_listing"),
    path("view_wishlist", views.view_wishlist, name="view_wishlist"),
    path("delete_wishlist/<int:pk>", views.delete_wishlist, name="delete_wishlist"),
    path('listing/<int:pk>/validate',views.validate_bid,name="validate")

]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
