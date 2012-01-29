import urllib


def getProtocolFromRequest(request):
    """Determine which protocol layers should use for this request.

    Layers should, where possible, match the request protocol to avoid
    client browsers reporting errors to users.
    """
    server_url = request and request.get('SERVER_URL', '') or None
    return server_url and urllib.splittype(server_url)[0] or 'http'
