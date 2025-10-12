from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client
import os
from typing import Optional

BEDROCK_MODEL_REGION = os.getenv("BEDROCK_MODEL_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "apac.anthropic.claude-3-5-sonnet-20241022-v2:0")

K8S_SYSTEM_PROMPT = """You are a Kubernetes operations assistant with access to cluster management tools.

Your capabilities:
- List and inspect pods across namespaces
- View all available namespaces in the cluster
- Retrieve and analyze pod logs for troubleshooting

Guidelines:
1. When users ask about pods, always specify which namespace you're checking
2. If namespace isn't mentioned, check the 'default' namespace first
3. For log requests, retrieve the last 100 lines by default unless specified
4. Provide concise, actionable information
5. If you encounter errors, explain them clearly and suggest alternatives
6. Format output in a readable way with proper structure
7. Proactively suggest relevant follow-up actions (e.g., "Would you like to check the logs?")

Example queries you can handle:
- "Show me all pods in the kube-system namespace"
- "What namespaces exist in this cluster?"
- "Get logs from pod nginx-xyz in default namespace"
- "Are there any failing pods?"
- "Show me the last 50 lines of logs from my-app pod"

Always be helpful, precise, and security-conscious when working with cluster resources."""


def initialize_k8s_agent() -> Optional[Agent]:
    """Initialize the Kubernetes agent with MCP tools."""
    try:
        server_params = StdioServerParameters(
            command="python",
            args=["k8s_mcp_server.py"]
        )

        mcp_client = MCPClient(lambda: stdio_client(server_params))
        
        mcp_client.__enter__()
        
        tools = mcp_client.list_tools_sync()
        
        if not tools:
            print("⚠️  Warning: No tools loaded from MCP server")
            return None
        
        print(f"✅ Successfully loaded {len(tools)} Kubernetes tools")

        bedrock_model = BedrockModel(
            model_id=BEDROCK_MODEL_ID,
            region_name=BEDROCK_MODEL_REGION
        )

        agent = Agent(
            model=bedrock_model,
            tools=tools,
            system_prompt=K8S_SYSTEM_PROMPT
        )
        
        return agent, mcp_client
        
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        return None


def print_welcome():
    """Print welcome message with usage examples."""
    print("\n" + "="*60)
    print("🚀 Kubernetes Operations Agent")
    print("="*60)
    print("\n📋 Example queries:")
    print("  • List all pods in default namespace")
    print("  • Show me namespaces")
    print("  • Get logs from pod <pod-name>")
    print("  • Check status of pods in kube-system")
    print("  • Show the last 50 lines of logs from <pod-name>")
    print("\n💡 Type 'exit' or 'quit' to end the session")
    print("="*60 + "\n")


def interactive_mode(agent: Agent):
    """Run the agent in interactive mode."""
    print_welcome()
    
    while True:
        try:
            user_query = input("🔍 Your query: ").strip()
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye! Shutting down Kubernetes agent...")
                break

            if not user_query:
                continue
            
            print("\n⏳ Processing...\n")
            response = agent(user_query)
            
            print("─" * 60)
            print("📊 Response:")
            print("─" * 60)
            print(response)
            print("─" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            continue


def main():
    """Main entry point."""

    result = initialize_k8s_agent()
    
    if result is None:
        print("Failed to initialize Kubernetes agent. Exiting...")
        return
    
    agent, mcp_client = result
    
    try:
        interactive_mode(agent)
    finally:
        # Cleanup MCP client
        try:
            mcp_client.__exit__(None, None, None)
            print("✅ MCP client closed successfully")
        except:
            pass


if __name__ == "__main__":
    main()