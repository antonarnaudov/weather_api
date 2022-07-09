from django.contrib.auth.models import User
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Extended
from core.utils.mixins import SerializerRequestSwitchMixin
from core.serializers import RegisterSerializer, UserSerializer, UserSimpleSerializer, \
    UpdateUserSerializer


class UserViewSet(SerializerRequestSwitchMixin, ModelViewSet):
    queryset = User.objects.all()
    serializers = {
        'show': UserSimpleSerializer,
        'create': RegisterSerializer,
        'update': UpdateUserSerializer,
        'detailed': UserSerializer
    }

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ('username',)
    ordering_fields = ''
    ordering = 'id'

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs['pk'] == '0':
            self.kwargs['pk'] = request.user.pk
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })
