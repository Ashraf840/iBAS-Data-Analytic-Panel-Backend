# from django.db.models import Q
# import operator
# from functools import reduce
from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned


# TODO: Need to make the multiple lookup_fields CASE-INSENSITIVE in terms of string-value as query-params
class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends further
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

        # # SHOULD NOT USE THE FLLOWING CODE-BLOCK, SINCE THIS MIXIN IS MEANT FOR RETURNING SINGLE OBJECT. FOR GETTING MULTIPLE RECORDS, USE DJANGO-FILTER.
        # try:
        #     obj = get_object_or_404(queryset, **filter)  # Lookup single object
        #     self.check_object_permissions(self.request, obj)
        #     return obj
        # # [Resource]
        # #   - [MultipleObjectsReturned] https://stackoverflow.com/a/65017689
        # #   - [get_list (from ques sample)] https://stackoverflow.com/q/12950250
        # #   - [get_list (Doc)] https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#get-list-or-404
        # except MultipleObjectsReturned as MOR:
        #     obj_list = get_list_or_404(queryset, **filter)
        #     self.check_object_permissions(self.request, obj_list)
        #     return obj_list
        #     # print('*'*50)
        #     # print(f"{'-'*5}>MultipleObjectsReturned")
        #     # print('*' * 50)
