"""Serializers for casting database models to/from JSON and XML representations.

Serializers handle the casting of database models to/from HTTP compatible
representations in a manner that is suitable for use by RESTful endpoints.
They encapsulate object serialization, data validation, and database object
creation.
"""

from rest_framework import serializers

from .models import *


class ClusterSerializer(serializers.ModelSerializer):
    """Object serializer for the `Cluster` class"""

    class Meta:
        model = Cluster
        fields = '__all__'


class AllocationSerializer(serializers.ModelSerializer):
    """Object serializer for the `Allocation` class"""

    class Meta:
        model = Allocation
        fields = '__all__'


class ProposalSerializer(serializers.ModelSerializer):
    """Object serializer for the `Proposal` class"""

    class Meta:
        model = Proposal
        fields = '__all__'
