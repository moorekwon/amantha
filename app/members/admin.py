from django.contrib import admin

# Register your models here.
from members.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRibbon)
class UserRibbonAdmin(admin.ModelAdmin):
    pass


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    pass


@admin.register(Pick)
class PickAdmin(admin.ModelAdmin):
    pass


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(UserIdealType)
class UserIdealTypeAdmin(admin.ModelAdmin):
    pass
