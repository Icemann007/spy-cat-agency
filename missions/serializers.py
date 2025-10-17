from rest_framework import serializers
from django.db import transaction

from cats.models import Cat
from missions.models import Target, Mission


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "name", "country", "notes", "is_complete"]
        read_only_fields = ["id", "is_complete"]


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = ["id", "cat", "is_complete", "created_at", "targets"]
        read_only_fields = ["id", "cat", "created_at"]

    def validate_is_complete(self, value):
        if not value:
            raise serializers.ValidationError("Cannot mark a mission as incomplete.")

        return value


class MissionCreateSerializer(serializers.ModelSerializer):
    MIN_TARGETS = 1
    MAX_TARGETS = 3

    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ["id", "targets"]
        read_only_fields = ["id"]

    def validate_targets(self, value):
        if not (self.MIN_TARGETS <= len(value) <= self.MAX_TARGETS):
            raise serializers.ValidationError(
                "A mission must have between 1 and 3 targets."
            )
        return value

    def create(self, validated_data):
        with transaction.atomic():
            targets_data = validated_data.pop("targets")
            mission = Mission.objects.create()

            for target_data in targets_data:
                Target.objects.create(mission=mission, **target_data)

            return mission


class MissionAssignSerializer(serializers.Serializer):
    cat_id = serializers.PrimaryKeyRelatedField(
        queryset=Cat.objects.all(), source="cat"
    )

    def validate(self, attrs):
        cat_to_assign = attrs.get("cat")

        if cat_to_assign:
            active_mission = Mission.objects.filter(
                cat=cat_to_assign, is_complete=False
            ).exists()

            if active_mission:
                raise serializers.ValidationError(
                    f"Cat '{cat_to_assign.name}' already has an active mission."
                )

        return attrs

    def update(self, instance, validated_data):
        instance.cat = validated_data.get("cat")
        instance.save()
        return instance


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["notes", "is_complete"]

    def validate(self, attrs):
        target = self.instance
        if "notes" in attrs and attrs["notes"] != target.notes:
            if target.is_complete:
                raise serializers.ValidationError(
                    {"notes": "Cannot update notes for a completed target"}
                )

            if target.mission.is_complete:
                raise serializers.ValidationError(
                    {"notes": "Cannot update notes for a completed mission"}
                )

        return attrs
