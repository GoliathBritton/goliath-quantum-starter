import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.agents.group_chat_manager import RoundRobinGroupChatManager
from semantic_kernel.agents.group_chat_orchestrator import GroupChatOrchestration
from semantic_kernel.contents.chat_history import ChatHistory

class MCPSemanticKernelOrchestrator:
    def __init__(self):
        self.kernel = sk.Kernel()
        
        # Add Azure OpenAI service - assuming env vars are set
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME') or 'gpt-35-turbo'
        
        if not all([api_key, endpoint, deployment]):
            raise ValueError("Missing Azure OpenAI configuration")
        
        self.kernel.add_service(
            AzureChatCompletion(
                deployment_name=deployment,
                endpoint=endpoint,
                api_key=api_key
            )
        )
        
        # Create agents
        self.mcp_agent = ChatCompletionAgent(
            service_id="azure_chat",
            kernel=self.kernel,
            name="MCP_Agent",
            instructions="You are an MCP orchestration agent specializing in multi-agent coordination for quantum tasks."
        )
        
        self.quantum_agent = ChatCompletionAgent(
            service_id="azure_chat",
            kernel=self.kernel,
            name="Quantum_Agent",
            instructions="You are a quantum computing expert agent."
        )
        
        self.agents = [self.mcp_agent, self.quantum_agent]

    async def orchestrate_task(self, task: str) -> str:
        # Set up group chat
        manager = RoundRobinGroupChatManager(self.agents)
        orchestrator = GroupChatOrchestration(manager=manager)
        
        # Start chat with user input
        chat_history = ChatHistory()
        chat_history.add_user_message(task)
        
        # Run orchestration
        result = await orchestrator.invoke_async(chat_history)
        
        # Extract final response (simplified - get last message)
        if result and result.content:
            return result.content
        return "No result from orchestration"

# Usage example (for testing)
# async def main():
#     orchestrator = MCPSemanticKernelOrchestrator()
#     result = await orchestrator.orchestrate_task("Discuss quantum computing in financial modeling")
#     print(result)
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())