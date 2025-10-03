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
DEFAULT_PORT = int(os.getenv("MCP_PORT", "3011"))
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
        
        # Register our tools and resources
        self._register_futurehouse_tools()
        self._register_futurehouse_resources()
    
    def _register_futurehouse_tools(self):
        """Register FutureHouse-specific tools."""
        # Register model-specific tools
        self.tool(
            name=f"{self.prefix}chem_agent", 
            description="Request PHOENIX model for chemistry tasks: synthesis planning, novel molecule design, and cheminformatics analysis"
        )(self.chem_agent)
        
        self.tool(
            name=f"{self.prefix}quick_search_agent", 
            description="Request CROW model for concise scientific search: produces succinct answers citing scientific data sources"
        )(self.quick_search_agent)
        
        self.tool(
            name=f"{self.prefix}precedent_search_agent", 
            description="Request OWL model for precedent search: determines if anyone has done something in science"
        )(self.precedent_search_agent)
        
        self.tool(
            name=f"{self.prefix}deep_search_agent", 
            description="Request FALCON model for deep search: produces long reports with many sources for literature reviews"
        )(self.deep_search_agent)
        
        # Register continuation tool
        self.tool(
            name=f"{self.prefix}continue_task", 
            description="Continue a previous task with a follow-up question"
        )(self.continue_task)
    
    def _register_futurehouse_resources(self):
        """Register FutureHouse-specific resources."""
        
        @self.resource(f"resource://{self.prefix}api-info")
        def get_api_info() -> str:
            """
            Get information about the FutureHouse client capabilities and usage.
            
            This resource contains information about:
            - Available models and their capabilities
            - Authentication requirements
            - Task submission patterns
            
            Returns:
                Client information and usage guidelines
            """
            return f"""
            # FutureHouse MCP Server
            
            ## Authentication
            - Uses FutureHouse client with API key authentication
            - API key: {self.api_key[:8]}...
            
            ## Available Models
            
            ### PHOENIX
            - **Task Type**: Chemistry Tasks (Experimental)
            - **Description**: Synthesis planning, novel molecule design, and cheminformatics analysis
            - **Example Queries**:
              - "Show three examples of amide coupling reactions"
              - "Tell me how to synthesize safinamide & where to buy each reactant"
              - "Propose 3 novel compounds that could treat a disease"
            
            ### CROW
            - **Task Type**: Concise Scientific Search
            - **Description**: Produces succinct answers citing scientific data sources
            - **Example Queries**:
              - "What are likely mechanisms for age-related macular degeneration?"
              - "How compelling is genetic evidence for targeting PTH1R in small cell lung cancer?"
            
            ### OWL
            - **Task Type**: Precedent Search
            - **Description**: Determines if anyone has done something in science
            - **Example Queries**:
              - "Has anyone developed efficient non-CRISPR methods for modifying DNA?"
              - "Has anyone used single-molecule footprinting to examine transcription factor binding?"
            
            ### FALCON
            - **Task Type**: Deep Search
            - **Description**: Produces long reports with many sources for literature reviews
            - **Example Queries**:
              - "What is the latest research on physiological benefits of coffee consumption?"
              - "What have been the most empirically effective treatments for Ulcerative Colitis?"
            
            ## Usage
            
            ```python
            # Request a model
            result = await futurehouse_chem_agent(query="Synthesize aspirin")
            result = await futurehouse_quick_search_agent(query="What causes Alzheimer's disease?")
            result = await futurehouse_precedent_search_agent(query="Has anyone used CRISPR for malaria treatment?")
            result = await futurehouse_deep_search_agent(query="Review treatments for diabetes")
            
            # Continue a previous task
            result = await futurehouse_continue_task(
                previous_task_id="task_123",
                query="Tell me more about the third option",
                job_name="phoenix"
            )
            ```
            """
    
    async def chem_agent(
        self,
        query: str
    ) -> FutureHouseResult:
        """
        Request PHOENIX model for chemistry tasks: synthesis planning, novel molecule design, and cheminformatics analysis.
        
        Example queries:
        - "Show three examples of amide coupling reactions"
        - "Tell me how to synthesize safinamide & where to buy each reactant"
        - "Propose 3 novel compounds that could treat a disease caused by over-expression of DENND1A"
        
        Args:
            query: The chemistry question or task to submit
            
        Returns:
            FutureHouseResult containing PHOENIX response
        """
        with start_action(action_type="chem_agent", query=query[:100] + "..." if len(query) > 100 else query):
            try:
                # Create task request for PHOENIX
                task_data = TaskRequest(
                    name=JobNames.PHOENIX,
                    query=query,
                )
                
                # Submit and run task until completion
                task_responses = self.client.run_tasks_until_done(task_data)
                
                if len(task_responses) == 0:
                    raise Exception("No tasks returned from PHOENIX")
                
                actual_response = task_responses[-1]
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
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
    
    async def quick_search_agent(
        self,
        query: str
    ) -> FutureHouseResult:
        """
        Request CROW model for concise scientific search: produces succinct answers citing scientific data sources.
        
        Example queries:
        - "What are likely mechanisms by which mutations near HTRA1 might cause age-related macular degeneration?"
        - "How compelling is genetic evidence for targeting PTH1R in small cell lung cancer?"
        - "What factors limit the wavelengths of light detectable by mammalian eyes?"
        
        Args:
            query: The scientific question to submit
            
        Returns:
            FutureHouseResult containing CROW response
        """
        with start_action(action_type="quick_search_agent", query=query[:100] + "..." if len(query) > 100 else query):
            try:
                # Create task request for CROW
                task_data = TaskRequest(
                    name=JobNames.CROW,
                    query=query,
                )
                
                # Submit and run task until completion
                task_responses = self.client.run_tasks_until_done(task_data)
                
                if len(task_responses) == 0:
                    raise Exception("No tasks returned from CROW")
                
                actual_response = task_responses[-1]
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
                        "job_name": "crow",
                        "query": query
                    },
                    success=True,
                    message=f"CROW task completed successfully with status: {actual_response.status}",
                    task_id=str(actual_response.task_id) if actual_response.task_id else None,
                    status=actual_response.status
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e), "job_name": "crow", "query": query},
                    success=False,
                    message=f"Failed to submit CROW request: {str(e)}"
                )
    
    async def precedent_search_agent(
        self,
        query: str
    ) -> FutureHouseResult:
        """
        Request OWL model for precedent search: determines if anyone has done something in science.
        
        Example queries:
        - "Has anyone developed efficient non-CRISPR methods for modifying DNA?"
        - "Has anyone used single-molecule footprinting to examine transcription factor binding in human cells?"
        - "Has anyone studied using a RAG system to help make better diagnoses for patients?"
        
        Args:
            query: The precedent question to submit
            
        Returns:
            FutureHouseResult containing OWL response
        """
        with start_action(action_type="precedent_search_agent", query=query[:100] + "..." if len(query) > 100 else query):
            try:
                # Create task request for OWL
                task_data = TaskRequest(
                    name=JobNames.OWL,
                    query=query,
                )
                
                # Submit and run task until completion
                task_responses = self.client.run_tasks_until_done(task_data)
                
                if len(task_responses) == 0:
                    raise Exception("No tasks returned from OWL")
                
                actual_response = task_responses[-1]
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
                        "job_name": "owl",
                        "query": query
                    },
                    success=True,
                    message=f"OWL task completed successfully with status: {actual_response.status}",
                    task_id=str(actual_response.task_id) if actual_response.task_id else None,
                    status=actual_response.status
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e), "job_name": "owl", "query": query},
                    success=False,
                    message=f"Failed to submit OWL request: {str(e)}"
                )
    
    async def deep_search_agent(
        self,
        query: str
    ) -> FutureHouseResult:
        """
        Request FALCON model for deep search: produces long reports with many sources for literature reviews.
        
        Example queries:
        - "What is the latest research on physiological benefits of high levels of coffee consumption?"
        - "What genes have been most strongly implicated in causing age-related macular degeneration?"
        - "What have been the most empirically effective treatments for Ulcerative Colitis?"
        
        Args:
            query: The literature review question to submit
            
        Returns:
            FutureHouseResult containing FALCON response
        """
        with start_action(action_type="deep_search_agent", query=query[:100] + "..." if len(query) > 100 else query):
            try:
                # Create task request for FALCON
                task_data = TaskRequest(
                    name=JobNames.FALCON,
                    query=query,
                )
                
                # Submit and run task until completion
                task_responses = self.client.run_tasks_until_done(task_data)
                
                if len(task_responses) == 0:
                    raise Exception("No tasks returned from FALCON")
                
                actual_response = task_responses[-1]
                answer = getattr(actual_response, 'answer', None) or getattr(actual_response, 'formatted_answer', None) or ""
                
                return FutureHouseResult(
                    data={
                        "task_id": str(actual_response.task_id) if actual_response.task_id else None,
                        "status": actual_response.status,
                        "answer": answer,
                        "job_name": "falcon",
                        "query": query
                    },
                    success=True,
                    message=f"FALCON task completed successfully with status: {actual_response.status}",
                    task_id=str(actual_response.task_id) if actual_response.task_id else None,
                    status=actual_response.status
                )
                
            except Exception as e:
                return FutureHouseResult(
                    data={"error": str(e), "job_name": "falcon", "query": query},
                    success=False,
                    message=f"Failed to submit FALCON request: {str(e)}"
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
    
# Create the MCP server instance lazily to avoid authentication during imports
def get_mcp_server():
    """Get or create the MCP server instance."""
    return FutureHouseMCP()

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

def cli_app_sse():
    """Entry point for SSE mode."""
    sse()

if __name__ == "__main__":
    app() 