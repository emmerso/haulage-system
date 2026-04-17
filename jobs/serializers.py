from rest_framework import serializers
from .models import Job
from trucks.models import Truck
from drivers.models import Driver

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

    def validate(self, data):
        truck = data.get('assigned_truck')
        driver = data.get('assigned_driver')

        # Truck availability check
        if truck:
            if truck.status in ['IN_TRANSIT', 'UNDER_MAINTENANCE']:
                raise serializers.ValidationError(
                    {'assigned_truck': f'Truck is currently {truck.status} and cannot be assigned.'}
                )

        # Driver active job check
        if driver:
            active_jobs = Job.objects.filter(
                assigned_driver=driver,
                status='IN_TRANSIT'
            )
            # Exclude current job if updating
            if self.instance:
                active_jobs = active_jobs.exclude(pk=self.instance.pk)
            if active_jobs.exists():
                raise serializers.ValidationError(
                    {'assigned_driver': 'Driver already has an active job.'}
                )

        return data