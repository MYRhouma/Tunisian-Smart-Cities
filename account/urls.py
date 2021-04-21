from django.urls import path, include
from .views import OrganisationsInCategory, CategoryList, EntityInOrganism, DocumentUpload, messagesInbox, messagesSent, \
    dashboard, home, SendMessage

urlpatterns = [
    path('category/', CategoryList, name='CategoryList'),
    path('category/<int:cat>/', OrganisationsInCategory, name='OrganisationsInCategory'),
    path('organism/<int:org>/', EntityInOrganism, name='EntityInOrganism'),
    path('document/', DocumentUpload, name="DocumentUpload"),
    path('inbox/', messagesInbox, name="messagesInbox"),
    path('sent/', messagesSent, name="messagesSent"),
    path('send/', SendMessage, name="sendMessage"),
    path('',include('django.contrib.auth.urls')), #hedha lel login page
    path('dashboard/', dashboard, name="dashboard"),
    path('',home, name='home'),
]
