import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer

logger = logging.getLogger('jobs')

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        job = serializer.save()
        logger.info(f'Job created: {job.job_id} - From {job.pickup_location} to {job.delivery_location}')

    def perform_destroy(self, instance):
        logger.info(f'Job deleted: {instance.job_id}')
        instance.delete()

    def update(self, request, *args, **kwargs):
        job = self.get_object()
        response = super().update(request, *args, **kwargs)

        job.refresh_from_db()
        if job.assigned_truck:
            truck = job.assigned_truck
            if job.status == 'IN_TRANSIT':
                truck.status = 'IN_TRANSIT'
            elif job.status in ['DELIVERED', 'CANCELLED']:
                truck.status = 'AVAILABLE'
            truck.save()

        logger.info(f'Job {job.job_id} status updated to: {job.status}')
        return response