from django.contrib import admin


from.models import Profile , EmailVerification
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
     list_display = ('user',)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(EmailVerification)
