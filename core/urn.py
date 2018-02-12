class Urn(object):
    Schema = 'urn:'

    def __init__(self, nid: str, nss: str):
        self.nid = nid
        self.nss = nss
        self.value = nid + ':' + nss

    def __str__(self):
        return Urn.Schema + self.value

