# Agentic Kubernetes Management

> Strands AI agent using MCP servers to expose Kubernetes tools (pods, namespaces, logs) for natural language cluster management.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kubernetes](https://img.shields.io/badge/kubernetes-1.20+-326CE5.svg)](https://kubernetes.io/)

## 🌟 Features

- **Natural Language Interface** - Manage Kubernetes clusters using conversational AI
- **MCP Protocol** - Leverages Model Context Protocol for extensible tool integration
- **Strands Framework** - Built on Strands AI agent framework for robust agentic behavior
- **AWS Bedrock Integration** - Powered by Claude models via Amazon Bedrock
- **Real-time Operations** - List pods, inspect namespaces, and retrieve logs instantly
- **Context-Aware** - Maintains conversation history for intelligent follow-up queries
- **Production Ready** - Error handling, graceful shutdown, and comprehensive logging

## 🏗️ Architecture

```
┌─────────────────┐
│   User Input    │
│ (Natural Lang)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Strands Agent  │
│  (Claude Model) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MCP Server    │
│ (Tool Provider) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Kubernetes API  │
│                 │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- Kubernetes cluster access (kubeconfig configured)
- AWS credentials configured for Bedrock access
- Anthropic model enabled

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Agentic-Kubernetes-Management.git
cd Agentic-Kubernetes-Management
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
export BEDROCK_MODEL_REGION="us-east-1"
export BEDROCK_MODEL_ID="apac.anthropic.claude-3-5-sonnet-20241022-v2:0"
```

4. **Verify Kubernetes access**
```bash
kubectl cluster-info
```

5. **Run the agent**
```bash
python agent.py
```

## 💬 Usage Examples

### Basic Queries

```
🔍 Your query: Show me all namespaces
📊 Response: Found 5 namespaces:
- default (Active)
- kube-system (Active)
- kube-public (Active)
- monitoring (Active)
- production (Active)
```

```
🔍 Your query: List pods in the production namespace
📊 Response: Found 12 pods in namespace 'production':
- nginx-deployment-7d8f9c5b6-abc12 (Running)
- redis-master-0 (Running)
- api-server-v2-5f9d8c7b-xyz34 (Running)
...
```

```
🔍 Your query: Get logs from api-server-v2-5f9d8c7b-xyz34
📊 Response: Logs from pod 'api-server-v2-5f9d8c7b-xyz34' (container: 'api', namespace: 'production'):

2024-01-15 10:23:45 INFO Starting API server...
2024-01-15 10:23:46 INFO Connected to database
...
```

### Advanced Queries

```
🔍 Your query: Are there any failing pods in kube-system?
🔍 Your query: Show me the last 50 lines of logs from the nginx pod
🔍 Your query: Which pods are running on node worker-01?
```

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get-pods` | List pods in a namespace | `namespace` (default: "default") |
| `get-namespaces` | List all namespaces | None |
| `check-logs` | Retrieve pod logs | `pod_name`, `namespace`, `container`, `tail_lines` |

## 📁 Project Structure

```
Agentic-Kubernetes-Management/
├── k8s_agent.py           # Main Strands agent with interactive CLI
├── k8s_mcp_server.py      # MCP server exposing Kubernetes tools
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .env.example           # Environment variables template
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BEDROCK_MODEL_REGION` | AWS region for Bedrock | `us-east-1` |
| `BEDROCK_MODEL_ID` | Claude model identifier | `apac.anthropic.claude-3-5-sonnet-20241022-v2:0` |

### Kubernetes Configuration

Ensure your `~/.kube/config` is properly configured:

```bash
kubectl config view
kubectl config current-context
```

## 🧩 How It Works

### 1. MCP Server (k8s_mcp_server.py)

The MCP server exposes Kubernetes operations as callable tools using the FastMCP framework:

- **`get-pods`** - Queries Kubernetes API for pod information
- **`get-namespaces`** - Lists all namespaces in the cluster
- **`check-logs`** - Retrieves container logs from pods

### 2. Strands Agent (agent.py)

The Strands agent:
- Connects to the MCP server via stdio transport
- Loads available tools dynamically
- Processes natural language queries using Claude
- Maintains conversation context across multiple queries
- Invokes appropriate tools based on user intent

### 3. Model Context Protocol (MCP)

MCP enables:
- **Tool Discovery** - Agent discovers available Kubernetes tools
- **Structured Communication** - Standardized request/response format
- **Extensibility** - Easy to add new tools without changing agent code

## 🚧 Roadmap

- [ ] context settings
- [ ] Add deployment management tools
- [ ] Support for ConfigMaps and Secrets
- [ ] Node resource monitoring
- [ ] Service and Ingress management
- [ ] Multi-cluster support
- [ ] Prometheus metrics integration
- [ ] Slack/Discord bot integration
- [ ] Web UI dashboard

## Acknowledgments

- [Strands AI Framework](https://github.com/strands-ai) - Agent orchestration
- [Model Context Protocol](https://modelcontextprotocol.io) - Tool integration standard
- [Anthropic Claude](https://www.anthropic.com/claude) - Language model
- [AWS Bedrock](https://aws.amazon.com/bedrock/) - Model hosting
- [Kubernetes Python Client](https://github.com/kubernetes-client/python) - K8s API access