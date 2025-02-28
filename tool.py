"""Tool for the TapTools API."""

from typing import Optional, Any
import json
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import Field

from utility import TapToolsAPIWrapper


with open("schema.json") as f:
    taptools_spec = json.load(f)

with open("policy_and_hex.json", 'r') as f:
    policy_and_hex = json.load(f)

with open("reduced_schema.json") as f:
    taptools_reduced_spec = json.load(f)



class TapToolsAPIResults(BaseTool):  # type: ignore[override]
    """Tool that queries the taptools.io cardano blockchain API and returns JSON."""

    name: str = "taptoolsapi_results_json"
    description: str = (
        "TapTools API provided by taptools.io."
        "This tool is handy when you need to find information about the cardano blockchain "
        "The input should be an endpoint plus required or optional parameters if necessary "
        "and the output is a JSON object with the results."
        f"To see enpoints and their descriptions and parameters check out the reduced openapi json spec {taptools_reduced_spec}. "
        #f"The policy id and hex name for some tokens can be found here {policy_and_hex} "
    )
    api_wrapper: TapToolsAPIWrapper = Field(default_factory=TapToolsAPIWrapper)

    def _run(
        self,
        endpoint: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs
    ) -> dict:
        """Use the tool."""
        return self.api_wrapper.run(endpoint, **kwargs)

    async def _arun(
        self,
        endpoint: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        **kwargs
    ) -> dict:
        """Use the tool asynchronously."""
        return await self.api_wrapper.arun(endpoint, **kwargs)
