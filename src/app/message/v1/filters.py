import django_filters


class MessageFilter(django_filters.FilterSet):
    chat_id = django_filters.NumberFilter(required=True)
