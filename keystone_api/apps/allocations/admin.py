"""Extends the builtin Django admin interface for the parent application.

Extends and customizes the site-wide administration utility with
interfaces for managing application database constructs.
"""

from django.conf import settings
from django.contrib import admin

from .models import *

settings.JAZZMIN_SETTINGS['icons'].update({
    'allocations.Cluster': 'fa fa-server',
    'allocations.Allocation': 'fas fa-coins',
    'allocations.AllocationRequest': 'fa fa-file-alt',
})

settings.JAZZMIN_SETTINGS['order_with_respect_to'].extend([
    'allocations.Cluster',
    'allocations.AllocationRequest',
    'allocations.Allocation'
])


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    """Admin interface for the `Cluster` model"""

    @admin.action
    def enable_selected_clusters(self, request, queryset) -> None:
        """Mark selected clusters as enabled"""

        queryset.update(enabled=True)

    @admin.action
    def disable_selected_clusters(self, request, queryset) -> None:
        """Mark selected clusters as disabled"""

        queryset.update(enabled=False)

    list_display = ['enabled', 'name', 'description']
    list_display_links = list_display
    ordering = ['name']
    list_filter = ['enabled']
    search_fields = ['name', 'description']
    actions = [enable_selected_clusters, disable_selected_clusters]


class AllocationRequestReviewInline(admin.StackedInline):
    """Inline admin interface for the `AllocationRequestReview` model"""

    model = AllocationRequestReview
    show_change_link = True
    readonly_fields = ('date_modified',)
    extra = 0


class AllocationInline(admin.TabularInline):
    """Inline admin interface for the `Allocation` model"""

    model = Allocation
    show_change_link = True
    extra = 0


@admin.register(AllocationRequest)
class AllocationRequestAdmin(admin.ModelAdmin):
    """Admin interface for the `AllocationRequest` model"""

    @staticmethod
    @admin.display
    def title(obj: AllocationRequest) -> str:
        """Return a request's title as a human friendly string"""

        return str(obj)

    @staticmethod
    @admin.display
    def reviews(obj: AllocationRequest) -> int:
        """Return the total number of request reviews"""

        return sum(1 for _ in obj.allocationrequestreview_set.all())

    @staticmethod
    @admin.display
    def approvals(obj: AllocationRequest) -> int:
        """Return the number of approving request reviews"""

        return sum(1 for review in obj.allocationrequestreview_set.all() if review.approve)

    list_display = ['group', title, 'submitted', 'approved', 'active', 'expire', 'reviews', 'approvals']
    list_display_links = list_display
    search_fields = ['title', 'description', 'group__name']
    ordering = ['submitted']
    list_filter = [
        ('submitted', admin.DateFieldListFilter),
        ('approved', admin.DateFieldListFilter),
        ('active', admin.DateFieldListFilter),
        ('expire', admin.DateFieldListFilter),
    ]
    inlines = [AllocationInline, AllocationRequestReviewInline]


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    """Admin interface for the `Allocation` model"""

    @staticmethod
    @admin.display
    def group(obj: Allocation) -> str:
        """Return the name of the group the allocation is assigned to"""

        return obj.request.group.name

    @staticmethod
    @admin.display
    def approved(obj: Allocation) -> bool:
        """Return whether the request for the allocation has been marked as approved"""

        return obj.request.approved or '--'

    @staticmethod
    @admin.display
    def requested(obj: Allocation) -> str:
        """Return the allocation's service units as a human friendly string"""

        return f'{obj.requested:,}'

    @staticmethod
    @admin.display
    def awarded(obj: Allocation) -> str:
        """Return the allocation's service units as a human friendly string"""

        return f'{obj.awarded:,}' if obj.awarded else '--'

    @staticmethod
    @admin.display
    def final_usage(obj: Allocation) -> str:
        """Return the allocation's final usage as a human friendly string"""

        return f'{obj.final:,}' if obj.final else '--'

    list_display = [group, 'request', 'cluster', requested, awarded, final_usage, approved]
    list_display_links = list_display
    ordering = ['request__group__name', 'cluster']
    search_fields = ['request__group__name', 'request__title', 'cluster__name']
    list_filter = [
        ('request__approved', admin.DateFieldListFilter)
    ]
