from django.db.models import Q

def filter_queryset(queryset, request):
    search_query = request.query_params.get('search', None)
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |  # For Artists & Genres
            Q(title__icontains=search_query)  # For Albums & Tracks
        )
    return queryset
