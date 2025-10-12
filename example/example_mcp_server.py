from mcp.server import FastMCP  # Import the MCP server framework from the library

# Create an MCP server instance with a descriptive name.
# This object manages the server's tools, resources, and prompts.
mcp = FastMCP("greeting-server")

# Decorator that registers the following function as an MCP tool.
# Tools are callable functions that can be invoked by the LLM.
@mcp.tool("say-hello")
def say_hello(name: str) -> dict:
    # When called, this tool returns a greeting message.
    # The message is formatted as a dictionary with 'content' indicating the message type.
    return {
        "content": [
            {
                "type": "text",
                # The greeting dynamically includes the name passed as an argument.
                "text": f"Hello, {name}! This is the greeting MCP server."
            }
        ]
    }

# The following code executes when the script runs directly.
if __name__ == "__main__":
    # Starts the MCP server and listens for incoming requests.
    # 'transport="stdio"' indicates communication via standard input/output, suitable for local testing.
    mcp.run(transport="stdio")
