# FutureHouse MCP Server Usage Guide

This guide provides comprehensive information on how to use the FutureHouse MCP Server.

## Quick Start

### 1. Installation

```bash
# Install the package
uv add futurehouse-mcp

# Or with pip
pip install futurehouse-mcp
```

### 2. Set up Authentication

```bash
export FUTUREHOUSE_API_KEY="your_api_key_here"
```

### 3. Configure Your MCP Client

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "futurehouse-mcp": {
      "command": "uvx",
      "args": ["futurehouse-mcp", "stdio"],
      "env": {
        "FUTUREHOUSE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### 1. `futurehouse_submit_task`

Submit a simple task to a FutureHouse job.

**Syntax:**
```
Use futurehouse_submit_task with job_name: "crow" and query: "Your question here"
```

**Example:**
```
Use futurehouse_submit_task with:
- job_name: "crow"
- query: "What is photosynthesis and how does it work?"
```

### 2. `futurehouse_submit_task_with_config`

Submit a task with custom runtime configuration.

**Syntax:**
```
Use futurehouse_submit_task_with_config with:
- job_name: "job_name"
- query: "Your question"
- model: "model_name" (optional)
- temperature: 0.0-1.0 (optional)
- max_steps: number (optional)
- agent_type: "SimpleAgent" (optional)
- agent_kwargs: {...} (optional)
```

**Example:**
```
Use futurehouse_submit_task_with_config with:
- job_name: "crow"
- query: "Explain quantum mechanics in simple terms"
- model: "gpt-4o"
- temperature: 0.1
- max_steps: 15
- agent_kwargs: {"max_tokens": 1000}
```

### 3. `futurehouse_continue_task`

Continue a previous task with a follow-up question.

**Syntax:**
```
Use futurehouse_continue_task with:
- previous_task_id: "task_id_from_previous_response"
- query: "Follow-up question"
- job_name: "same_job_name_as_original"
```

**Example:**
```
Use futurehouse_continue_task with:
- previous_task_id: "task_abc123"
- query: "Can you provide more specific examples?"
- job_name: "crow"
```

### 4. `futurehouse_list_available_jobs`

List all available job names.

**Syntax:**
```
Use futurehouse_list_available_jobs
```

### 5. `futurehouse_create_agent_config`

Create a custom agent configuration.

**Syntax:**
```
Use futurehouse_create_agent_config with:
- agent_type: "SimpleAgent" (optional)
- model: "model_name" (optional)
- temperature: 0.0-1.0 (optional)
- additional_kwargs: {...} (optional)
```

## Common Use Cases

### Scientific Research Queries

```
Use futurehouse_submit_task with:
- job_name: "crow"
- query: "What are the latest breakthroughs in CRISPR gene editing technology?"
```

### Complex Multi-step Analysis

```
Use futurehouse_submit_task_with_config with:
- job_name: "crow"
- query: "Analyze the environmental impact of renewable energy adoption"
- model: "gpt-4o"
- temperature: 0.0
- max_steps: 20
```

### Follow-up Conversations

```
# First query
Use futurehouse_submit_task with:
- job_name: "crow"
- query: "What are the main types of renewable energy?"

# Follow-up (using task_id from first response)
Use futurehouse_continue_task with:
- previous_task_id: "task_xyz789"
- query: "Which of these is most cost-effective for residential use?"
- job_name: "crow"
```

## Advanced Configuration

### Custom Agent Parameters

You can customize the AI agent behavior:

```
Use futurehouse_submit_task_with_config with:
- job_name: "crow"
- query: "Your question"
- agent_type: "SimpleAgent"
- model: "gpt-4o"
- temperature: 0.2  # Higher for more creativity, lower for consistency
- max_steps: 25     # More steps for complex tasks
- agent_kwargs: {
    "max_tokens": 1500,
    "top_p": 0.9,
    "frequency_penalty": 0.1
  }
```

### Available Models

Common models you can use:
- `gpt-4o` - Latest GPT-4 model (recommended)
- `gpt-4` - Standard GPT-4
- `gpt-3.5-turbo` - Faster, less capable
- `claude-3-opus` - Anthropic's most capable model
- `claude-3-sonnet` - Balanced performance

### Temperature Settings

- `0.0` - Deterministic, consistent responses
- `0.1-0.3` - Slightly varied but focused
- `0.4-0.7` - Balanced creativity and consistency
- `0.8-1.0` - Highly creative but less predictable

## Error Handling

### Common Issues

**API Key Missing:**
```
Error: "FutureHouse API key is required"
Solution: Set FUTUREHOUSE_API_KEY environment variable
```

**Invalid Job Name:**
```
Error: Job name not found
Solution: Use futurehouse_list_available_jobs to see available options
```

**Task Timeout:**
```
Error: Task execution timed out
Solution: Reduce max_steps or simplify the query
```

### Debugging

Enable debug mode in your MCP configuration:

```json
{
  "mcpServers": {
    "futurehouse-mcp": {
      "command": "uvx",
      "args": ["futurehouse-mcp", "stdio"],
      "env": {
        "FUTUREHOUSE_API_KEY": "your_api_key_here",
        "DEBUG": "1",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## Best Practices

### Query Formulation

1. **Be Specific:** Clear, detailed questions get better results
   ```
   Good: "What are the molecular mechanisms of photosynthesis in C4 plants?"
   Avoid: "Tell me about plants"
   ```

2. **Provide Context:** Include relevant background information
   ```
   "I'm studying biochemistry. Can you explain how enzymes work at the molecular level?"
   ```

3. **Break Down Complex Questions:** Use follow-up queries for multi-part questions

### Performance Optimization

1. **Choose Appropriate Models:**
   - Use `gpt-3.5-turbo` for simple questions
   - Use `gpt-4o` for complex analysis
   - Use `claude-3-opus` for detailed reasoning

2. **Set Reasonable Limits:**
   - `max_steps: 10-15` for most queries
   - `max_steps: 20-30` for complex research tasks

3. **Use Continuation Wisely:**
   - Continue tasks to build on previous context
   - Don't continue if starting a new topic

### Resource Management

1. **Monitor Task Duration:** Long-running tasks consume more resources
2. **Use Appropriate Temperature:** Lower values for factual queries
3. **Batch Related Questions:** Use continuation instead of separate tasks

## Examples Repository

Check out these complete examples:

- `simple_example.py` - Basic usage patterns
- `user_friendly_example.py` - Interactive examples with error handling
- `client_notebook.ipynb` - Jupyter notebook examples

## Troubleshooting

### Connection Issues

If you experience connection problems:

1. Verify your API key is correct
2. Check network connectivity
3. Try different transport modes (stdio, http, sse)

### Performance Issues

For slow responses:

1. Reduce `max_steps`
2. Use simpler models for basic questions
3. Avoid very long queries

### Integration Issues

When integrating with MCP clients:

1. Ensure correct JSON configuration
2. Check environment variable setup
3. Verify command paths are correct

## Support

For additional help:

1. Check the main README.md for setup instructions
2. Review example scripts for usage patterns
3. Open an issue on the project repository
4. Check FutureHouse documentation for platform-specific information 