from django.contrib import admin

# Register your models here.
from members.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRibbon)
class UserRibbonAdmin(admin.ModelAdmin):
    pass


@admin.register(SendStar)
class SendStarAdmin(admin.ModelAdmin):
    pass


@admin.register(SendLike)
class SendLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(SelectStory)
class SelectStoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SelectTag)
class SelectTagAdmin(admin.ModelAdmin):
    pass
