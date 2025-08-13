# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', base, name='base'),
    
    path('signup/', register_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
    path('edit-profile/', edit_profile, name='edit_profile'),
 
    # Messaging
    path('send_message/', send_message, name='send_message'),
    path('inbox/', inbox, name='inbox'),

    # Feedback
    path('feedback/', submit_feedback, name='submit_feedback'),
    
    
    path('dashboard/', dashboard, name='dashboard'),
    
    path('summary/', summary_view, name='summary_view'),
    path('distribution/', sentiment_distribution_view, name='sentiment_distribution'),
    path('trend/', sentiment_trend_view, name='sentiment_trend'),
    path('health-terms/', health_terms_view, name='health_terms'),
    path('health_insight_dashboard/', health_insight_dashboard, name='health_insight_dashboard'),
    
    path("classify/",classify_text, name="classify_text"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

