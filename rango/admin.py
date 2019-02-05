from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

  # Class for customising the admin interface with slugs 
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)} 


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)

# Changing the view of the admin page - I mean, hopefully. 


