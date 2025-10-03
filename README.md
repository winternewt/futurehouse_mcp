# FutureHouse MCP Server

A Model Context Protocol (MCP) server for interacting with the [FutureHouse platform](https://platform.futurehouse.org/). This server provides simple, LLM-tailored tools to access FutureHouse's AI agents for scientific research, chemistry tasks, and literature search.

## Features

- **Chemistry Agent (PHOENIX)**: Synthesis planning, molecule design, and cheminformatics
- **Quick Search Agent (CROW)**: Concise scientific answers with citations
- **Precedent Search Agent (OWL)**: Determine if anyone has done something in science
- **Deep Search Agent (FALCON)**: Long reports with many sources for literature reviews
- **Task Continuation**: Continue previous tasks with follow-up questions
- **Multiple Transports**: Support for stdio, HTTP, and SSE transports

## Tools TL;DR

| Tool Name | FutureHouse Model | Task Type | Description |
|-----------|-------------------|-----------|-------------|
| `futurehouse_chem_agent` | PHOENIX | Chemistry Tasks | Synthesis planning, molecule design, and cheminformatics analysis |
| `futurehouse_quick_search_agent` | CROW | Concise Search | Produces succinct answers citing scientific data sources |
| `futurehouse_precedent_search_agent` | OWL | Precedent Search | Determines if anyone has done something in science |
| `futurehouse_deep_search_agent` | FALCON | Deep Search | Produces long reports with many sources for literature reviews |
| `futurehouse_continue_task` | All | Task Continuation | Continue a previous task with a follow-up question |

## Installation

```bash
# Install using uv (recommended)
uv add futurehouse-mcp

# Or install using pip
pip install futurehouse-mcp
```

## Configuration

### Get Your API Key

Visit [https://platform.futurehouse.org/](https://platform.futurehouse.org/) to:

1. Create an account or log in
2. Navigate to your user profile
3. Generate an API key

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
      "args": ["futurehouse-mcp@latest", "stdio"],
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
      "args": ["futurehouse-mcp@latest", "server"],
      "env": {
        "FUTUREHOUSE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### `futurehouse_chem_agent`

Request PHOENIX model for chemistry tasks: synthesis planning, novel molecule design, and cheminformatics analysis.

**Parameters:**

- `query` (string): The chemistry question or task to submit

**Example:**

```text
Use futurehouse_chem_agent with query "Show three examples of amide coupling reactions"
```

### `futurehouse_quick_search_agent`

Request CROW model for concise scientific search: produces succinct answers citing scientific data sources.

**Parameters:**

- `query` (string): The scientific question to submit

**Example:**

```text
Use futurehouse_quick_search_agent with query "What causes age-related macular degeneration?"
```

### `futurehouse_precedent_search_agent`

Request OWL model for precedent search: determines if anyone has done something in science.

**Parameters:**

- `query` (string): The precedent question to submit

**Example:**

```text
Use futurehouse_precedent_search_agent with query "Has anyone used CRISPR for malaria treatment?"
```

### `futurehouse_deep_search_agent`

Request FALCON model for deep search: produces long reports with many sources for literature reviews.

**Parameters:**

- `query` (string): The literature review question to submit

**Example:**

```text
Use futurehouse_deep_search_agent with query "What are the most effective treatments for Ulcerative Colitis?"
```

### `futurehouse_continue_task`

Continue a previous task with a follow-up question.

**Parameters:**

- `previous_task_id` (string): ID of the previous task to continue
- `query` (string): Follow-up question or task
- `job_name` (string): Name of the job (phoenix, crow, owl, or falcon)

**Example:**

```text
Use futurehouse_continue_task with:
- previous_task_id: "task_123"
- query: "Tell me more about the third option"
- job_name: "phoenix"
```

## Usage Examples

### Chemistry Task

```text
Use futurehouse_chem_agent with query:
"Propose 3 novel compounds that could inhibit DENND1A and include their SMILES notation"
```

### Scientific Literature Search

```text
Use futurehouse_quick_search_agent with query:
"How compelling is genetic evidence for targeting PTH1R in small cell lung cancer?"
```

### Precedent Research

```text
Use futurehouse_precedent_search_agent with query:
"Has anyone developed efficient non-CRISPR methods for modifying DNA?"
```

### Literature Review

```text
Use futurehouse_deep_search_agent with query:
"What is the latest research on the physiological benefits of coffee consumption?"
```

### Task Continuation

```text
# First, submit a task
Use futurehouse_quick_search_agent with query:
"What are the main causes of Alzheimer's disease?"

# Then continue with a follow-up using the task_id from the response
Use futurehouse_continue_task with:
- previous_task_id: "task_from_previous_response"
- query: "What are the most promising treatments for these causes?"
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
uv run python3 -m futurehouse_mcp.server stdio

# Run with HTTP transport
uv run python3 -m futurehouse_mcp.server main --host 0.0.0.0 --port 3011
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

For more information about the FutureHouse platform and available models:

- **Platform Home**: [https://platform.futurehouse.org/](https://platform.futurehouse.org/)
- **Models Overview**: [https://platform.futurehouse.org/models](https://platform.futurehouse.org/models)
- **API Documentation**: [FutureHouse Cookbook](https://futurehouse.gitbook.io/futurehouse-cookbook/futurehouse-client#quickstart)

## FutureHouse Platform Models

### CROW (`JobNames.CROW`)

**Job Name:** `job-futurehouse-paperqa2`  
**Task Type:** Concise Search  
**Description:** Produces a succinct answer citing scientific data sources, good for API calls and specific questions. Built with PaperQA2.

**Sample Queries:**

- What are some likely mechanisms by which mutations near the HTRA1 locus in humans might be causal for age-related macular degeneration?
- How might you capture electron transfer effects using classical force fields for molecular dynamics simulations of protein-protein interactions?
- How compelling is genetic evidence for targeting PTH1R in small cell lung cancer?
- What factors limit the wavelengths of light detectable by mammalian eyes?

**LLMs (priority order):**

- `openai/gpt-4.1-2025-04-14`
- `anthropic/claude-3-7-sonnet-20250219`
- `anthropic/claude-3-5-sonnet-20241022`
- `openai/gpt-4o-2024-11-20`

**Tools the agent uses:**

- `complete` - Terminate using the last proposed answer. Do not invoke this tool in parallel with other tools or itself.
- `open_targets_search` - Search for disease-target associations from OpenTargets database. Adds new disease-target association data to the state and returns top search results.
- `collect_cited_papers_in_evidence` - Collect papers by traversing the citations of relevant papers to increase the paper count. This tool has no effect if called when paper count or relevant papers are zero. This tool will find papers that are likely to lead to more relevant evidence.
- `gather_evidence` - Gather evidence from previous papers, clinical trials, and disease-target data given a specific question. Each "evidence" is a synthesized summary from the raw sources, which can then be used in gen_answer.
- `clinical_trials_search` - Search for clinical trials, with support for repeated calls and concurrent execution. Will add new clinical trials to the state, and return metadata about the number of trials found.
- `paper_search` - Search for papers to increase the paper count. Can be called repeatedly with identical parameters to retrieve more results (max 2 repeats). This tool can be used concurrently with other tools for complementary research strategies.
- `gen_answer` - Generate an answer using current evidence. The tool may fail, indicating that better or different evidence should be found. Aim for at least five pieces of evidence from multiple sources before invoking this tool.

### FALCON (`JobNames.FALCON`)

**Job Name:** `job-futurehouse-paperqa2-deep`  
**Task Type:** Deep Search  
**Description:** Produces a long report with many sources, good for literature reviews and evaluating hypotheses.

**Sample Queries:**

- What is the latest research on the physiological benefits and detriments of high levels of coffee consumption?
- What genes have been most strongly implicated in causing age-related macular degeneration, and what mutations contribute to those associations?
- What have been the most empirically effective treatments for Ulcerative Colitis?
- How can RNA transcriptional history be studied in humans?

**LLMs (priority order):**

- `openai/gpt-4.1-2025-04-14`
- `anthropic/claude-3-7-sonnet-20250219`
- `anthropic/claude-3-5-sonnet-20241022`
- `openai/gpt-4o-2024-11-20`

**Tools the agent uses:**

- `complete` - Terminate using the last proposed answer. Do not invoke this tool in parallel with other tools or itself.
- `open_targets_search` - Search for disease-target associations from OpenTargets database. Adds new disease-target association data to the state and returns top search results.
- `collect_cited_papers_in_evidence` - Collect papers by traversing the citations of relevant papers to increase the paper count. This tool has no effect if called when paper count or relevant papers are zero. This tool will find papers that are likely to lead to more relevant evidence.
- `gather_evidence` - Gather evidence from previous papers, clinical trials, and disease-target data given a specific question. Each "evidence" is a synthesized summary from the raw sources, which can then be used in gen_answer.
- `clinical_trials_search` - Search for clinical trials, with support for repeated calls and concurrent execution. Will add new clinical trials to the state, and return metadata about the number of trials found.
- `paper_search` - Search for papers to increase the paper count. Can be called repeatedly with identical parameters to retrieve more results (max 2 repeats). This tool can be used concurrently with other tools for complementary research strategies.
- `gen_answer` - Generate an answer using current evidence. The tool may fail, indicating that better or different evidence should be found. Aim for at least five pieces of evidence from multiple sources before invoking this tool.

### OWL (`JobNames.OWL`)

**Job Name:** `job-futurehouse-hasanyone`  
**Task Type:** Precedent Search  
**Description:** Formerly known as HasAnyone, good for understanding if anyone has ever done something in science.

**Sample Queries:**

- Has anyone developed efficient non CRISPR methods for modifying DNA?
- Has anyone studied using a RAG system to help make better diagnoses for patients?
- Has anyone ever made an all-atom autoencoder for proteins?
- Has anyone used single-molecule footprinting to examine transcription factor binding in human cells?

**LLMs (priority order):**

- `openai/gpt-4.1-2025-04-14`
- `anthropic/claude-3-7-sonnet-20250219`
- `anthropic/claude-3-5-sonnet-20241022`
- `openai/gpt-4o-2024-11-20`

**Tools the agent uses:**

- `complete` - Terminate using the last proposed answer. Do not invoke this tool in parallel with other tools or itself.
- `open_targets_search` - Search for disease-target associations from OpenTargets database. Adds new disease-target association data to the state and returns top search results.
- `collect_cited_papers_in_evidence` - Collect papers by traversing the citations of relevant papers to increase the paper count. This tool has no effect if called when paper count or relevant papers are zero. This tool will find papers that are likely to lead to more relevant evidence.
- `gather_evidence` - Gather evidence from previous papers, clinical trials, and disease-target data given a specific question. Each "evidence" is a synthesized summary from the raw sources, which can then be used in gen_answer.
- `clinical_trials_search` - Search for clinical trials, with support for repeated calls and concurrent execution. Will add new clinical trials to the state, and return metadata about the number of trials found.
- `paper_search` - Search for papers to increase the paper count. Can be called repeatedly with identical parameters to retrieve more results (max 2 repeats). This tool can be used concurrently with other tools for complementary research strategies.
- `gen_answer` - Generate an answer using current evidence. The tool may fail, indicating that better or different evidence should be found. Aim for at least five pieces of evidence from multiple sources before invoking this tool.

### PHOENIX (`JobNames.PHOENIX`)

**Job Name:** `job-futurehouse-phoenix`  
**Task Type:** Chemistry Tasks (Experimental)  
**Description:** A new iteration of ChemCrow, Phoenix uses cheminformatics tools to do chemistry. Good for planning synthesis and designing new molecules.

**Sample Queries:**

- Has anyone used single-molecule footprinting to examine transcription factor binding in human cells?
- Show three examples of amide coupling reactions.
- Tell me how to synthesize safinamide & where to buy each reactant. Is it cheaper to make or buy it?

**LLMs (priority order):**

- `openai/gpt-4.1-2025-04-14`
- `anthropic/claude-3-7-sonnet-20250219`
- `anthropic/claude-3-5-sonnet-20241022`
- `openai/gpt-4o-2024-11-20`

**Tools the agent uses:**

- `submit_final_answer` - Submit final answer to the environment. Include SMILES for most discussed molecules, so that there are rendered structures. Put all SMILES or Reaction SMARTS/SMILES into XML tags of `<smiles>...</smiles>`.
- `get_cheapest_price_of_mol` - Get the N cheapest prices of a molecule from ChemSpace.
- `get_ghs` - Retrieve GHS classification of a molecule from PubChem.
- `get_ld50` - Retrieve LD50 value of a molecule from PubChem.
- `chem_wep` - Check a molecule against known databases for chemical weapons.
- `fda_approval` - Check the clintox database for FDA approval of a molecule.
- `similarity_quantifier` - Computes tanimoto similarity between two SMILES strings.
- `check_if_mol_is_smiles` - Check if a string is a valid SMILES.
- `query2smiles` - Converts query to smiles.
- `modify_mol` - Proposes small chemically accessible modifications to a compound.
- `query2name` - Converts query to molecule name.
- `query2cas` - Converts a query to its CAS number.
- `get_molecular_weight` - Calculate the molecular weight of a given molecule using its SMILES representation.
- `list_functional_groups` - List functional groups in a molecule given its SMILES representation.
- `reaction_info` - Get information about a reaction given the reaction smarts (including product).
- `mol_purchasable_check` - Check if a molecule is purchasable in common catalogs.
- `mol_solubility` - Predict the aqueous solubility in units of logS.
- `predict_reaction` - Predict the product of a reaction given reaction SMARTS (w/o product). Reaction SMARTS must be formatted as `reactants_smiles>reagents_smiles>`.
- `is_patented` - True, if molecule is patented, False otherwise. Use this to assess novelty.
- `predict_binders` - Propose small molecule binders for a given gene symbol, up to max_binders.
- `web_search` - Search web for a keyword query and get snippets of top 3 results.

---

**Sources:**

- [FutureHouse Platform API Documentation](https://futurehouse.gitbook.io/futurehouse-cookbook/futurehouse-client#quickstart)
- [FutureHouse Platform Models](https://platform.futurehouse.org/models)

## Architecture

The server provides simplified, LLM-tailored access to FutureHouse's AI agents:

- **Model-Specific Tools**: Each tool corresponds to a specific FutureHouse model optimized for different scientific tasks
- **Automatic Task Management**: Tasks run until completion with automatic status tracking
- **Task Continuation**: Build on previous queries by continuing tasks with follow-up questions
- **Standard Results**: All tools return consistent `FutureHouseResult` objects with task IDs, status, and answers

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

- Check the [FutureHouse Platform](https://platform.futurehouse.org/) documentation
- Review the example scripts in the repository
- Open an issue on the GitHub repository

## Credits

This MCP server provides access to FutureHouse's AI agents for scientific discovery:

- **CROW/FALCON**: Built with PaperQA2 for scientific literature search
- **OWL**: Precedent search (formerly HasAnyone)
- **PHOENIX**: Chemistry agent (iteration of ChemCrow)

For more information, visit [https://platform.futurehouse.org/](https://platform.futurehouse.org/)
