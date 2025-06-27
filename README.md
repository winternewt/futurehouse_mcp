# FutureHouse MCP Server

A Model Context Protocol (MCP) server for interacting with the FutureHouse platform. This server provides tools to submit tasks, manage jobs, and interact with FutureHouse's AI agents and environments.

## Features

- **Task Submission**: Submit queries to available FutureHouse jobs
- **Custom Agent Configuration**: Configure agents with specific models and parameters
- **Task Continuation**: Continue previous tasks with follow-up questions
- **Job Management**: List available jobs and track task status
- **Multiple Transport Modes**: Support for stdio, HTTP, and SSE transports

## Installation

```bash
# Install using uv (recommended)
uv add futurehouse-mcp

# Or install using pip
pip install futurehouse-mcp
```

## Configuration

### Environment Variables

Set your FutureHouse API key:

```bash
export FUTUREHOUSE_API_KEY="your_api_key_here"
```

### MCP Client Configuration

Add to your MCP client configuration file:

#### stdio transport (recommended)
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

#### HTTP transport
```json
{
  "mcpServers": {
    "futurehouse-mcp": {
      "command": "uvx",
      "args": ["futurehouse-mcp", "server"],
      "env": {
        "FUTUREHOUSE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### `futurehouse_submit_task`
Submit a simple task to a FutureHouse job.

**Parameters:**
- `job_name` (string): Name of the job (e.g., "crow")
- `query` (string): The question or task to submit

**Example:**
```
Submit task to job "crow" with query "What is the molecule known to have the greatest solubility in water?"
```

### `futurehouse_submit_task_with_config`
Submit a task with custom runtime configuration.

**Parameters:**
- `job_name` (string): Name of the job
- `query` (string): The question or task to submit
- `agent_type` (string, optional): Type of agent (default: "SimpleAgent")
- `model` (string, optional): Model to use (default: "gpt-4o")
- `temperature` (float, optional): Temperature setting (default: 0.0)
- `max_steps` (int, optional): Maximum steps (default: 10)
- `agent_kwargs` (dict, optional): Additional agent parameters

**Example:**
```
Submit task with custom config:
- job_name: "crow"
- query: "How many moons does earth have?"
- model: "gpt-4o"
- temperature: 0.0
- max_steps: 10
```

### `futurehouse_continue_task`
Continue a previous task with a follow-up question.

**Parameters:**
- `previous_task_id` (string): ID of the previous task
- `query` (string): Follow-up question
- `job_name` (string): Name of the job

**Example:**
```
Continue task "task_123" with query "From the previous answer, specifically how many species of crows are there?"
```

### `futurehouse_list_available_jobs`
List all available job names in the FutureHouse platform.

**Example:**
```
List all available jobs
```

### `futurehouse_create_agent_config`
Create a custom agent configuration.

**Parameters:**
- `agent_type` (string, optional): Type of agent (default: "SimpleAgent")
- `model` (string, optional): Model to use (default: "gpt-4o")
- `temperature` (float, optional): Temperature setting (default: 0.0)
- `additional_kwargs` (dict, optional): Additional parameters

## Usage Examples

### Simple Task Submission
```
Use futurehouse_submit_task with:
- job_name: "crow"
- query: "What are the latest developments in quantum computing?"
```

### Custom Agent Configuration
```
Use futurehouse_submit_task_with_config with:
- job_name: "crow"
- query: "Explain photosynthesis in simple terms"
- model: "gpt-4o"
- temperature: 0.1
- max_steps: 15
```

### Task Continuation
```
# First, submit a task
Use futurehouse_submit_task with:
- job_name: "crow"
- query: "How many species of birds are there?"

# Then continue with a follow-up
Use futurehouse_continue_task with:
- previous_task_id: "task_from_previous_response"
- query: "From the previous answer, specifically how many species of crows are there?"
- job_name: "crow"
```

## Development

### Running Locally

```bash
# Clone the repository
git clone <repository-url>
cd futurehouse-mcp

# Install dependencies
uv sync

# Run with stdio transport
uv run python -m futurehouse_mcp.server stdio

# Run with HTTP transport
uv run python -m futurehouse_mcp.server main --host 0.0.0.0 --port 3001
```

### Testing

```bash
# Install development dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=futurehouse_mcp
```

## API Reference

The server provides access to FutureHouse platform capabilities including:

- **Job Management**: Submit and track tasks across different job types
- **Agent Configuration**: Customize AI agent behavior and parameters
- **Task Continuation**: Build conversations by continuing previous tasks
- **Runtime Configuration**: Control execution parameters like max steps

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the documentation above
- Review the example scripts in the repository
- Open an issue on the GitHub repository

## Authentication

This server requires a valid FutureHouse API key. To obtain an API key:
1. Log in to the FutureHouse platform
2. Go to your user settings
3. Generate an API key
4. Set it as the `FUTUREHOUSE_API_KEY` environment variable
