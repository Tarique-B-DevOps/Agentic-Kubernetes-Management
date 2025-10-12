from mcp.server import FastMCP
from kubernetes import client, config
from typing import Optional

mcp = FastMCP("kubernetes-server")

try:
    config.load_kube_config()
except:
    config.load_incluster_config()

v1 = client.CoreV1Api()


@mcp.tool("get-pods")
def get_pods(namespace: str = "default") -> dict:
    """
    Get list of pods in a specified namespace.
    
    Args:
        namespace: Kubernetes namespace (default: "default")
    
    Returns:
        Dictionary containing pod information
    """
    try:
        pods = v1.list_namespaced_pod(namespace=namespace)
        
        pod_list = []
        for pod in pods.items:
            pod_info = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "ip": pod.status.pod_ip,
                "containers": [c.name for c in pod.spec.containers]
            }
            pod_list.append(pod_info)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Found {len(pod_list)} pods in namespace '{namespace}':\n" + 
                           "\n".join([f"- {p['name']} ({p['status']})" for p in pod_list])
                }
            ],
            "pods": pod_list
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error getting pods: {str(e)}"
                }
            ]
        }


@mcp.tool("get-namespaces")
def get_namespaces() -> dict:
    """
    Get list of all namespaces in the cluster.
    
    Returns:
        Dictionary containing namespace information
    """
    try:
        namespaces = v1.list_namespace()
        
        ns_list = []
        for ns in namespaces.items:
            ns_info = {
                "name": ns.metadata.name,
                "status": ns.status.phase,
                "created": str(ns.metadata.creation_timestamp)
            }
            ns_list.append(ns_info)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Found {len(ns_list)} namespaces:\n" + 
                           "\n".join([f"- {ns['name']} ({ns['status']})" for ns in ns_list])
                }
            ],
            "namespaces": ns_list
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error getting namespaces: {str(e)}"
                }
            ]
        }


@mcp.tool("check-logs")
def check_logs(
    pod_name: str, 
    namespace: str = "default", 
    container: Optional[str] = None,
    tail_lines: int = 100
) -> dict:
    """
    Get logs from a specific pod.
    
    Args:
        pod_name: Name of the pod
        namespace: Kubernetes namespace (default: "default")
        container: Specific container name (optional, uses first container if not specified)
        tail_lines: Number of lines to retrieve from end of logs (default: 100)
    
    Returns:
        Dictionary containing pod logs
    """
    try:
        if not container:
            pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            container = pod.spec.containers[0].name
        
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container,
            tail_lines=tail_lines
        )
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Logs from pod '{pod_name}' (container: '{container}', namespace: '{namespace}'):\n\n{logs}"
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error getting logs: {str(e)}"
                }
            ]
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")