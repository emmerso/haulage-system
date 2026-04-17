import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Driver
from .serializers import DriverSerializer

logger = logging.getLogger('drivers')

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def perform_create(self, serializer):
        driver = serializer.save()
        logger.info(f'Driver created: {driver.name} - License: {driver.license_number}')

    def perform_update(self, serializer):
        driver = serializer.save()
        logger.info(f'Driver updated: {driver.name}')

    def perform_destroy(self, instance):
        logger.info(f'Driver deleted: {instance.name}')
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        driver = self.get_object()
        active_jobs = driver.job_set.filter(status='IN_TRANSIT')
        if active_jobs.exists():
            return Response(
                {'error': 'Cannot delete a driver with an active job.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)