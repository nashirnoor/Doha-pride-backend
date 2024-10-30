"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking.views import BookingViewSet,BookingTransferViewSet,TransferBookingAuditViewSet
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from contact.views import ContactView
from ToursAndActivities.views import ToursAndActivitiesDetailView,ToursListView,TopActivitiesListView,TourBookingView
from about.views import StatisticListCreateAPIView,ActivityListCreateAPIView,DescriptionDetailView
from driver.views import AuthViewSet,BannerViewSet,DriverFeedbackViewSet,DriverViewSet,DriverProfile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'bookings-tour', BookingViewSet)
router.register(r'bookings-transfer', BookingTransferViewSet,basename='booking-transfer')
router.register(r'drivers', DriverViewSet, basename='drivers')
router.register('auth', AuthViewSet, basename='auth')
router.register('banners', BannerViewSet)
router.register('driver-feedback', DriverFeedbackViewSet)
router.register('transfer-audit', TransferBookingAuditViewSet)
router.register('driver-profile',DriverProfile,basename='driver-profile')


urlpatterns = [
    path('api/', include(router.urls)),
    path('',include('chat.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin', admin.site.urls),
    path('transfer-meet-assist/', views.TransferMeetAssistList.as_view(), name='transfer-meet-assist-list'),
    # path('transfer-meet-assist/<int:pk>/', views.TransferMeetAssistDetail.as_view(), name='transfer-meet-assist-detail'),
    path('contact/',  ContactView.as_view(), name='contact'),
    path('statistics/', StatisticListCreateAPIView.as_view(), name='statistic-list'),
    path('activities/', ActivityListCreateAPIView.as_view(), name='activity-list'),
    path('about-description/', DescriptionDetailView.as_view(), name='about-description'),
    path('tours/', ToursListView.as_view(), name='tours-list'),
    path('tours/<int:id>/', ToursAndActivitiesDetailView.as_view(), name='tour-detail'),
    path('top-activities/', TopActivitiesListView.as_view(), name='top-activities-list'),
    path('tour-booking/', TourBookingView.as_view(), name='tour-booking'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
