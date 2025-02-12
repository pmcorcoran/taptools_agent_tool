from typing import Any, Dict, Optional
import aiohttp
import requests
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, ConfigDict, model_validator

with open("schema.json") as f:
        taptools_spec = f

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
    

    def _taptools_api_results(self, endpoint: str, **kwargs: Any):
        request_details = self._prepare_request(endpoint, **kwargs)
        response = requests.request(
            method=request_details["method"],
            url=request_details["url"],
            params=request_details["params"],
            headers=request_details["headers"],
        )       
        response.raise_for_status()
        return response.json()
    
    
    async def _async_taptools_api_results(self, endpoint: str, **kwargs: Any) -> dict:
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
    
    

    def _prepare_request(self, endpoint: str, **kwargs: Any) -> dict:
        method = self._get_request_method(endpoint)
        return {
            "method": method, 
            "url": "https://openapi.taptools.io/api/v1" + endpoint, 
            "headers": {
                "x-api-key": f"Bearer {self.taptools_api_key}",
            },
            "params": {
                #"q": input,
                **{key: value for key, value in kwargs.items() if value is not None}, ###figure out what this means
            },
        }
    
    #def results():
    #    return
    
    #@staticmethod
    #def _result_as_string(result: dict) -> str:
    #    return()
    
    def run(self, endpoint: str, **kwargs: dict) -> dict:
        return self._taptools_api_results(endpoint, **kwargs)
    
    async def arun(self, endpoint: str, **kwargs: dict) -> dict:
         results = await self._async_taptools_api_results(endpoint, **kwargs)
         return results
    
    def _get_request_method(endpoint):
        taptools_paths = taptools_spec['paths']
        method = taptools_paths['endpoint'].keys()[0]
        return method