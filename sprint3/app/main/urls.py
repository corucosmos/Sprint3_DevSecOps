from django.urls import path
from django.conf.urls.static import static

from main.views import debug_settings
from seng406_unsecure import settings as SETTINGS

from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("settings/", views.settings, name="settings"),
    path("payment-methods/", views.payment_methods, name="payment-methods"),
    path("analytics/", views.analytics, name="analytics"),
    path("profile/<int:user_id>/", views.user_profile, name='user-profile'),
    path("all-profiles/", views.all_profiles, name='all-profiles'),
    path("create-post/", views.create_post, name='create-post'),
    path("help/", views.help, name='help'),
    path("change-password/", views.change_password, name='change-password'),
    path("edit-profile/", views.edit_profile, name='edit-profile'),
    path("edit-address/", views.edit_address, name='edit-address'),
    path("debug-settings/", debug_settings, name="debug-settings"),
    path('events/', views.events, name='events')
]

urlpatterns += static(SETTINGS.MEDIA_URL, document_root=SETTINGS.MEDIA_ROOT)

handler404 = "main.views.custom_404_view"
handler500 = "main.views.custom_500_view"