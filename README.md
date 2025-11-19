# Multi-Agent Research System

A research system that uses Moonshot Kimi API to research any topic and generate comprehensive reports with web search capabilities.

## Features

- **Web Search Integration**: Uses Kimi's built-in web search to find current, authoritative information
- **Automated Topic Breakdown**: Intelligently divides complex topics into focused subtopics
- **Parallel Research**: Investigates multiple subtopics efficiently
- **Report Generation**: Synthesizes findings into professional, well-organized reports
- **Session Logging**: Tracks all research activities with detailed logs

## Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Set Your API Key

Get your API key from [Moonshot Console](https://platform.moonshot.cn/console/api-keys)

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key
MOONSHOT_API_KEY=your_moonshot_api_key_here
```

### 3. Run the Agent

```bash
# Using uv
uv run research_agent/agent_kimi.py

# Or using python
python research_agent/agent_kimi.py
```

## Usage Examples

Try these research queries:

```
Research quantum computing developments in 2025
研究2025年人工智能的最新进展
What are current trends in renewable energy?
分析电动汽车市场的现状和未来趋势
```

## How It Works

1. **User Input**: You provide a research topic
2. **Topic Analysis**: Kimi breaks down the topic into 2-4 focused subtopics
3. **Web Research**: Each subtopic is researched using web search
4. **Note Taking**: Research findings are saved to `files/research_notes/`
5. **Report Writing**: All findings are synthesized into a comprehensive report in `files/reports/`

## Project Structure

```
.
├── research_agent/
│   ├── agent_kimi.py          # Main Kimi-based research agent
│   ├── agent.py               # Original Claude-based agent (legacy)
│   ├── prompts/               # System prompts (for legacy version)
│   └── utils/                 # Utility modules (for legacy version)
├── files/
│   ├── research_notes/        # Individual research findings
│   └── reports/               # Final synthesized reports
├── logs/                      # Session transcripts and logs
├── pyproject.toml            # Project dependencies
└── README.md                 # This file
```

## API Information

### Moonshot Kimi API

- **Endpoint**: `https://api.moonshot.cn/v1`
- **Model**: `moonshot-v1-auto` (supports web search)
- **Documentation**: [Kimi API Docs](https://platform.moonshot.cn/docs)
- **Console**: [Moonshot Console](https://platform.moonshot.cn/console)

### Supported Models

- `moonshot-v1-auto` - Auto-selects best model, supports web search (recommended)
- `moonshot-v1-8k` - 8K context window
- `moonshot-v1-32k` - 32K context window
- `moonshot-v1-128k` - 128K context window

## Configuration

### Environment Variables

```bash
MOONSHOT_API_KEY=your_api_key_here  # Required
```

### Customization

You can modify the agent behavior by editing `research_agent/agent_kimi.py`:

- **Model Selection**: Change `model="moonshot-v1-auto"` to use different models
- **Temperature**: Adjust creativity (0.0 = focused, 1.0 = creative)
- **Output Directories**: Customize paths for research notes and reports

## Output Files

### Research Notes (`files/research_notes/`)

Individual markdown files for each subtopic:
- Focused findings from web search
- Source URLs and citations
- Timestamp of research

### Reports (`files/reports/`)

Comprehensive synthesized reports:
- Professional formatting
- Organized sections
- Consolidated insights
- Full citations

### Session Logs (`logs/session_YYYYMMDD_HHMMSS/`)

- `transcript.txt` - Full conversation and activity log

## Advanced Usage

### Programmatic Use

```python
from research_agent.agent_kimi import KimiResearchAgent
import os

# Initialize agent
agent = KimiResearchAgent(
    api_key=os.environ.get("MOONSHOT_API_KEY"),
    model="moonshot-v1-auto"
)

# Process research request
agent.process_research_request("Research quantum computing")
```

### Custom Research Flow

```python
# Manual control over research steps
agent = KimiResearchAgent(api_key=your_key)

# 1. Research specific subtopics
results = agent.research_topic(
    topic="AI Development",
    subtopics=["GPT models", "Computer Vision", "Reinforcement Learning"]
)

# 2. Generate report
report_path = agent.generate_report("AI Development")
```

## Comparison: Kimi vs Claude Version

| Feature | Kimi Version | Claude Version (Legacy) |
|---------|-------------|------------------------|
| Web Search | ✓ Built-in | ✓ Via WebSearch tool |
| Multi-Agent | Sequential | Parallel (via Task tool) |
| API Cost | Lower | Higher |
| Chinese Support | ✓ Excellent | Limited |
| Setup Complexity | Simple | Complex (SDK required) |

## Troubleshooting

### API Key Issues

```
Error: MOONSHOT_API_KEY not found
```

**Solution**: Make sure you've set the environment variable in `.env` file

### Connection Errors

```
Error: Connection timeout
```

**Solution**: Check your internet connection and verify API endpoint is accessible

### Import Errors

```
ModuleNotFoundError: No module named 'openai'
```

**Solution**: Install dependencies with `uv sync` or `pip install openai python-dotenv`

## License

MIT License - Feel free to use and modify for your projects.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

- **API Issues**: Contact Moonshot support at [platform.moonshot.cn](https://platform.moonshot.cn)
- **Code Issues**: Open an issue on GitHub

## Acknowledgments

- Built with [Moonshot Kimi API](https://platform.moonshot.cn)
- Inspired by multi-agent research methodologies
