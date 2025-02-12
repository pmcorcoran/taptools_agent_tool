"""Tool for the TapTools API."""

from typing import Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import Field

from mytoolutility import TapToolsAPIWrapper


with open("schema.json") as f:
        taptools_spec = f



class TapToolsAPIResults(BaseTool):  # type: ignore[override]
    """Tool that queries the taptools.io cardano blockchain API and returns JSON."""

    name: str = "taptoolsapi_results_json"
    description: str = (
        "TapTools API provided by taptools.io."
        "This tool is handy when you need to find information about the cardano blockchain "
        "The input should be an endpoint plus required or optional parameters if necessary "
        "and the output is a JSON object with the results."
        f"to see enpoints and parameters check out the openapi json spec {taptools_spec}"
    )
    api_wrapper: TapToolsAPIWrapper = Field(default_factory=TapToolsAPIWrapper)

    def _run(
        self,
        endpoint: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return str(self.api_wrapper.run(endpoint))

    async def _arun(
        self,
        endpoint: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return (await self.api_wrapper.arun(endpoint)).__str__()