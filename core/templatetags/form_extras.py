from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def datetime_local_format(value):
    """
    Formatar datetime para o formato aceito pelo input datetime-local
    """
    if not value:
        return ''
    
    # Converter para timezone local se necessário
    if timezone.is_aware(value):
        local_dt = timezone.localtime(value)
    else:
        local_dt = value
    
    # Retornar no formato YYYY-MM-DDTHH:MM
    return local_dt.strftime('%Y-%m-%dT%H:%M')
