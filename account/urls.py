from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from .views import OrganisationsInCategory, EntityInOrganism, messagesInbox, messagesSent, \
    dashboard, home, SendMessage, CategoryList, EditProfile, AddEntity

urlpatterns = [
    path('category/', CategoryList, name='CategoryList'),
    path('category/<int:cat>/', OrganisationsInCategory, name='OrganisationsInCategory'),
    path('organism/<int:org>/', EntityInOrganism, name='EntityInOrganism'),
    # path('document/', DocumentUpload, name="DocumentUpload"),
    path('inbox/', messagesInbox, name="messagesInbox"),
    path('sent/', messagesSent, name="messagesSent"),
    path('send/', SendMessage, name="sendMessage"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit/', EditProfile, name='editprofile'),
    path('dashboard/', dashboard, name="dashboard"),
    path('addentity/', AddEntity, name="AddEntity"),
    path('',home, name='home'),
]
