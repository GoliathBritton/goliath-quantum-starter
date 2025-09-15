#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Agent Demo
"""

import asyncio
from agents.chatbot import create_chatbot

async def main():
    """Run agent demonstration"""
    print("FLYFOX AI Agent Demo")
    print("=" * 30)
    
    # Create chatbot
    chatbot = create_chatbot()
    
    # Test interaction
    messages = [
        "Hello!",
        "Tell me about quantum computing",
        "How can I use quantum optimization?",
        "Goodbye!"
    ]
    
    for message in messages:
        print(f"\nYou: {message}")
        response = await chatbot.process_message(message)
        print(f"Bot: {response.content}")
        
        if response.suggestions:
            print("Suggestions:")
            for suggestion in response.suggestions:
                print(f"   • {suggestion}")

if __name__ == "__main__":
    asyncio.run(main())
