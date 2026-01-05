"""
Modelos para auditoría de seguridad.
"""
from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """Log de eventos de seguridad."""
    
    EVENT_TYPES = [
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cierre de sesión'),
        ('LOGIN_FAILED', 'Login fallido'),
        ('REGISTER', 'Registro'),
        ('KEY_GENERATE', 'Generación de claves'),
        ('KEY_ROTATE', 'Rotación de claves'),
        ('ENCRYPT', 'Cifrado'),
        ('DECRYPT', 'Descifrado'),
        ('SIGN', 'Firma digital'),
        ('VERIFY', 'Verificación'),
        ('MESSAGE_SEND', 'Mensaje enviado'),
        ('MESSAGE_READ', 'Mensaje leído'),
    ]
    
    SEVERITY_LEVELS = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='INFO')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]


class SecurityAlert(models.Model):
    """Alertas de seguridad."""
    
    ALERT_TYPES = [
        ('BRUTE_FORCE', 'Ataque de fuerza bruta'),
        ('SUSPICIOUS_ACTIVITY', 'Actividad sospechosa'),
        ('UNAUTHORIZED_ACCESS', 'Acceso no autorizado'),
        ('KEY_COMPROMISE', 'Posible compromiso de clave'),
    ]
    
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, default='WARNING')
    description = models.TextField()
    related_logs = models.ManyToManyField(AuditLog, blank=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_alerts'
        ordering = ['-created_at']
