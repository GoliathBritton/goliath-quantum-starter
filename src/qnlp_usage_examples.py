"""
Usage and Test Scaffolding for QNLP + Dynex
-------------------------------------------
- Shows how to use qdllm for various QNLP tasks and algorithms
- Includes async test functions for text classification, sentiment, NER, summarization
"""

import asyncio
from nqba_stack.qdllm import qdllm


async def test_text_classification():
    result = await qdllm.generate(
        prompt="Quantum computing is the future.",
        task="text_classification",
        labels=["tech", "finance", "health"],
        algorithm="qaoa",
    )
    print("Text Classification:", result)


async def test_sentiment():
    result = await qdllm.generate(
        prompt="I love quantum breakthroughs!", task="sentiment", algorithm="vqe"
    )
    print("Sentiment:", result)


async def test_ner():
    result = await qdllm.generate(
        prompt="Dynex and IBM are leaders in quantum.",
        task="ner",
        labels=["ORG", "PERSON", "LOC"],
        algorithm="custom",
    )
    print("NER:", result)


async def test_summarization():
    result = await qdllm.generate(
        prompt="Quantum computers solve problems. They use qubits. They are fast.",
        task="summarization",
        algorithm="qaoa",
    )
    print("Summarization:", result)


async def test_qdllm_diffusion():
    result = await qdllm.generate(
        prompt="Quantum AI is revolutionizing everything.", mode="qdllm"
    )
    print("qdLLM Quantum Diffusion:", result)


async def test_qtransformer():
    result = await qdllm.generate(
        prompt="Quantum transformers enable parallel reasoning.", mode="qtransformer"
    )
    print("QTransformer:", result)


if __name__ == "__main__":
    asyncio.run(test_text_classification())
    asyncio.run(test_sentiment())
    asyncio.run(test_ner())
    asyncio.run(test_summarization())
    asyncio.run(test_qdllm_diffusion())
    asyncio.run(test_qtransformer())
