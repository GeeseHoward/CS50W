from django.contrib import admin
from .models import CategoryA, CategoryB, CategoryC, Listing, Comment, Bid

# Register your models here. admin.site.register(Flight)
admin.site.register(CategoryA)
admin.site.register(CategoryB)
admin.site.register(CategoryC)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
