from django.contrib import admin
from .models import LoteBipagem

@admin.register(LoteBipagem)
class LoteBipagemAdmin(admin.ModelAdmin):
    list_display = ['id', 'criado_em', 'status', 'user_created', 'group_user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group_user__in=request.user.groups.all())