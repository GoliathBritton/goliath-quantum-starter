#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Agent Demo
"""

import asyncio
from agents.chatbot import create_chatbot
from nqba_stack.ltc_logger import LTCLogger

async def main():
    """Run agent demonstration"""
    print("FLYFOX AI Agent Demo")
    print("=" * 30)
    
    # Create chatbot
    logger = LTCLogger()\n    chatbot = create_chatbot()\n    \n    # Test interaction\n    messages = [\n        "Hello!",\n        "Tell me about quantum computing",\n        "How can I use quantum optimization?",\n        "Goodbye!"\n    ]\n    \n    for message in messages:\n        print(f"\nYou: {message}")\n        response = await chatbot.process_message(message)\n        print(f"Bot: {response.content}")\n        logger.log_operation(\n            operation_type="chatbot_response",\n            inputs={"message": message},\n            outputs={"response": response.content},\n            explanation="Processed user message in agent demo"\n        )\n        \n        if response.suggestions:\n            print("Suggestions:")\n            for suggestion in response.suggestions:\n                print(f"   � {suggestion}")\n

if __name__ == "__main__":
    asyncio.run(main())
