import os

class LocalFiles():

    def __init__(self):
        self.get_local_pages()

    def get_local_pages(self):
        """ Get folder (vendor) and file (html) list for pages in /data
            in the format {vendor: [page, ...], ...} """

        d = {}
        for vendor in os.listdir('data'):
            d[vendor] = ([file for file in os.listdir('data/{}'.format(vendor))
                if file[-4:] == 'html'])

        self.pages = d
        return d

    def yield_file_paths(self):
        """ get full file path and url """

        cwd = os.getcwd()
        for vendor in self.pages:
            vd = os.path.join(cwd, 'data', vendor)
            urls = open( os.path.join(vd, 'urls.txt'), 'r').readlines()

            for i, page in enumerate(self.pages[vendor]):
                url = urls[i]

                yield url, vd, page
