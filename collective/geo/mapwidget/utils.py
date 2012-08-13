import urllib
from Products.CMFCore import DirectoryView

def getProtocolFromRequest(request):
    """Determine which protocol layers should use for this request.

    Layers should, where possible, match the request protocol to avoid
    client browsers reporting errors to users.
    """
    server_url = request and request.get('SERVER_URL', '') or None
    return server_url and urllib.splittype(server_url)[0] or 'http'

def list_language_files():
    """ Returns a dictionary of available Openlayers translations.

    Keys are the language codes (lowercase, 2-4 in length).
    Values are the urls to the language files.
    """

    path = 'collective.geo.openlayers:skins/geo_openlayers/lang'
    urlbase = 'lang/'
    files = dict()
    
    info = DirectoryView._dirreg.getDirectoryInfo(path)
    
    if info:
        for key in info.getContents(DirectoryView._dirreg)[0].keys():
            files[key.replace('.js', '').lower()] = urlbase + key

    return files