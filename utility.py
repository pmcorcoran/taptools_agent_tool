from typing import Any, Dict, Optional
import aiohttp
import requests
import json
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, ConfigDict, model_validator

with open("schema.json", 'r') as f:
        taptools_spec = json.load(f)

with open("policy_and_hex.json", 'r') as f:
    policy_and_hex = json.load(f)


class TapToolsAPIWrapper(BaseModel):
    """
    Wrapper around TapTools API.

    To use you should have the environment variable 'TAPTOOLS_API_KEY'
    set with your API key, or pass 'taptools_api_key'
    as a named parameter to the constructor.

    Example:
        .. code-block:: python

           import TapToolsAPIWrapper
           taptoolsapi = TapToolsAPIWrapper()
    """

    taptools_api_key: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    
    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that API key exists in environment"""
        taptools_api_key = get_from_dict_or_env(
            values, "taptools_api_key", "TAPTOOLS_API_KEY"
        )
        values["taptools_api_key"] = taptools_api_key
        return values
    

    def _taptools_api_results(self, endpoint: str, **kwargs) -> dict:
        request_details = self._prepare_request(endpoint, **kwargs)
        print(request_details)
        response = requests.request(
            method=request_details["method"],
            url=request_details["url"],
            params=request_details["params"],
            headers=request_details["headers"],
        )       
        response.raise_for_status()
        return response.json()
    
    
    async def _async_taptools_api_results(self, endpoint: str, **kwargs) -> dict:
        """Use aiohttp to send request to TapTools API and return results async."""
        request_details = self._prepare_request(endpoint, **kwargs)
        if not self.aiosession:
            async with aiohttp.ClientSession() as session:
                if request_details['method'] == 'get':
                    async with session.get(
                        url=request_details["url"],
                        headers=request_details["headers"],
                        params=request_details["params"],
                        raise_for_status=True,
                    ) as response:
                        results = await response.json()
                else:
                    async with session.post(
                        url=request_details["url"],
                        headers=request_details["headers"],
                        params=request_details["params"],
                        raise_for_status=True,
                    ) as response:
                        results = await response.json()
        else:
            if request_details['method'] == 'get':
                async with self.aiosession.get(
                    url=request_details["url"],
                    headers=request_details["headers"],
                    params=request_details["params"],
                    raise_for_status=True,
                ) as response:
                    results = await response.json()
            else:
                async with self.aiosession.post(
                    url=request_details["url"],
                    headers=request_details["headers"],
                    params=request_details["params"],
                    raise_for_status=True,
                ) as response:
                    results = await response.json()

        return results
    
    

    def _prepare_request(self, endpoint: str, **kwargs) -> dict:
        method = self._get_request_method(endpoint)
        headers = {'x-api-key' : f"{self.taptools_api_key}"}
        params = self._get_headers(**kwargs)
        return {
            "method": method, 
            "url": "https://openapi.taptools.io/api/v1" + endpoint, 
            "headers": headers,
            "params": params,
        }
    

    
    def run(self, endpoint: str, **kwargs) -> dict:
        return self._taptools_api_results(endpoint, **kwargs)
    
    async def arun(self, endpoint: str, **kwargs) -> dict:
         results = await self._async_taptools_api_results(endpoint, **kwargs)
         return results
    
    def _get_request_method(self, endpoint: str) ->  str:
        taptools_paths = taptools_spec['paths']
        keys_list = list(taptools_paths[endpoint].keys())
        method = keys_list[0]
        return method
    
    def _get_headers(self, **kwargs):
        print(kwargs)
        headers = {}
        if kwargs is not None:
            for key, value in kwargs['kwargs'].items():
                headers[key] = str(value)
        return headers
        