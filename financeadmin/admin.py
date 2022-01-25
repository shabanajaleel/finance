from django.contrib import admin
from . models import project,partner,partnership,profit

# Register your models here.
admin.site.register(project)
admin.site.register(partner)
admin.site.register(partnership)
admin.site.register(profit)
