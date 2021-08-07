from rest_framework import viewsets, mixins
from .models import Solution
from .serializers import SolutionSerializer


class SolutionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
