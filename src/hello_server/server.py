"""
👋 Welcome to your Smithery project!
To run your server, use "uv run dev"
To test interactively, use "uv run playground"

You might find this resources useful:

🧑‍💻 MCP's Python SDK (helps you define your server)
https://github.com/modelcontextprotocol/python-sdk
"""

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from smithery.decorators import smithery


# Optional: If you want to receive session-level config from user, define it here
class ConfigSchema(BaseModel):
    # access_token: str = Field(..., description="Your access token for authentication")
    pirate_mode: bool = Field(False, description="Speak like a pirate")
    num_papers: int = Field(5, description="Number of arXiv papers to return")


# For servers with configuration:
@smithery.server(config_schema=ConfigSchema)
# For servers without configuration, simply use:
# @smithery.server()
def create_server():
    """Create and configure the MCP server."""

    # Create your FastMCP server as usual
    server = FastMCP("Say Hello and search arXiv")

    # Add a tool
    @server.tool()
    def hello(name: str, ctx: Context) -> str:
        """Say hello to someone."""
        # Access session-specific config through context
        session_config = ctx.session_config

        # In real apps, use token for API requests:
        # requests.get(url, headers={"Authorization": f"Bearer {session_config.access_token}"})
        # if not session_config.access_token:
        #     return "Error: Access token required"

        # Create greeting based on pirate mode
        if session_config.pirate_mode:
            return f"Ahoy, {name}!"
        else:
            return f"Hello, {name}!"

    # Tool: Find new arXiv papers in a category from the last day (via RSS)
    @server.tool()
    def fetch_current_arxiv_postings_rss(category: str, ctx: Context) -> list:
        """
        Returns all of today's brand-new arXiv submissions in a category via RSS.
        """
        import feedparser

        url = f"https://rss.arxiv.org/rss/{category}"
        feed = feedparser.parse(url)

        results = []
        for e in feed.entries:
            announce_type = getattr(e, "arxiv_announce_type", None)
            if "replace" in announce_type.lower():
                continue  # skip replaced articles but keeps new cross-lists

            results.append({
                "title": e.title,
                "authors": e.get("authors", []),
                "summary": e.summary,
                "url": e.link,
                "published": str(e.published) if hasattr(e, "published") else None,
            })

        return results

    # Tool: Find new arXiv papers in a category from the last day (via RSS), filtered by keyword
    @server.tool()
    def keyword_search_arxiv_rss(category: str, keyword: str, ctx: Context) -> list:
        """Search the daily arXiv RSS feed for a category, filtering by keyword in title or summary."""
        import feedparser


        keyword_lower = keyword.lower()

        url = f"https://rss.arxiv.org/rss/{category}"
        feed = feedparser.parse(url)

        results = []
        for e in feed.entries:

            announce_type = getattr(e, "arxiv_announce_type", None)
            if "replace" in announce_type.lower():
                continue  # skip replaced articles but keeps cross-lists

            text = (e.title + " " + e.summary).lower()
            if keyword_lower in text:
                results.append({
                    "title": e.title,
                    "authors": e.get("authors", []),   # RSS usually provides this
                    "summary": e.summary,
                    "url": e.link,
                    "published": str(e.published) if hasattr(e, "published") else None,
                })

        return results

    # Add a resource
    @server.resource("history://hello-world")
    def hello_world() -> str:
        """The origin story of the famous 'Hello, World' program."""
        return (
            '"Hello, World" first appeared in a 1972 Bell Labs memo by '
            "Brian Kernighan and later became the iconic first program "
            "for beginners in countless languages."
        )

    # Add a prompt
    @server.prompt()
    def greet(name: str) -> list:
        """Generate a greeting prompt."""
        return [
            {
                "role": "user",
                "content": f"Say hello to {name}",
            },
        ]

    return server
