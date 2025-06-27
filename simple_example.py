#!/usr/bin/env python3
"""Simple example demonstrating FutureHouse MCP server usage."""

import asyncio
import os
from futurehouse_mcp.server import FutureHouseMCP

async def main():
    """Run simple examples of FutureHouse MCP functionality."""
    
    # Initialize the MCP server (you can also pass api_key directly)
    server = FutureHouseMCP()
    
    print("=== FutureHouse MCP Server Example ===\n")
    
    # Example 1: Simple task submission
    print("1. Simple task submission:")
    result = await server.submit_task(
        job_name="crow",
        query="What is the molecule known to have the greatest solubility in water?"
    )
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    if result.success:
        print(f"Task ID: {result.task_id}")
        print(f"Status: {result.status}")
        print(f"Answer: {result.data['answer'][:200]}..." if len(result.data['answer']) > 200 else result.data['answer'])
    print("\n" + "="*50 + "\n")
    
    # Example 2: Task with custom configuration
    print("2. Task with custom configuration:")
    result = await server.submit_task_with_config(
        job_name="crow",
        query="How many moons does earth have?",
        model="gpt-4o",
        temperature=0.0,
        max_steps=10
    )
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    if result.success:
        print(f"Task ID: {result.task_id}")
        print(f"Status: {result.status}")
        print(f"Answer: {result.data['answer'][:200]}..." if len(result.data['answer']) > 200 else result.data['answer'])
        print(f"Used model: {result.data['config']['model']}")
    print("\n" + "="*50 + "\n")
    
    # Example 3: List available jobs
    print("3. Available jobs:")
    result = await server.list_available_jobs()
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    if result.success:
        print(f"Available jobs: {result.data['available_jobs']}")
    print("\n" + "="*50 + "\n")
    
    # Example 4: Create agent configuration
    print("4. Create custom agent configuration:")
    result = await server.create_agent_config(
        agent_type="SimpleAgent",
        model="gpt-4o",
        temperature=0.1,
        additional_kwargs={"max_tokens": 1000}
    )
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    if result.success:
        print(f"Agent config: {result.data['agent_config']}")
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    # Make sure you have set FUTUREHOUSE_API_KEY environment variable
    if not os.getenv("FUTUREHOUSE_API_KEY"):
        print("Please set FUTUREHOUSE_API_KEY environment variable")
        exit(1)
    
    asyncio.run(main()) 