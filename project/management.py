import os

class LocalFiles():

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
        for vendor in local_files.pages:
            for page in local_files.pages[vendor]:
                src = os.path.join(os.getcwd(), 'data', vendor, page)

                yield src