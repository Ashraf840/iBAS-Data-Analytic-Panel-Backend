# from django.db.models import Q
# import operator
# from functools import reduce
from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)  # Apply any filter backends further
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

        # try:
        #     obj = get_object_or_404(queryset, **filter)  # Lookup single object
        #     self.check_object_permissions(self.request, obj)
        #     return obj
        # except MultipleObjectsReturned as MOR:
        #     obj_list = get_list_or_404(queryset, **filter)
        #     self.check_object_permissions(self.request, obj_list)
        #     return obj_list
        #     # print('*'*50)
        #     # print(f"{'-'*5}>MultipleObjectsReturned")
        #     # print('*' * 50)
