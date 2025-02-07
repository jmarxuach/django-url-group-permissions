from functools import wraps

def url_permission_required(view_func):
    """Decorator to mark views that require URL permission checking."""
    view_func.requires_url_permission = True
    return view_func