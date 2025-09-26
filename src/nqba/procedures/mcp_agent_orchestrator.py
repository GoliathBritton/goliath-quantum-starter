import os
import asyncio
from typing import Optional, Union
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Import Semantic Kernel orchestrator if available
try:
    from nqba.core.mcp_semantic_kernel import MCPSemanticKernelOrchestrator
    SEMANTIC_KERNEL_AVAILABLE = True
except ImportError:
    SEMANTIC_KERNEL_AVAILABLE = False


class MCPAgentOrchestrator:
    def __init__(self, api_key: str = os.getenv("OPENAI_API_KEY"), use_semantic_kernel: bool = False):
        self.use_semantic_kernel = use_semantic_kernel and SEMANTIC_KERNEL_AVAILABLE
        
        if self.use_semantic_kernel:
            try:
                self.sk_orchestrator = MCPSemanticKernelOrchestrator()
            except Exception as e:
                print(f"Failed to initialize Semantic Kernel orchestrator: {e}")
                self.use_semantic_kernel = False
        
        if not self.use_semantic_kernel:
            if not api_key or api_key == "your_api_key_here":
                raise ValueError("Invalid OpenAI API key. Please set OPENAI_API_KEY environment variable to a valid key.")
            config_list = [{"model": "gpt-4", "api_key": api_key}]
            
            self.user_proxy = UserProxyAgent(
                name="user_proxy",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=10,
                code_execution_config={"work_dir": "mcp_orchestration", "use_docker": False},
            )
            
            self.mcp_agent = AssistantAgent(
                name="MCP_Agent",
                system_message="You are an expert in Model Content Protocols (MCP). Orchestrate MCP tasks using quantum-enhanced methods.",
                llm_config={"config_list": config_list},
            )
            
            self.quantum_agent = AssistantAgent(
                name="Quantum_Agent",
                system_message="You handle quantum computations and integrations with Dynex or other quantum backends.",
                llm_config={"config_list": config_list},
            )
            
            groupchat = GroupChat(agents=[self.user_proxy, self.mcp_agent, self.quantum_agent], messages=[], max_round=12)
            self.manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

    def orchestrate_mcp_task(self, task_description: str) -> str:
        """
        Orchestrate an MCP task using either AutoGen or Semantic Kernel.
        
        Args:
            task_description: The task to be orchestrated
            
        Returns:
            The orchestration result as a string
        """
        if self.use_semantic_kernel:
            # Run the Semantic Kernel orchestrator asynchronously
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # Create a new event loop if one doesn't exist
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(self.sk_orchestrator.orchestrate_task(task_description))
            return result
        else:
            # Use the original AutoGen orchestration
            self.user_proxy.initiate_chat(
                self.manager,
                message=task_description
            )
            # Extract and return the final result from chat history
            chat_history = self.user_proxy.chat_messages.get(self.manager, [])
            if chat_history:
                results = []
                for msg in chat_history:
                    if msg.get('name') != 'user_proxy' and msg['content']:
                        results.append(f"{msg['name']}: {msg['content']}")
                return "\n\n".join(results)
            return "No result found"

# Example usage
if __name__ == "__main__":
    # Try with Semantic Kernel if available
    try:
        orchestrator = MCPAgentOrchestrator(use_semantic_kernel=True)
        result = orchestrator.orchestrate_mcp_task("Optimize MCP for financial modeling using quantum algorithms.")
        print("Using Semantic Kernel:")
        print(result)
    except Exception as e:
        print(f"Semantic Kernel orchestration failed: {e}")
    
    # Fallback to AutoGen
    orchestrator = MCPAgentOrchestrator(use_semantic_kernel=False)
    result = orchestrator.orchestrate_mcp_task("Optimize MCP for financial modeling using quantum algorithms.")
    print("\nUsing AutoGen:")
    print(result)