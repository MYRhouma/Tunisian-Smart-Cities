from django.contrib.auth.models import Group
from .models import Category, Entity, Organisme, Application, Message, Article, Admin, Document
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

admin.site.unregister(Group)


admin.site.register(Category)


admin.site.register(Entity)


class OrganismeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    fields = ('category','name', 'username','email','bio','is_superuser','is_staff')
    prepopulated_fields = {'username': ('name',)}
    list_filter = ['category','is_superuser','is_staff']
    class Meta:
        model=Organisme


admin.site.register(Organisme,OrganismeAdmin)


class CandidatureAdmin(admin.ModelAdmin):
    fields = ('category','name', 'username','email','bio','message','accepted')
    prepopulated_fields = {'username': ('name',)}
    list_filter = ['accepted',]
    class Meta:
        model=Application


admin.site.register(Application,CandidatureAdmin)

class MessageAdmin(admin.ModelAdmin):
    model = Message
    search_fields = ('msg_content','created_at')
admin.site.register(Message,MessageAdmin)


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ['title', 'author', 'published_at',]
    list_filter = ['author',]
    search_fields = ('title', 'content')
admin.site.register(Article,ArticleAdmin)
admin.site.register(Admin)


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ('__str__', 'uploaded_at')
admin.site.register(Document,DocumentAdmin)