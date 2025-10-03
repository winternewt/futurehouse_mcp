#!/usr/bin/env python3
"""Battle Integration Tests for FutureHouse MCP server.

These tests make real API calls to the FutureHouse platform to verify functionality.
Requires valid FUTUREHOUSE_API_KEY environment variable or .env file.
"""

import pytest
import asyncio
import os
from dotenv import load_dotenv
from futurehouse_mcp.server import FutureHouseMCP

# Load environment variables from .env file
load_dotenv()


class TestFutureHouseBattleIntegration:
    """Battle integration tests that make real API calls."""
    
    @pytest.fixture(scope="class")
    def api_key(self) -> str:
        """Get API key from environment."""
        api_key = os.getenv("FUTUREHOUSE_API_KEY")
        if not api_key:
            pytest.skip("FUTUREHOUSE_API_KEY not set - skipping integration tests")
        return api_key
    
    @pytest.fixture(scope="class")
    def server(self, api_key: str) -> FutureHouseMCP:
        """Create a real server instance for integration testing."""
        return FutureHouseMCP(api_key=api_key)
    
    @pytest.mark.asyncio
    async def test_chem_agent(self, server: FutureHouseMCP):
        """
        BATTLE TEST: Real PHOENIX chemistry request with actual API.
        
        This test makes a real API call to PHOENIX and verifies:
        1. The request succeeds
        2. We get back actual chemistry data
        3. Response format is correct
        """
        # First sample query from tool documentation
        battle_query = "Show three examples of amide coupling reactions"
        
        print(f"\n🧪 BATTLE TEST: Submitting real PHOENIX request...")
        print(f"🔍 Query: {battle_query}")
        
        try:
            # Make the real API call
            print(f"\n🚀 Making real API call...")
            result = await server.chem_agent(query=battle_query)
            
            # Debug dump the entire result
            print(f"\n📋 FULL RESULT DEBUG DUMP:")
            print(f"  Result type: {type(result)}")
            print(f"  Success: {result.success}")
            print(f"  Message: {result.message}")
            print(f"  Task ID: {result.task_id}")
            print(f"  Status: {result.status}")
            print(f"  Data keys: {list(result.data.keys()) if result.data else 'None'}")
            
            # Verify success
            assert result.success is True, f"API call failed: {result.message}"
            assert result.task_id is not None, "No task ID returned"
            assert result.status is not None, "No status returned"
            assert result.data is not None, "No data returned"
            
            # Verify we got actual answer content
            answer = result.data.get("answer", "")
            print(f"\n📄 ANSWER ANALYSIS:")
            print(f"  Answer length: {len(answer)} characters")
            print(f"  Answer preview (first 300 chars): {answer[:300]}...")
            
            assert len(answer) > 50, f"Answer too short, got: {len(answer)} characters"
            
            # Verify job name is correct
            assert result.data["job_name"] == "phoenix", f"Wrong job name: {result.data['job_name']}"
            
            print(f"\n🎯 BATTLE TEST COMPLETED!")
            print(f"✅ API call successful: {result.success}")
            print(f"✅ Task ID received: {result.task_id}")
            print(f"✅ Status: {result.status}")
            print(f"✅ Answer length: {len(answer)} chars")
            
            return result
            
        except Exception as e:
            print(f"\n💥 EXCEPTION DURING BATTLE TEST:")
            print(f"  Exception type: {type(e)}")
            print(f"  Exception message: {str(e)}")
            
            import traceback
            print(f"\n📍 FULL TRACEBACK:")
            traceback.print_exc()
            
            raise
    
    @pytest.mark.asyncio
    async def test_quick_search_agent(self, server: FutureHouseMCP):
        """
        BATTLE TEST: Real CROW quick search request with actual API.
        
        This test makes a real API call to CROW and verifies:
        1. The request succeeds
        2. We get back actual search data
        3. Response format is correct
        """
        # First sample query from tool documentation
        battle_query = "What are likely mechanisms by which mutations near HTRA1 might cause age-related macular degeneration?"
        
        print(f"\n🔍 BATTLE TEST: Submitting real CROW request...")
        print(f"🔍 Query: {battle_query}")
        
        try:
            # Make the real API call
            print(f"\n🚀 Making real API call...")
            result = await server.quick_search_agent(query=battle_query)
            
            # Debug dump the entire result
            print(f"\n📋 FULL RESULT DEBUG DUMP:")
            print(f"  Result type: {type(result)}")
            print(f"  Success: {result.success}")
            print(f"  Message: {result.message}")
            print(f"  Task ID: {result.task_id}")
            print(f"  Status: {result.status}")
            print(f"  Data keys: {list(result.data.keys()) if result.data else 'None'}")
            
            # Verify success
            assert result.success is True, f"API call failed: {result.message}"
            assert result.task_id is not None, "No task ID returned"
            assert result.status is not None, "No status returned"
            assert result.data is not None, "No data returned"
            
            # Verify we got actual answer content
            answer = result.data.get("answer", "")
            print(f"\n📄 ANSWER ANALYSIS:")
            print(f"  Answer length: {len(answer)} characters")
            print(f"  Answer preview (first 300 chars): {answer[:300]}...")
            
            assert len(answer) > 50, f"Answer too short, got: {len(answer)} characters"
            
            # Verify job name is correct
            assert result.data["job_name"] == "crow", f"Wrong job name: {result.data['job_name']}"
            
            print(f"\n🎯 BATTLE TEST COMPLETED!")
            print(f"✅ API call successful: {result.success}")
            print(f"✅ Task ID received: {result.task_id}")
            print(f"✅ Status: {result.status}")
            print(f"✅ Answer length: {len(answer)} chars")
            
            return result
            
        except Exception as e:
            print(f"\n💥 EXCEPTION DURING BATTLE TEST:")
            print(f"  Exception type: {type(e)}")
            print(f"  Exception message: {str(e)}")
            
            import traceback
            print(f"\n📍 FULL TRACEBACK:")
            traceback.print_exc()
            
            raise
    
    @pytest.mark.asyncio
    async def test_precedent_search_agent(self, server: FutureHouseMCP):
        """
        BATTLE TEST: Real OWL precedent search request with actual API.
        
        This test makes a real API call to OWL and verifies:
        1. The request succeeds
        2. We get back actual precedent data
        3. Response format is correct
        """
        # First sample query from tool documentation
        battle_query = "Has anyone developed efficient non-CRISPR methods for modifying DNA?"
        
        print(f"\n🦉 BATTLE TEST: Submitting real OWL request...")
        print(f"🔍 Query: {battle_query}")
        
        try:
            # Make the real API call
            print(f"\n🚀 Making real API call...")
            result = await server.precedent_search_agent(query=battle_query)
            
            # Debug dump the entire result
            print(f"\n📋 FULL RESULT DEBUG DUMP:")
            print(f"  Result type: {type(result)}")
            print(f"  Success: {result.success}")
            print(f"  Message: {result.message}")
            print(f"  Task ID: {result.task_id}")
            print(f"  Status: {result.status}")
            print(f"  Data keys: {list(result.data.keys()) if result.data else 'None'}")
            
            # Verify success
            assert result.success is True, f"API call failed: {result.message}"
            assert result.task_id is not None, "No task ID returned"
            assert result.status is not None, "No status returned"
            assert result.data is not None, "No data returned"
            
            # Verify we got actual answer content
            answer = result.data.get("answer", "")
            print(f"\n📄 ANSWER ANALYSIS:")
            print(f"  Answer length: {len(answer)} characters")
            print(f"  Answer preview (first 300 chars): {answer[:300]}...")
            
            assert len(answer) > 50, f"Answer too short, got: {len(answer)} characters"
            
            # Verify job name is correct
            assert result.data["job_name"] == "owl", f"Wrong job name: {result.data['job_name']}"
            
            print(f"\n🎯 BATTLE TEST COMPLETED!")
            print(f"✅ API call successful: {result.success}")
            print(f"✅ Task ID received: {result.task_id}")
            print(f"✅ Status: {result.status}")
            print(f"✅ Answer length: {len(answer)} chars")
            
            return result
            
        except Exception as e:
            print(f"\n💥 EXCEPTION DURING BATTLE TEST:")
            print(f"  Exception type: {type(e)}")
            print(f"  Exception message: {str(e)}")
            
            import traceback
            print(f"\n📍 FULL TRACEBACK:")
            traceback.print_exc()
            
            raise
    
    @pytest.mark.asyncio
    async def test_deep_search_agent(self, server: FutureHouseMCP):
        """
        BATTLE TEST: Real FALCON deep search request with actual API.
        
        This test makes a real API call to FALCON and verifies:
        1. The request succeeds
        2. We get back actual deep search data
        3. Response format is correct
        """
        # First sample query from tool documentation
        battle_query = "What is the latest research on physiological benefits of high levels of coffee consumption?"
        
        print(f"\n🦅 BATTLE TEST: Submitting real FALCON request...")
        print(f"🔍 Query: {battle_query}")
        
        try:
            # Make the real API call
            print(f"\n🚀 Making real API call...")
            result = await server.deep_search_agent(query=battle_query)
            
            # Debug dump the entire result
            print(f"\n📋 FULL RESULT DEBUG DUMP:")
            print(f"  Result type: {type(result)}")
            print(f"  Success: {result.success}")
            print(f"  Message: {result.message}")
            print(f"  Task ID: {result.task_id}")
            print(f"  Status: {result.status}")
            print(f"  Data keys: {list(result.data.keys()) if result.data else 'None'}")
            
            # Verify success
            assert result.success is True, f"API call failed: {result.message}"
            assert result.task_id is not None, "No task ID returned"
            assert result.status is not None, "No status returned"
            assert result.data is not None, "No data returned"
            
            # Verify we got actual answer content
            answer = result.data.get("answer", "")
            print(f"\n📄 ANSWER ANALYSIS:")
            print(f"  Answer length: {len(answer)} characters")
            print(f"  Answer preview (first 300 chars): {answer[:300]}...")
            
            assert len(answer) > 50, f"Answer too short, got: {len(answer)} characters"
            
            # Verify job name is correct
            assert result.data["job_name"] == "falcon", f"Wrong job name: {result.data['job_name']}"
            
            print(f"\n🎯 BATTLE TEST COMPLETED!")
            print(f"✅ API call successful: {result.success}")
            print(f"✅ Task ID received: {result.task_id}")
            print(f"✅ Status: {result.status}")
            print(f"✅ Answer length: {len(answer)} chars")
            
            return result
            
        except Exception as e:
            print(f"\n💥 EXCEPTION DURING BATTLE TEST:")
            print(f"  Exception type: {type(e)}")
            print(f"  Exception message: {str(e)}")
            
            import traceback
            print(f"\n📍 FULL TRACEBACK:")
            traceback.print_exc()
            
            raise
    
    @pytest.mark.asyncio
    async def test_continue_task(self, server: FutureHouseMCP):
        """
        BATTLE TEST: Test follow-up query using quick search result.
        
        This test:
        1. Submits initial quick search query
        2. Gets the task ID
        3. Submits a follow-up question using continue_task
        4. Verifies the continuation works correctly
        """
        # Initial query
        initial_query = "What are likely mechanisms by which mutations near HTRA1 might cause age-related macular degeneration?"
        
        print(f"\n🔄 BATTLE TEST: Testing task continuation...")
        print(f"🔍 Initial Query: {initial_query}")
        
        try:
            # Step 1: Make initial quick search call
            print(f"\n🚀 Making initial API call...")
            initial_result = await server.quick_search_agent(query=initial_query)
            
            # Verify initial call succeeded
            assert initial_result.success is True, f"Initial API call failed: {initial_result.message}"
            assert initial_result.task_id is not None, "No task ID returned from initial call"
            
            task_id = initial_result.task_id
            print(f"\n✅ Initial call succeeded, got task ID: {task_id}")
            print(f"   Initial answer preview: {initial_result.data['answer'][:200]}...")
            
            # Step 2: Make continuation call
            followup_query = "What are the most promising therapeutic approaches based on these mechanisms?"
            
            print(f"\n🔄 Making continuation call...")
            print(f"🔍 Follow-up Query: {followup_query}")
            
            continuation_result = await server.continue_task(
                previous_task_id=task_id,
                query=followup_query,
                job_name="crow"
            )
            
            # Debug dump the continuation result
            print(f"\n📋 CONTINUATION RESULT DEBUG DUMP:")
            print(f"  Result type: {type(continuation_result)}")
            print(f"  Success: {continuation_result.success}")
            print(f"  Message: {continuation_result.message}")
            print(f"  Task ID: {continuation_result.task_id}")
            print(f"  Status: {continuation_result.status}")
            print(f"  Data keys: {list(continuation_result.data.keys()) if continuation_result.data else 'None'}")
            
            # Verify continuation succeeded
            assert continuation_result.success is True, f"Continuation API call failed: {continuation_result.message}"
            assert continuation_result.task_id is not None, "No task ID returned from continuation"
            assert continuation_result.status is not None, "No status returned from continuation"
            assert continuation_result.data is not None, "No data returned from continuation"
            
            # Verify we got actual answer content
            answer = continuation_result.data.get("answer", "")
            print(f"\n📄 CONTINUATION ANSWER ANALYSIS:")
            print(f"  Answer length: {len(answer)} characters")
            print(f"  Answer preview (first 300 chars): {answer[:300]}...")
            
            assert len(answer) > 50, f"Continuation answer too short, got: {len(answer)} characters"
            
            # Verify job name and previous task ID are preserved
            assert continuation_result.data["job_name"] == "crow", f"Wrong job name: {continuation_result.data['job_name']}"
            assert continuation_result.data["previous_task_id"] == task_id, f"Previous task ID not preserved: {continuation_result.data['previous_task_id']}"
            
            # Verify the continuation task ID is different from the original
            assert continuation_result.task_id != task_id, "Continuation should have a new task ID"
            
            print(f"\n🎯 BATTLE TEST COMPLETED!")
            print(f"✅ Initial call successful: {initial_result.success}")
            print(f"✅ Initial task ID: {task_id}")
            print(f"✅ Continuation successful: {continuation_result.success}")
            print(f"✅ Continuation task ID: {continuation_result.task_id}")
            print(f"✅ Answer length: {len(answer)} chars")
            print(f"✅ Previous task ID preserved: {continuation_result.data['previous_task_id']}")
            
            return continuation_result
            
        except Exception as e:
            print(f"\n💥 EXCEPTION DURING BATTLE TEST:")
            print(f"  Exception type: {type(e)}")
            print(f"  Exception message: {str(e)}")
            
            import traceback
            print(f"\n📍 FULL TRACEBACK:")
            traceback.print_exc()
            
            raise


if __name__ == "__main__":
    # Run integration tests with specific markers
    pytest.main([
        __file__,
        "-v",
        "--tb=short"
    ])
