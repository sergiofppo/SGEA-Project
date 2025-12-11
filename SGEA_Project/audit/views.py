from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import AuditLog
from users.models import Usuario
from events.views import OrganizadorRequiredMixin 

class AuditLogListView(LoginRequiredMixin, OrganizadorRequiredMixin, ListView):
    model = AuditLog
    template_name = 'audit/audit_log_list.html'
    context_object_name = 'logs'
    paginate_by = 25

    def get_queryset(self):
        queryset = AuditLog.objects.all().select_related('user').order_by('-timestamp')
        query_date = self.request.GET.get('date')
        query_user = self.request.GET.get('user')

        if query_date:
            try:
                date_obj = datetime.strptime(query_date, '%Y-%m-%d').date()
                queryset = queryset.filter(timestamp__date=date_obj)
            except ValueError:
                messages.error(self.request, "Formato de data inválido. Use AAAA-MM-DD.")
        
        if query_user:
            queryset = queryset.filter(user__username__icontains=query_user)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_users'] = Usuario.objects.all().order_by('username')
        context['current_date'] = self.request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        context['current_user'] = self.request.GET.get('user', '')
        return context