from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listings_view, name="listings_view"),
    path("watchlist_view", views.watchlist_view, name="watchlist_view"),
    path("categories_view", views.categories_view, name="categories_view")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
