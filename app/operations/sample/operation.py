from app.operations.baseOperation import BaseOperation


class SampleOperation(BaseOperation):
    """
        Change Sample word to your Operation name.
        Eg. Change Sample with "User".
        So classname is "UserOperation"
    """

    def application_name(self):
        """
            Return the name of your Operation.
            Eg. Change Sample with User
            So your return statement looks like
            return 'User'
        """
        return 'Sample'

    def _prepare_record(self):
        pass

    # Override any other methods from BaseOperation class
    # to customize the behaviour of CRUD methods
    # See sample in "ShopOperation" class
