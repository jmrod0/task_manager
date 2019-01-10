
from django.urls import path, include

urlpatterns = [
    path('', include('apps.helper_app.urls'))
]
