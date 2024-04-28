from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('surveys/', include('surveys.urls', namespace='surveys')),
    path('accounts/logout/', LogoutView.as_view(next_page='surveys:login'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]