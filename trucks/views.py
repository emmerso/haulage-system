import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Truck
from .serializers import TruckSerializer

logger = logging.getLogger('trucks')

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def perform_create(self, serializer):
        truck = serializer.save()
        logger.info(f'Truck registered: {truck.registration_number}')

    def perform_update(self, serializer):
        truck = serializer.save()
        logger.info(f'Truck updated: {truck.registration_number} - Status: {truck.status}')

    def perform_destroy(self, instance):
        logger.info(f'Truck deleted: {instance.registration_number}')
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        truck = self.get_object()
        if truck.status == 'IN_TRANSIT':
            return Response(
                {'error': 'Cannot delete a truck that is currently in transit.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)