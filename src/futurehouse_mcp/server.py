#!/usr/bin/env python3
"""FutureHouse MCP Server - Interface for interacting with FutureHouse platform."""

import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import json

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from eliot import start_action
import typer

# Import FutureHouse client components
from futurehouse_client import FutureHouseClient, JobNames
from futurehouse_client.models import (
    RuntimeConfig,
    TaskRequest,
)
from ldp.agent import AgentConfig

# Configuration
DEFAULT_HOST = os.getenv("MCP_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("MCP_PORT", "3001"))
DEFAULT_TRANSPORT = os.getenv("MCP_TRANSPORT", "streamable-http")

class FutureHouseResult(BaseModel):
    """Result from a FutureHouse API call."""
    data: Any = Field(description="Response data from FutureHouse")
    success: bool = Field(description="Whether the operation was successful")
    message: str = Field(description="Operation description")
    task_id: Optional[str] = Field(default=None, description="Task ID for tracking")
    status: Optional[str] = Field(default=None, description="Task status")

class FutureHouseMCP(FastMCP):
    """FutureHouse MCP Server with client-based tools that can be inherited and extended."""
    
    def __init__(
        self, 
        name: str = "FutureHouse MCP Server",
        api_key: Optional[str] = None,
        prefix: str = "futurehouse_",
        phoenix_only: bool = False,
        **kwargs
    ):
        """Initialize the FutureHouse tools with client and FastMCP functionality."""
        # Initialize FastMCP with the provided name and any additional kwargs
        super().__init__(name=name, **kwargs)
        
        # Get API credentials from environment if not provided
        self.api_key = api_key or os.getenv("FUTUREHOUSE_API_KEY")
        
        if not self.api_key:
            raise ValueError("FutureHouse API key is required. Set FUTUREHOUSE_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize our FutureHouse client
        self.client = FutureHouseClient(api_key=self.api_key)
        
        self.prefix = prefix
        self.phoenix_only = phoenix_only
        
        # Register our tools and resources
        self._register_futurehouse_tools()
        self._register_futurehouse_resources()
    
    def _register_futurehouse_tools(self):
        """Register FutureHouse-specific tools."""
        if self.phoenix_only:
            # Only register the PHOENIX tool
            self.tool(
                name=f"{self.prefix}request_phoenix_smiles", 
                description="Request PHOENIX to generate novel compounds with SMILES notation for drug discovery"
            )(self.request_phoenix_smiles)
        else:
            # Register all tools
            self.tool(
                name=f"{self.prefix}submit_task", 
                description="Submit a task to a FutureHouse job and run it until completion"
            )(self.submit_task)
            
            self.tool(
                name=f"{self.prefix}submit_task_with_config", 
                description="Submit a task to a FutureHouse job with custom runtime configuration"
            )(self.submit_task_with_config)
            
            self.tool(
                name=f"{self.prefix}continue_task", 
                description="Continue a previous task with a follow-up question"
            )(self.continue_task)
            
            self.tool(
                name=f"{self.prefix}list_available_jobs", 
                description="List all available job names in the FutureHouse platform"
            )(self.list_available_jobs)
            
            self.tool(
                name=f"{self.prefix}create_agent_config", 
                description="Create a custom agent configuration for task submission"
            )(self.create_agent_config)
            
            self.tool(
                name=f"{self.prefix}request_phoenix_smiles", 
                description="Request PHOENIX to generate novel compounds with SMILES notation for drug discovery"
            )(self.request_phoenix_smiles)
    
    def _register_futurehouse_resources(self):
        """Register FutureHouse-specific resources."""
        
        @self.resource(f"resource://{self.prefix}api-info")
        def get_api_info() -> str:
            """
            Get information about the FutureHouse client capabilities and usage.
            
            This resource contains information about:
            - Available jobs and their capabilities
            - Authentication requirements
            - Task submission patterns
            - Runtime configuration options
            
            Returns:
                Client information and usage guidelines
            """
            return f"""
            # FutureHouse Client Information
            
            ## Authentication
            - Uses FutureHouse client with API key authentication
            - API key: {self.api_key[:8]}...
            
            ## Available Services
            - Task Submission: Submit queries to available FutureHouse jobs
            - Job Management: Track and continue tasks
            - Agent Configuration: Customize agent behavior
            - Runtime Configuration: Control execution parameters
            
            ## Available Jobs
            The platform supports various job types including:
            - CROW: Research and analysis tasks
            - And other specialized jobs available on the platform
            
            ## Task Flow
            1. Submit a task with a query and job name
            2. Optionally configure runtime parameters (agent, max_steps, etc.)
            3. Monitor task execution until completion
            4. Continue with follow-up questions if needed
            
            ## Agent Configuration
            You can customize the agent used for task execution:
            - Model selection (e.g., gpt-4o, claude-3, etc.)
            - Temperature settings
            - Other agent-specific parameters
            
            ## Example Usage
            ```python
            # Simple task submission
            result = await submit_task(
                job_name="crow",
                query="What is the molecule known to have the greatest solubility in water?"
            )
            
            # Task with custom configuration
            result = await submit_task_with_config(
                job_name="crow",
                query="How many moons does earth have?",
                agent_type="SimpleAgent",
                model="gpt-4o",
                temperature=0.0,
                max_steps=10
            )
            
            # Continue a previous task
            result = await continue_task(
                previous_task_id="task_123",
                query="From the previous answer, specifically how many species of crows are there?",
                job_name="crow"
            )
            ```
            """
    
    async def submit_task(
        self,
        job_name: str,
        query: str
    ) -> FutureHouseResult:
        """
        Submit a task to a FutureHouse job and run it until completion.
        
        Args:
            job_name: Name of the job to submit to (e.g., "crow")
            query: The question or task to submit
            
        Returns:
            FutureHouseResult containing the task response
        """
        with start_action(action_type="submit_task", job_name=job_name, query=query[:100] + "..." if len(query) > 100 else query):
            try:
                # Create task request
                task_data = TaskRequest(
                    name=JobNames.from_string(job_name),
                    query=query,
                )
                
                # Submit and run task until completion
                task_responses = self.client.run_tasks_until_done(task_data)
                
                # run_tasks_until_done always returns a list
                if len(task_responses) == 0:
                    raise Exception("No tasks returned")
                
                # Take the last task response (most recent)
                actual_response = task_responses[-1]
                
                # Get the answer - different response types have different fields
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
                        "job_name": job_name,
                        "query": query
                    },
                    success=True,
                    message=f"Task completed successfully with status: {actual_response.status}",
                    task_id=str(actual_response.task_id) if actual_response.task_id else None,
                    status=actual_response.status
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e), "job_name": job_name, "query": query},
                    success=False,
                    message=f"Failed to submit task: {str(e)}"
                )
    
    async def submit_task_with_config(
        self,
        job_name: str,
        query: str,
        agent_type: str = "SimpleAgent",
        model: str = "gpt-4o",
        temperature: float = 0.0,
        max_steps: int = 10,
        agent_kwargs: Optional[Dict[str, Any]] = None
    ) -> FutureHouseResult:
        """
        Submit a task to a FutureHouse job with custom runtime configuration.
        
        Args:
            job_name: Name of the job to submit to (e.g., "crow")
            query: The question or task to submit
            agent_type: Type of agent to use (default: "SimpleAgent")
            model: Model to use for the agent (default: "gpt-4o")
            temperature: Temperature setting for the model (default: 0.0)
            max_steps: Maximum number of steps for task execution (default: 10)
            agent_kwargs: Additional agent configuration parameters
            
        Returns:
            FutureHouseResult containing the task response
        """
        with start_action(action_type="submit_task_with_config", job_name=job_name, model=model):
            try:
                # Prepare agent kwargs
                final_agent_kwargs = {"model": model, "temperature": temperature}
                if agent_kwargs:
                    final_agent_kwargs.update(agent_kwargs)
                
                # Create agent configuration
                agent = AgentConfig(
                    agent_type=agent_type,
                    agent_kwargs=final_agent_kwargs,
                )
                
                # Create task request with runtime config
                task_data = TaskRequest(
                    name=JobNames.from_string(job_name),
                    query=query,
                    runtime_config=RuntimeConfig(agent=agent, max_steps=max_steps),
                )
                
                # Submit and run task until completion
                task_responses = self.client.run_tasks_until_done(task_data)
                
                # run_tasks_until_done always returns a list
                if len(task_responses) == 0:
                    raise Exception("No tasks returned")
                
                # Take the last task response (most recent)
                actual_response = task_responses[-1]
                
                # Get the answer - different response types have different fields
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
                        "job_name": job_name,
                        "query": query,
                        "config": {
                            "agent_type": agent_type,
                            "model": model,
                            "temperature": temperature,
                            "max_steps": max_steps,
                            "agent_kwargs": final_agent_kwargs
                        }
                    },
                    success=True,
                    message=f"Task completed successfully with custom config. Status: {actual_response.status}",
                    task_id=str(actual_response.task_id) if actual_response.task_id else None,
                    status=actual_response.status
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e), "job_name": job_name, "query": query},
                    success=False,
                    message=f"Failed to submit task with config: {str(e)}"
                )
    
    async def continue_task(
        self,
        previous_task_id: str,
        query: str,
        job_name: str
    ) -> FutureHouseResult:
        """
        Continue a previous task with a follow-up question.
        
        Args:
            previous_task_id: ID of the previous task to continue
            query: Follow-up question or task
            job_name: Name of the job (should match the original task)
            
        Returns:
            FutureHouseResult containing the continued task response
        """
        with start_action(action_type="continue_task", task_id=previous_task_id, job_name=job_name):
            try:
                # Create continued task data
                continued_job_data = {
                    "name": JobNames.from_string(job_name),
                    "query": query,
                    "runtime_config": {"continued_job_id": previous_task_id},
                }
                
                # Submit and run continued task until completion
                task_responses = self.client.run_tasks_until_done(continued_job_data)
                
                # run_tasks_until_done always returns a list
                if len(task_responses) == 0:
                    raise Exception("No tasks returned")
                
                # Take the last task response (most recent)
                actual_response = task_responses[-1]
                
                # Get the answer - different response types have different fields
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
                        "job_name": job_name,
                        "query": query,
                        "previous_task_id": previous_task_id
                    },
                    success=True,
                    message=f"Continued task completed successfully. Status: {actual_response.status}",
                    task_id=str(actual_response.task_id) if actual_response.task_id else None,
                    status=actual_response.status
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e), "previous_task_id": previous_task_id, "query": query},
                    success=False,
                    message=f"Failed to continue task: {str(e)}"
                )
    
    async def list_available_jobs(self) -> FutureHouseResult:
        """
        List all available job names in the FutureHouse platform.
        
        Returns:
            FutureHouseResult containing available job names
        """
        with start_action(action_type="list_available_jobs"):
            try:
                # Get available job names from JobNames enum
                available_jobs = []
                
                # Try to get all available job names
                # We'll check for common attributes/methods in JobNames
                if hasattr(JobNames, '__members__'):
                    available_jobs = list(JobNames.__members__.keys())
                elif hasattr(JobNames, 'CROW'):
                    # At minimum we know CROW exists from the notebook
                    available_jobs = ['CROW']
                else:
                    # Fallback - try to introspect the class
                    available_jobs = [attr for attr in dir(JobNames) if not attr.startswith('_')]
                
                return FutureHouseResult(
                    data={
                        "available_jobs": available_jobs,
                        "count": len(available_jobs)
                    },
                    success=True,
                    message=f"Found {len(available_jobs)} available jobs"
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e)},
                    success=False,
                    message=f"Failed to list available jobs: {str(e)}"
                )
    
    async def create_agent_config(
        self,
        agent_type: str = "SimpleAgent",
        model: str = "gpt-4o",
        temperature: float = 0.0,
        additional_kwargs: Optional[Dict[str, Any]] = None
    ) -> FutureHouseResult:
        """
        Create a custom agent configuration that can be used in task submission.
        
        Args:
            agent_type: Type of agent to create (default: "SimpleAgent")
            model: Model to use for the agent (default: "gpt-4o")
            temperature: Temperature setting for the model (default: 0.0)
            additional_kwargs: Additional agent configuration parameters
            
        Returns:
            FutureHouseResult containing the agent configuration
        """
        with start_action(action_type="create_agent_config", agent_type=agent_type, model=model):
            try:
                # Prepare agent kwargs
                agent_kwargs = {"model": model, "temperature": temperature}
                if additional_kwargs:
                    agent_kwargs.update(additional_kwargs)
                
                # Create agent configuration
                agent_config = AgentConfig(
                    agent_type=agent_type,
                    agent_kwargs=agent_kwargs,
                )
                
                return FutureHouseResult(
                    data={
                        "agent_config": {
                            "agent_type": agent_type,
                            "agent_kwargs": agent_kwargs
                        },
                        "usage_example": {
                            "description": "Use this config in submit_task_with_config or in RuntimeConfig",
                            "example": f"RuntimeConfig(agent=agent_config, max_steps=10)"
                        }
                    },
                    success=True,
                    message=f"Agent configuration created successfully for {agent_type} with model {model}"
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e)},
                    success=False,
                    message=f"Failed to create agent config: {str(e)}"
                )

    async def request_phoenix_smiles(
        self,
        query: str
    ) -> FutureHouseResult:
        """
        Request PHOENIX to generate novel compounds with SMILES notation for drug discovery.
        
        Example: "Propose 3 novel compounds that could treat a disease caused by over-expression of DENND1A"
        
        Args:
            query: The drug discovery query or disease target description
            
        Returns:
            FutureHouseResult containing PHOENIX response with compound suggestions
        """
        with start_action(action_type="request_phoenix_smiles", query=query[:100] + "..." if len(query) > 100 else query):
            try:
                # Create task request for PHOENIX
                task_data = TaskRequest(
                    name=JobNames.PHOENIX,
                    query=query,
                )
                
                # Submit and run task until completion
                task_responses = self.client.run_tasks_until_done(task_data)
                
                # run_tasks_until_done always returns a list
                if len(task_responses) == 0:
                    raise Exception("No tasks returned from PHOENIX")
                
                # Take the last task response (most recent)
                actual_response = task_responses[-1]
                
                # Get the answer - PhoenixTaskResponse has 'answer' field
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
                        "compounds": answer,  # PHOENIX typically returns compound data
                        "job_name": "phoenix",
                        "query": query
                    },
                    success=True,
                    message=f"PHOENIX task completed successfully with status: {actual_response.status}",
                    task_id=str(actual_response.task_id) if actual_response.task_id else None,
                    status=actual_response.status
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e), "job_name": "phoenix", "query": query},
                    success=False,
                    message=f"Failed to submit PHOENIX request: {str(e)}"
                )

# Create the MCP server instances lazily to avoid authentication during imports
def get_mcp_server():
    """Get or create the main MCP server instance."""
    return FutureHouseMCP()

def get_phoenix_server():
    """Get or create the PHOENIX-only MCP server instance."""
    return FutureHouseMCP(
        name="FutureHouse PHOENIX MCP Server",
        phoenix_only=True
    )

# CLI application using typer
app = typer.Typer()

@app.command()
def main(
    host: str = typer.Option(DEFAULT_HOST, help="Host to bind to"),
    port: int = typer.Option(DEFAULT_PORT, help="Port to bind to"),
    transport: str = typer.Option(DEFAULT_TRANSPORT, help="Transport type")
):
    """Run the FutureHouse MCP server."""
    get_mcp_server().run(transport=transport, host=host, port=port)

@app.command()
def stdio():
    """Run the FutureHouse MCP server with stdio transport."""
    get_mcp_server().run(transport="stdio")

@app.command()
def stdio_phoenix():
    """Run the FutureHouse MCP server with stdio transport optimized for PHOENIX drug discovery."""
    get_phoenix_server().run(transport="stdio")

@app.command()
def sse(
    host: str = typer.Option(DEFAULT_HOST, help="Host to bind to"),
    port: int = typer.Option(DEFAULT_PORT, help="Port to bind to")
):
    """Run the FutureHouse MCP server with SSE transport."""
    get_mcp_server().run(transport="sse", host=host, port=port)

def cli_app():
    """Entry point for the CLI application."""
    app()

def cli_app_stdio():
    """Entry point for stdio mode."""
    stdio()

def cli_app_stdio_phoenix():
    """Entry point for stdio-phoenix mode."""
    stdio_phoenix()

def cli_app_sse():
    """Entry point for SSE mode."""
    sse()

if __name__ == "__main__":
    app() 