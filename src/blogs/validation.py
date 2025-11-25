def post_list_params(request, default_limit=10, max_limit=100, max_offset=10000):
    try:
        author_id = int(request.query_params.get('author_id'))
    except:
        author_id = None

    sort_by = request.query_params.get('sort_by', 'created_at')
    if sort_by not in ('title', 'created_at'):
        sort_by = 'created_at'

    sort_order = request.query_params.get('sort_order', 'desc').lower()
    if sort_order not in ('asc', 'desc'):
        sort_order = 'desc'

    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', default_limit))

    offset = max(0, min(offset, max_offset))
    limit = max(1, min(limit, max_limit))

    return author_id, sort_by, sort_order, offset, limit
