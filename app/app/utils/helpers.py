"""Helper methods."""


def get_data(request):
    """Get data from request."""
    data = None
    try:
        data = request.json
        if data == {} or data is None:
            data = request.data
    except:
        traceback.print_exc()
        data = {}

    return data
