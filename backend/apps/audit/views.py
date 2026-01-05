"""
Views para auditoría.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import AuditLog, SecurityAlert
from .services import AuditService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_activity(request):
    """
    Obtiene actividad del usuario actual.
    
    GET /api/audit/my-activity/
    """
    logs = AuditService.get_user_activity(request.user)
    
    return Response({
        'logs': [
            {
                'event_type': log.event_type,
                'description': log.description,
                'created_at': log.created_at,
                'severity': log.severity
            }
            for log in logs
        ]
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_logs(request):
    """
    Obtiene todos los logs (solo admin).
    
    GET /api/audit/logs/
    """
    limit = int(request.query_params.get('limit', 100))
    event_type = request.query_params.get('event_type')
    
    logs = AuditLog.objects.all()
    if event_type:
        logs = logs.filter(event_type=event_type)
    logs = logs[:limit]
    
    return Response({
        'logs': [
            {
                'id': log.id,
                'event_type': log.event_type,
                'severity': log.severity,
                'user': log.user.username if log.user else None,
                'ip_address': log.ip_address,
                'description': log.description,
                'created_at': log.created_at
            }
            for log in logs
        ]
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def alerts(request):
    """
    Obtiene alertas de seguridad (solo admin).
    
    GET /api/audit/alerts/
    """
    unresolved_only = request.query_params.get('unresolved', 'true') == 'true'
    
    alert_list = AuditService.get_recent_alerts(resolved=not unresolved_only)
    
    return Response({
        'alerts': [
            {
                'id': alert.id,
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'description': alert.description,
                'is_resolved': alert.is_resolved,
                'created_at': alert.created_at
            }
            for alert in alert_list
        ]
    })
