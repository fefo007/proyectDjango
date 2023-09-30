from django.contrib import admin
from .forms import ChangeTravelAdmin,ChangeToursAdmin
from .models import Messages,Travel,Order,Avatar,Tours


# Register your models here.
admin.site.register(Messages)
admin.site.register(Order)
admin.site.register(Travel,ChangeTravelAdmin)
admin.site.register(Avatar)
admin.site.register(Tours,ChangeToursAdmin)