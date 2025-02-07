from django.urls import path, include
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),  # Include the accounts app URLs
        # OpenAPI schema:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Redoc:
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),   
]
