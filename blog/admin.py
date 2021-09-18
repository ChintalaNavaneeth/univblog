from django.contrib import admin

# Register your models here.


from .models import Post, Author, Categorie, subscribe, Contact, Comment, SubComment

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Categorie)
admin.site.register(subscribe)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(SubComment)
