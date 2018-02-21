class Urn(object):
    Schema = 'urn:'

    def __init__(self, nid: str, nss: str = None):
        if nss is None:
            index = nid.rindex(':')
            nss = nid[index+1:]
            nid = nid[len(Urn.Schema):index]

        self.nid = nid
        self.nss = nss
        self.value = nid + ':' + nss

    def __str__(self):
        return Urn.Schema + self.value


class UserUrn(Urn):
    def __init__(self, user: str):
        super(UserUrn, self).__init__('user', user)

