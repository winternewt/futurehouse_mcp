#!/usr/bin/env python3
"""Tests for FutureHouse MCP server."""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch, AsyncMock
from futurehouse_mcp.server import FutureHouseMCP, FutureHouseResult

# Mock the FutureHouse client imports to avoid dependency issues during testing
@pytest.fixture
def mock_futurehouse_client():
    """Mock FutureHouse client for testing."""
    with patch('futurehouse_mcp.server.FutureHouseClient') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock task response
        mock_response = Mock()
        mock_response.task_id = "test_task_123"
        mock_response.status = "completed"
        mock_response.formatted_answer = "Test answer from FutureHouse"
        
        mock_instance.run_tasks_until_done.return_value = mock_response
        
        yield mock_instance

@pytest.fixture
def server(mock_futurehouse_client):
    """Create a test server instance."""
    with patch.dict(os.environ, {'FUTUREHOUSE_API_KEY': 'test_api_key'}):
        return FutureHouseMCP()

class TestFutureHouseMCP:
    """Test cases for FutureHouse MCP server."""
    
    @pytest.mark.asyncio
    async def test_submit_task_success(self, server, mock_futurehouse_client):
        """Test successful task submission."""
        result = await server.submit_task(
            job_name="crow",
            query="Test query"
        )
        
        assert result.success is True
        assert result.task_id == "test_task_123"
        assert result.status == "completed"
        assert "Test answer from FutureHouse" in result.data["answer"]
        
        # Verify client was called correctly
        mock_futurehouse_client.run_tasks_until_done.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_submit_task_with_config_success(self, server, mock_futurehouse_client):
        """Test successful task submission with custom configuration."""
        result = await server.submit_task_with_config(
            job_name="crow",
            query="Test query",
            model="gpt-4o",
            temperature=0.1,
            max_steps=15
        )
        
        assert result.success is True
        assert result.task_id == "test_task_123"
        assert result.status == "completed"
        assert result.data["config"]["model"] == "gpt-4o"
        assert result.data["config"]["temperature"] == 0.1
        assert result.data["config"]["max_steps"] == 15
        
    @pytest.mark.asyncio
    async def test_continue_task_success(self, server, mock_futurehouse_client):
        """Test successful task continuation."""
        result = await server.continue_task(
            previous_task_id="previous_task_123",
            query="Follow-up query",
            job_name="crow"
        )
        
        assert result.success is True
        assert result.task_id == "test_task_123"
        assert result.data["previous_task_id"] == "previous_task_123"
        
    @pytest.mark.asyncio
    async def test_list_available_jobs_success(self, server):
        """Test listing available jobs."""
        with patch('futurehouse_mcp.server.JobNames') as mock_job_names:
            mock_job_names.__members__ = {'CROW': 'crow', 'OTHER': 'other'}
            
            result = await server.list_available_jobs()
            
            assert result.success is True
            assert 'CROW' in result.data["available_jobs"]
            assert result.data["count"] >= 1
            
    @pytest.mark.asyncio
    async def test_create_agent_config_success(self, server):
        """Test creating agent configuration."""
        result = await server.create_agent_config(
            agent_type="SimpleAgent",
            model="gpt-4o",
            temperature=0.2,
            additional_kwargs={"max_tokens": 1000}
        )
        
        assert result.success is True
        assert result.data["agent_config"]["agent_type"] == "SimpleAgent"
        assert result.data["agent_config"]["agent_kwargs"]["model"] == "gpt-4o"
        assert result.data["agent_config"]["agent_kwargs"]["temperature"] == 0.2
        assert result.data["agent_config"]["agent_kwargs"]["max_tokens"] == 1000
        
    @pytest.mark.asyncio
    async def test_submit_task_error_handling(self, server, mock_futurehouse_client):
        """Test error handling in task submission."""
        # Make the client raise an exception
        mock_futurehouse_client.run_tasks_until_done.side_effect = Exception("API Error")
        
        result = await server.submit_task(
            job_name="crow",
            query="Test query"
        )
        
        assert result.success is False
        assert "Failed to submit task" in result.message
        assert "API Error" in result.data["error"]
        
    def test_initialization_without_api_key(self):
        """Test that initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="FutureHouse API key is required"):
                FutureHouseMCP()
                
    def test_initialization_with_api_key(self, mock_futurehouse_client):
        """Test successful initialization with API key."""
        with patch.dict(os.environ, {'FUTUREHOUSE_API_KEY': 'test_key'}):
            server = FutureHouseMCP()
            assert server.api_key == 'test_key'
            assert server.prefix == 'futurehouse_'

    @pytest.mark.asyncio
    async def test_request_phoenix_smiles_success(self, server, mock_futurehouse_client):
        """Test successful PHOENIX SMILES request."""
        # Mock a PHOENIX-specific response
        mock_response = Mock()
        mock_response.task_id = "phoenix_task_456"
        mock_response.status = "completed"
        mock_response.formatted_answer = "SMILES: CC(C)C1=CC=C(C=C1)C2=CC=C(C=C2)C(=O)O\nCompound Name: Novel DENND1A inhibitor candidate\nMolecular Weight: 268.31 g/mol"
        mock_futurehouse_client.run_tasks_until_done.return_value = mock_response
        
        result = await server.request_phoenix_smiles(
            query="Propose 3 novel compounds that could treat a disease caused by over-expression of DENND1A"
        )
        
        assert result.success is True
        assert result.task_id == "phoenix_task_456"
        assert result.status == "completed"
        assert "SMILES:" in result.data["answer"]
        assert result.data["job_name"] == "phoenix"
        
        # Verify client was called correctly with PHOENIX job
        mock_futurehouse_client.run_tasks_until_done.assert_called_once()
        call_args = mock_futurehouse_client.run_tasks_until_done.call_args[0][0]
        assert hasattr(call_args, 'query')
        assert "DENND1A" in call_args.query

class TestFutureHousePhoenixMCP:
    """Test cases specifically for FutureHouse PHOENIX-only MCP server."""
    
    @pytest.fixture
    def phoenix_server(self, mock_futurehouse_client):
        """Create a test PHOENIX-only server instance."""
        with patch.dict(os.environ, {'FUTUREHOUSE_API_KEY': 'test_api_key'}):
            return FutureHouseMCP(phoenix_only=True)
    
    def test_phoenix_only_initialization(self, mock_futurehouse_client):
        """Test that phoenix_only mode only registers phoenix tool."""
        with patch.dict(os.environ, {'FUTUREHOUSE_API_KEY': 'test_key'}):
            server = FutureHouseMCP(phoenix_only=True)
            assert server.phoenix_only is True
            assert server.api_key == 'test_key'
    
    @pytest.mark.asyncio
    async def test_phoenix_battle_test(self, phoenix_server, mock_futurehouse_client):
        """Battle test: Real-world example of PHOENIX drug discovery request."""
        # Mock PHOENIX response with realistic drug discovery output
        mock_response = Mock()
        mock_response.task_id = "phoenix_battle_789"
        mock_response.status = "completed"
        mock_response.formatted_answer = """
        Based on your request for novel compounds targeting DENND1A over-expression, here are 3 promising candidates:

        **Compound 1:**
        SMILES: CC1=CC=C(C=C1)C2=NC3=CC=CC=C3C(=N2)C4=CC=C(C=C4)Cl
        Name: DENND1A-Inhibitor-001
        Molecular Weight: 349.81 g/mol
        Predicted IC50: 2.3 μM
        Drug-likeness Score: 0.85

        **Compound 2:**
        SMILES: COC1=CC=C(C=C1)C2=CC=C(C=C2)C(=O)NC3=CC=C(C=C3)F
        Name: DENND1A-Inhibitor-002
        Molecular Weight: 339.35 g/mol
        Predicted IC50: 1.8 μM
        Drug-likeness Score: 0.78

        **Compound 3:**
        SMILES: CC(C)(C)OC(=O)N1CCN(CC1)C2=NC=NC3=C2C=CC=C3
        Name: DENND1A-Inhibitor-003
        Molecular Weight: 328.41 g/mol
        Predicted IC50: 3.1 μM
        Drug-likeness Score: 0.82

        All compounds show favorable ADMET properties and low toxicity predictions.
        """
        mock_futurehouse_client.run_tasks_until_done.return_value = mock_response
        
        # Battle test query - realistic drug discovery scenario
        battle_query = """
        Propose 3 novel compounds that could treat a disease caused by over-expression of DENND1A.
        The compounds should:
        1. Have good drug-like properties (Lipinski's Rule of Five)
        2. Show potential for crossing the blood-brain barrier
        3. Have low predicted toxicity
        4. Include SMILES notation and predicted binding affinity
        """
        
        result = await phoenix_server.request_phoenix_smiles(query=battle_query)
        
        # Verify the battle test results
        assert result.success is True
        assert result.task_id == "phoenix_battle_789"
        assert result.status == "completed"
        assert "SMILES:" in result.data["answer"]
        assert "DENND1A-Inhibitor" in result.data["answer"]
        assert "Molecular Weight:" in result.data["answer"]
        assert "IC50:" in result.data["answer"]
        assert result.data["job_name"] == "phoenix"
        assert "DENND1A" in result.data["query"]
        
        # Verify that compounds data is available
        assert "compounds" in result.data
        assert result.data["compounds"] == result.data["answer"]
        
        # Verify client was called with correct job name
        mock_futurehouse_client.run_tasks_until_done.assert_called_once()
        call_args = mock_futurehouse_client.run_tasks_until_done.call_args[0][0]
        assert hasattr(call_args, 'query')
        assert "blood-brain barrier" in call_args.query
        assert "Lipinski" in call_args.query
        
    @pytest.mark.asyncio
    async def test_phoenix_error_handling(self, phoenix_server, mock_futurehouse_client):
        """Test error handling in PHOENIX requests."""
        # Make the client raise an exception
        mock_futurehouse_client.run_tasks_until_done.side_effect = Exception("PHOENIX API Error")
        
        result = await phoenix_server.request_phoenix_smiles(
            query="Invalid query that causes error"
        )
        
        assert result.success is False
        assert "Failed to submit PHOENIX request" in result.message
        assert "PHOENIX API Error" in result.data["error"]
        assert result.data["job_name"] == "phoenix"

if __name__ == "__main__":
    pytest.main([__file__]) 