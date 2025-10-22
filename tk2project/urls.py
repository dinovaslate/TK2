from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('ragaspace.urls', 'ragaspace'), namespace='ragaspace')),
]
