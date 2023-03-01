from fastapi import HTTPException, status, Security, Request
from fastapi.security import APIKeyHeader, APIKeyQuery

import os
import requests

# Define the name of query param to retrieve an API key from
api_key_query = APIKeyQuery(name="code", auto_error=False)
# Define the name of HTTP header to retrieve an API key from
api_key_header = APIKeyHeader(name="x-functions-key", auto_error=False)


def keys_from_azure_function(request: Request) -> list[str]:

    admin_url = str(request.url.replace(
        path='/admin/host/keys',
        scheme='http' if request.url.hostname == 'localhost' else 'https'
    ))
    
    keys_response = requests.get(f'{admin_url}', headers={
        'x-functions-key': os.getenv('FUNC_HOST_KEY', '')
    })
    
    return [key['value'] for key in keys_response.json()['keys']]
    

def get_api_key(
    request: Request,
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
):
    """Retrieve & validate an API key from the query parameters or HTTP header"""
    # If the API Key is present as a query param & is valid, return it
    
    api_keys = keys_from_azure_function(request=request)
    
    if api_key_query in api_keys:
        return api_key_query

    # If the API Key is present in the header of the request & is valid, return it
    if api_key_header in api_keys:
        return api_key_header

    # Otherwise, we can raise a 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
