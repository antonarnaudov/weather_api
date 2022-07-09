class SerializerRequestSwitchMixin:
    """
    show is the default serializer
    serializers = {
        'show': ShowSerializer,
        'create': CreateSerializer,
        'update': UpdateSerializer,
        'detailed': RetrieveSerializer
    }
    """

    serializers = {}

    def get_serializer_class(self):
        if self.action == 'retrieve' \
                and 'detailed' in self.serializers.keys():
            return self.serializers['detailed']

        elif self.action in ['update', 'partial_update'] \
                and 'update' in self.serializers.keys():
            return self.serializers['update']

        elif self.action == 'create' \
                and 'create' in self.serializers.keys():
            return self.serializers['create']

        return self.serializers['show']
