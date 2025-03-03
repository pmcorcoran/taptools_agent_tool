Taptools AI Agent Tool

A langchain tool for AI agents to gather information from the taptools API.

The four files currently in the repository are

- utility.py: the taptools api wrapper
- tool.py: used by the agent and calls functions from utility.py
- schema.json: The taptools openapi spec. This is used in utility.py for
api wrapper logic. And is given to the agent in tool.py so the agent
knows the information available and what endpoint and parameters
are needed to to request that information.
- non_nft_schema.json: same as schema.json but nft related endpoints are
removed to reduce input tokens. Recommended if you don't need NFT info.
- policy_and_hex.json: contains the policy id and hex name for
cardano native tokens. These values are required as parameters for certain
api calls. Currently only contains SNEK, more will be added. This is also
given to the agent in tool.py for the agent to use when parameters require
these values.

There will likely be more json files similar to policy_and_hex.json added
for use with other api parameters.
