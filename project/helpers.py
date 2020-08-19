from urllib.parse import urlparse, urlunparse

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    netloc_split = parsed_url[1].split('.')
    vendor = netloc_split[1] if 'www' in netloc_split else netloc_split[0]
    path = parsed_url[2]
    for nono in ('\\', '/', ':', '*', '?', '"', '<', '>', '|', '-', '.'):
        if nono in path:
            path = path.replace(nono, '')
    filename =  '{}{}'.format(vendor, path)
    print(filename)
    return vendor, filename

def link_in_netloc(netloc, link):
    parsed_link = urlparse(link)
    if parsed_link[1] == netloc:
        return urlunparse(parsed_link)

def parse_url(url):
    return urlparse(url)

def unparse_url(url):
    return urlunparse(url)
