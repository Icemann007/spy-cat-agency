from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from missions.models import Mission, Target
from missions.serializers import (
    MissionSerializer,
    MissionCreateSerializer,
    TargetUpdateSerializer,
    MissionAssignSerializer,
)


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.select_related("cat").prefetch_related("targets")

    def get_serializer_class(self):
        if self.action == "create":
            return MissionCreateSerializer

        return MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()

        if mission.cat is not None:
            return Response(
                {"detail": "Cannot delete a mission that is assigned to a cat"},
                status=status.HTTP_409_CONFLICT,
            )

        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        description="Assign an available spy cat to this mission",
        request=MissionAssignSerializer,
        responses={200: MissionSerializer},
    )
    @action(
        detail=True,
        methods=["PATCH"],
        url_path="assign",
        serializer_class=MissionAssignSerializer,
    )
    def assign_cat(self, request, pk=None):
        mission = self.get_object()

        serializer = self.get_serializer(
            instance=mission, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(MissionSerializer(mission).data)

    @extend_schema(
        description="Update a specific target (e.g., update notes or mark as complete) within this mission",
        request=TargetUpdateSerializer,
        responses={200: MissionSerializer},
        parameters=[
            OpenApiParameter(
                name="target_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the target to assign to this mission.",
            ),
        ],
    )
    @action(detail=True, methods=["PATCH"], url_path="targets/(?P<target_id>[^/.]+)")
    def update_target(self, request, pk=None, target_id=None):
        mission = self.get_object()

        try:
            target = mission.targets.get(pk=target_id)
        except Target.DoesNotExist:
            return Response(
                {"detail": "Target not found in this mission"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TargetUpdateSerializer(
            instance=target, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        if not mission.targets.filter(is_complete=False).exists():
            mission.is_complete = True
            mission.save()

        mission.refresh_from_db()

        return Response(MissionSerializer(mission).data)
