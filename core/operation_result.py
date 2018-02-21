class OperationResult(object):
    @staticmethod
    def success(data):
        return OperationResult(True, data)

    @staticmethod
    def fail(data):
        return OperationResult(False, data)

    def __init__(self, success: bool, data):
        self.is_success = success
        self.data = data
