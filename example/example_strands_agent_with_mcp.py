from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client
import os

BEDROCK_MODEL_REGION = os.getenv("BEDROCK_MODEL_REGION", "ap-south-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

bedrock_model = BedrockModel(model_id=BEDROCK_MODEL_ID, region_name=BEDROCK_MODEL_REGION)

system_prompt = "You are a greeting agent. You summarize the user input and what the tool has reponded"

def main():
    # Define MCP server parameters for stdio
    server_params = StdioServerParameters(
        command="python",
        args=["greeting_server.py"]
    )

    # Create MCPClient wrapping the stdio client connection
    mcp_client = MCPClient(lambda: stdio_client(server_params))

    # Connect and manage MCP client lifecycle synchronously
    with mcp_client:
        # Retrieve tools exposed by the MCP server synchronously
        tools = mcp_client.list_tools_sync()
        print("Available tools:", tools)

        # Create a Strands Agent instance with the discovered tools
        agent = Agent(model=bedrock_model,tools=tools, system_prompt=system_prompt)

        # Get the user input for the tool parameter
        name = input("Enter your name: ")

        # Use the agent to invoke the 'say-hello' tool synchronously
        response = agent(name)

        # Print the tool's response
        print("Agent response:", response)


if __name__ == "__main__":
    main()
