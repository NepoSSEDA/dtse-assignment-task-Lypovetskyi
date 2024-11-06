# Exception class for handling exceptions in situations when count of provided dataset columns is lower than required
class MissingMinimumAmountOfColumnsError(Exception):
    
    def __init__(self, columns_count = None):
        if columns_count is None:
            super().__init__('Missing minimum amount of required dataset columns (9 required)')
        else:
            super().__init__(f'Missing minimum amount of required dataset columns ({columns_count} provided, 9 required)')

# Exception class for handling exceptions in situations when mandatory column is missing in provided dataset
class MissingMandatoryColumnError(Exception):
    
    def __init__(self, column_name = None):
        if column_name is None:
            super().__init__(f'Missing mandatory dataset column')
        else:
            super().__init__(f'Missing mandatory \"{column_name}\" dataset column')

class CategoricalValueNotAllowed(Exception):

    def __init__(self, column_name, value, accepted):
        super().__init__(f'Categorical value \"{value}\" in column \"{column_name}\" is forbidden. Please use one of {str(accepted)}')