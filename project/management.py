import os

class LocalFiles():
    """ If extracting from saved webpages (not recommended*), use format:
        ./data/vendor/page
        e.g. ./data/boots/some-product

    * Not recommended as saving webpage first loses some of the valuable styling
    """

    def __init__(self):
        self.data_dir = os.path.join(os.getcwd(), 'data')
        self.get_initial_urls()
        self.get_local_pages()

    def get_initial_urls(self):
        """ gets the list of urls to crawl """
        url_records = 'url_record.txt'
        init_urls = []
        for u in open(url_records, 'r').readlines():
            u = u.strip()
            if u:
                init_urls.append(u)
        self.init_urls = init_urls

    def get_local_pages(self):
        """ Get folder (vendor) and file (html) list for folders and pages
         in /data in the format {vendor: [page, ...], ...} """
        d = {}
        for vendor in os.listdir('data'):
            # ignore _screenshot folder. if more, just ignore folder[0] == '_'
            if vendor not in ('_screenshots',):
                d[vendor] = ([file for file in os.listdir('data/{}'
                    .format(vendor)) if file[-4:] == 'html'])

        self.pages = d
        return d


    def yield_file_paths(self):
        """ yield file path and url for local data """
        for vendor in self.pages:
            vd = os.path.join(self.data_dir, vendor)
            urls = open( os.path.join(vd, 'urls.txt'), 'r').readlines()

            for i, page in enumerate(self.pages[vendor]):
                url = urls[i]

                yield url, vd, page

    def add_url(self, vendor, url):
        """ adds a url to the urls.txt of specified vendor """
        urls = os.path.join(self.data_dir, vendor, 'urls.txt')
        with open(urls, 'a+') as f:
            f.write(url)
