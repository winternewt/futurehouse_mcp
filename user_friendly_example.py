#!/usr/bin/env python3
"""User-friendly example demonstrating FutureHouse MCP server with comprehensive error handling."""

import asyncio
import os
import sys
from src.futurehouse_mcp.server import FutureHouseMCP

def print_separator(title: str = ""):
    """Print a nice separator with optional title."""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("="*60)

def print_result(result, show_full_answer: bool = False):
    """Print result in a user-friendly format."""
    print(f"✅ Success: {result.success}")
    print(f"📝 Message: {result.message}")
    
    if result.success:
        if result.task_id:
            print(f"🆔 Task ID: {result.task_id}")
        if result.status:
            print(f"📊 Status: {result.status}")
        
        # Handle different types of data
        if 'answer' in result.data:
            answer = result.data['answer']
            if show_full_answer or len(answer) <= 200:
                print(f"💬 Answer: {answer}")
            else:
                print(f"💬 Answer (truncated): {answer[:200]}...")
                print("   (Use show_full_answer=True to see complete answer)")
        
        if 'available_jobs' in result.data:
            print(f"🛠️  Available jobs: {', '.join(result.data['available_jobs'])}")
            print(f"📊 Total count: {result.data['count']}")
        
        if 'config' in result.data:
            config = result.data['config']
            print(f"⚙️  Configuration used:")
            print(f"   - Model: {config.get('model', 'N/A')}")
            print(f"   - Temperature: {config.get('temperature', 'N/A')}")
            print(f"   - Max steps: {config.get('max_steps', 'N/A')}")
        
        if 'agent_config' in result.data:
            agent_config = result.data['agent_config']
            print(f"🤖 Agent Configuration:")
            print(f"   - Type: {agent_config.get('agent_type', 'N/A')}")
            print(f"   - Parameters: {agent_config.get('agent_kwargs', {})}")
    else:
        print(f"❌ Error details: {result.data.get('error', 'Unknown error')}")

async def run_examples():
    """Run comprehensive examples of FutureHouse MCP functionality."""
    
    # Check for API key
    if not os.getenv("FUTUREHOUSE_API_KEY"):
        print("❌ FUTUREHOUSE_API_KEY environment variable is not set!")
        print("Please set your API key: export FUTUREHOUSE_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize the MCP server
        print("🚀 Initializing FutureHouse MCP Server...")
        server = FutureHouseMCP()
        print("✅ Server initialized successfully!")
        
        print_separator("Example 1: List Available Jobs")
        print("📋 Getting list of available jobs...")
        result = await server.list_available_jobs()
        print_result(result)
        
        print_separator("Example 2: Simple Task Submission")
        print("🔬 Submitting a scientific query...")
        result = await server.submit_task(
            job_name="crow",
            query="What is the molecule known to have the greatest solubility in water?"
        )
        print_result(result)
        
        # Store task ID for continuation example
        first_task_id = result.task_id if result.success else None
        
        print_separator("Example 3: Task with Custom Configuration")
        print("⚙️  Submitting task with custom agent configuration...")
        result = await server.submit_task_with_config(
            job_name="crow",
            query="How many moons does earth have?",
            model="gpt-4o",
            temperature=0.0,
            max_steps=10
        )
        print_result(result)
        
        print_separator("Example 4: Create Custom Agent Configuration")
        print("🤖 Creating a custom agent configuration...")
        result = await server.create_agent_config(
            agent_type="SimpleAgent",
            model="gpt-4o",
            temperature=0.1,
            additional_kwargs={"max_tokens": 1000, "top_p": 0.9}
        )
        print_result(result)
        
        # Task continuation example (only if we have a task ID)
        if first_task_id:
            print_separator("Example 5: Task Continuation")
            print("🔄 Continuing previous task with follow-up question...")
            result = await server.continue_task(
                previous_task_id=first_task_id,
                query="From the previous answer, what are some practical applications of this molecule's high solubility?",
                job_name="crow"
            )
            print_result(result, show_full_answer=True)
        else:
            print_separator("Example 5: Task Continuation (Skipped)")
            print("⚠️  Skipping task continuation - no valid task ID from previous example")
        
        print_separator("All Examples Completed Successfully! 🎉")
        return True
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

async def interactive_mode():
    """Run an interactive session for testing queries."""
    print_separator("Interactive Mode")
    print("🎮 Welcome to Interactive FutureHouse MCP!")
    print("You can submit custom queries. Type 'quit' to exit.")
    
    try:
        server = FutureHouseMCP()
        
        while True:
            print("\n" + "-"*40)
            query = input("🤔 Enter your query (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if not query:
                print("Please enter a valid query.")
                continue
            
            job_name = input("🛠️  Enter job name (default: crow): ").strip() or "crow"
            
            print(f"\n🚀 Submitting query to job '{job_name}'...")
            result = await server.submit_task(job_name=job_name, query=query)
            print_result(result, show_full_answer=True)
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")

def main():
    """Main entry point with user options."""
    print("🏠 FutureHouse MCP Server - User-Friendly Example")
    print("="*50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_mode())
    else:
        print("Running standard examples...")
        print("(Use --interactive flag for interactive mode)")
        success = asyncio.run(run_examples())
        
        if success:
            print("\n🎯 Want to try interactive mode? Run:")
            print("   python user_friendly_example.py --interactive")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main() 