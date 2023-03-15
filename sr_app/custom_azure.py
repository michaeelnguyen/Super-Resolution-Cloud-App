from storages.backends.azure_storage import AzureStorage
from decouple import config

class AzureStaticStorage(AzureStorage):
    account_name = config('AZURE_ACCOUNT_NAME')
    account_key = config('AZURE_ACCOUNT_KEY')
    azure_container = 'static'
    expiration_secs = None

class AzureMediaStorage(AzureStorage):
    account_name = config('AZURE_ACCOUNT_NAME')
    account_key = config('AZURE_ACCOUNT_KEY')
    azure_container = 'media'
    expiration_secs = None