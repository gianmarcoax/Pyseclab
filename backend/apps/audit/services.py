"""
Servicio de logging centralizado.
"""
from django.utils import timezone
from .models import AuditLog, SecurityAlert


class AuditService:
    """Servicio para registrar eventos de auditoría."""
    
    BRUTE_FORCE_THRESHOLD = 5
    BRUTE_FORCE_WINDOW_MINUTES = 10
    
    @staticmethod
    def log(event_type: str, description: str, 
            user=None, request=None, severity='INFO', metadata=None):
        """Registra un evento de auditoría."""
        
        ip_address = None
        user_agent = ''
        
        if request:
            ip_address = AuditService._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        AuditLog.objects.create(
            event_type=event_type,
            severity=severity,
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            description=description,
            metadata=metadata or {}
        )
        
        # Verificar patrones sospechosos
        if event_type == 'LOGIN_FAILED':
            AuditService._check_brute_force(ip_address)
    
    @staticmethod
    def _get_client_ip(request):
        """Obtiene IP del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
    @staticmethod
    def _check_brute_force(ip_address):
        """Detecta ataques de fuerza bruta."""
        if not ip_address:
            return
        
        window_start = timezone.now() - timezone.timedelta(
            minutes=AuditService.BRUTE_FORCE_WINDOW_MINUTES
        )
        
        failed_attempts = AuditLog.objects.filter(
            event_type='LOGIN_FAILED',
            ip_address=ip_address,
            created_at__gte=window_start
        ).count()
        
        if failed_attempts >= AuditService.BRUTE_FORCE_THRESHOLD:
            # Crear alerta
            alert, created = SecurityAlert.objects.get_or_create(
                alert_type='BRUTE_FORCE',
                is_resolved=False,
                defaults={
                    'description': f'Posible ataque desde IP {ip_address}',
                    'severity': 'CRITICAL'
                }
            )
    
    @staticmethod
    def get_user_activity(user, limit=50):
        """Obtiene actividad reciente de un usuario."""
        return AuditLog.objects.filter(user=user)[:limit]
    
    @staticmethod
    def get_recent_alerts(resolved=False, limit=20):
        """Obtiene alertas recientes."""
        return SecurityAlert.objects.filter(is_resolved=resolved)[:limit]
