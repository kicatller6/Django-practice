from django.contrib import admin

from .models import Author ,Genre ,Book ,BookInstance,Language
admin.site.register(Language)
admin.site.register(Genre)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book

#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BooksInstanceInline]

#admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['last_name','first_name' ,'date_of_birth', 'date_of_death']
    inlines = [BooksInline]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

#admin.site.register(BookInstance)
@admin.register(BookInstance) #equals to register
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book','due_back','borrower','id','status')
    fieldsets = (
        (None, 
        {'fields': ('book','imprint', 'id')}
        ),
        ('Availability', 
        {'fields': ('status', 'due_back','borrower')}
        ),
    )


