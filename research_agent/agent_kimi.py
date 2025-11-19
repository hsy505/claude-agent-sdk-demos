"""Research agent using Moonshot Kimi API with web search."""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Constants
RESEARCH_NOTES_DIR = Path("files/research_notes")
REPORTS_DIR = Path("files/reports")
LOGS_DIR = Path("logs")

# Ensure directories exist
RESEARCH_NOTES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


class KimiResearchAgent:
    """Research agent using Kimi API with web search capabilities."""

    def __init__(self, api_key: str, model: str = "moonshot-v1-auto"):
        """
        Initialize the Kimi research agent.

        Args:
            api_key: Moonshot API key
            model: Model name (default: moonshot-v1-auto for web search support)
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )
        self.model = model
        self.conversation_history = []

        # Session tracking
        session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = LOGS_DIR / f"session_{session_timestamp}"
        self.session_dir.mkdir(exist_ok=True)
        self.transcript_file = self.session_dir / "transcript.txt"

    def log(self, message: str, to_console: bool = True, to_file: bool = True):
        """Log message to console and/or file."""
        if to_console:
            print(message)
        if to_file:
            with open(self.transcript_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")

    def research_topic(self, topic: str, subtopics: list[str]) -> dict:
        """
        Research a topic by breaking it down into subtopics.

        Args:
            topic: Main research topic
            subtopics: List of subtopics to research

        Returns:
            Dict with research results for each subtopic
        """
        results = {}

        self.log(f"\n=== Researching: {topic} ===")
        self.log(f"Subtopics: {', '.join(subtopics)}\n")

        for i, subtopic in enumerate(subtopics, 1):
            self.log(f"\n[{i}/{len(subtopics)}] Researching: {subtopic}")

            # Create research prompt
            research_prompt = f"""You are a research specialist. Research the following subtopic using web search:

Subtopic: {subtopic}

Instructions:
1. Use web search to find current, authoritative information
2. Focus on recent developments and reliable sources
3. Keep your findings concise (3-4 paragraphs maximum)
4. Include key facts, statistics, and source URLs
5. Summarize the most important findings

Provide a well-structured research summary."""

            try:
                # Call Kimi API with web search tool
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a thorough research assistant with access to web search. Always search the web for current information."},
                        {"role": "user", "content": research_prompt}
                    ],
                    tools=[{
                        "type": "web_search",
                        "web_search": {
                            "search_query": subtopic
                        }
                    }],
                    temperature=0.3,
                )

                result = response.choices[0].message.content
                results[subtopic] = result

                # Save to file
                filename = f"{subtopic.lower().replace(' ', '_')[:50]}.md"
                filepath = RESEARCH_NOTES_DIR / filename

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {subtopic}\n\n")
                    f.write(f"*Researched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                    f.write(result)

                self.log(f"✓ Saved to: {filepath}")
                self.log(f"\nFindings preview:\n{result[:200]}...\n")

            except Exception as e:
                error_msg = f"✗ Error researching '{subtopic}': {str(e)}"
                self.log(error_msg)
                results[subtopic] = f"Error: {str(e)}"

        return results

    def generate_report(self, topic: str) -> str:
        """
        Generate a comprehensive report from research notes.

        Args:
            topic: Main research topic

        Returns:
            Path to generated report
        """
        self.log("\n=== Generating Report ===")

        # Read all research notes
        research_notes = []
        for note_file in RESEARCH_NOTES_DIR.glob("*.md"):
            with open(note_file, "r", encoding="utf-8") as f:
                content = f.read()
                research_notes.append(f"## From: {note_file.name}\n\n{content}\n")

        if not research_notes:
            self.log("✗ No research notes found!")
            return None

        # Create report generation prompt
        combined_notes = "\n---\n".join(research_notes)

        report_prompt = f"""You are a professional report writer. Create a comprehensive research report based on the following research notes.

Topic: {topic}

Research Notes:
{combined_notes}

Instructions:
1. Synthesize all research findings into a cohesive report
2. Organize information logically with clear sections
3. Include key findings, trends, and insights
4. Cite sources where mentioned in the research notes
5. Keep the report concise but comprehensive (2-3 pages)
6. Use professional formatting with markdown

Generate a well-structured final report."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional report writer who synthesizes research into clear, well-organized documents."},
                    {"role": "user", "content": report_prompt}
                ],
                temperature=0.3,
            )

            report_content = response.choices[0].message.content

            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{topic.lower().replace(' ', '_')[:50]}_report_{timestamp}.md"
            filepath = REPORTS_DIR / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# Research Report: {topic}\n\n")
                f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                f.write("---\n\n")
                f.write(report_content)

            self.log(f"✓ Report saved to: {filepath}")
            return str(filepath)

        except Exception as e:
            error_msg = f"✗ Error generating report: {str(e)}"
            self.log(error_msg)
            return None

    def process_research_request(self, user_request: str):
        """
        Process a research request end-to-end.

        Args:
            user_request: User's research request
        """
        self.log(f"\nUser: {user_request}\n", to_console=False)
        self.log("Agent: Analyzing research request...")

        # Use Kimi to break down the request into subtopics
        breakdown_prompt = f"""Break down this research request into 2-4 specific subtopics to investigate:

Request: {user_request}

Provide ONLY a JSON response in this exact format:
{{
    "topic": "main topic name",
    "subtopics": ["subtopic 1", "subtopic 2", "subtopic 3"]
}}

Keep subtopics focused and specific. Each should be 3-8 words."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a research coordinator who breaks down complex topics into focused subtopics. Respond ONLY with valid JSON."},
                    {"role": "user", "content": breakdown_prompt}
                ],
                temperature=0.3,
            )

            # Parse the response
            breakdown_text = response.choices[0].message.content.strip()

            # Extract JSON from response (handle potential markdown code blocks)
            if "```json" in breakdown_text:
                breakdown_text = breakdown_text.split("```json")[1].split("```")[0].strip()
            elif "```" in breakdown_text:
                breakdown_text = breakdown_text.split("```")[1].split("```")[0].strip()

            breakdown = json.loads(breakdown_text)
            topic = breakdown["topic"]
            subtopics = breakdown["subtopics"]

            self.log(f"\nTopic: {topic}")
            self.log(f"Breaking into {len(subtopics)} subtopics: {', '.join(subtopics)}\n")

            # Conduct research
            self.research_topic(topic, subtopics)

            # Generate report
            report_path = self.generate_report(topic)

            if report_path:
                self.log(f"\n✓ Research complete! Report saved to: {report_path}\n")
            else:
                self.log("\n✗ Failed to generate report.\n")

        except Exception as e:
            self.log(f"\n✗ Error processing request: {str(e)}\n")


async def chat():
    """Start interactive chat with the research agent."""

    # Check API key
    api_key = os.environ.get("MOONSHOT_API_KEY")
    if not api_key:
        print("\nError: MOONSHOT_API_KEY not found.")
        print("Set it in a .env file or export it in your shell.")
        print("Get your key at: https://platform.moonshot.cn/console/api-keys\n")
        return

    # Initialize agent
    agent = KimiResearchAgent(api_key)

    print("\n=== Kimi Research Agent ===")
    print("Ask me to research any topic and I'll gather information using web search.")
    print("I will break down complex topics, research each aspect, and generate a comprehensive report.")
    print(f"\nSession logs: {agent.session_dir}")
    print("Type 'exit' or 'quit' to end.\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ["exit", "quit", "q"]:
            break

        # Process the research request
        agent.process_research_request(user_input)

    print(f"\nGoodbye! Session logs saved to: {agent.session_dir}")


if __name__ == "__main__":
    asyncio.run(chat())
