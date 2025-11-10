"""
MCP client entry point for HexStrike service.
"""
import sys
from pathlib import Path


def main() -> None:
    """Start the HexStrike MCP client."""
    # Add the parent directory to the path
    parent_dir = str(Path(__file__).parent.parent)
    sys.path.insert(0, parent_dir)

    try:
        import hexstrike_mcp
        print("Starting HexStrike MCP client...")
        # Execute the MCP client
        if hasattr(hexstrike_mcp, 'main'):
            hexstrike_mcp.main()
        else:
            print("HexStrike MCP client loaded successfully")
    except ImportError as e:
        print(f"Error importing hexstrike_mcp: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
