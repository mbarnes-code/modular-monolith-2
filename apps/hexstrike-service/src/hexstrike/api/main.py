"""
Main entry point for HexStrike API server.
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import hexstrike modules
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)


def main() -> None:
    """Start the HexStrike server."""
    # Import here to avoid circular imports
    try:
        # Import and run the original server
        import hexstrike_server

        # Execute the server's main functionality
        if hasattr(hexstrike_server, 'main'):
            hexstrike_server.main()
        elif hasattr(hexstrike_server, 'app'):
            # If it's a Flask app, run it
            hexstrike_server.app.run(host='0.0.0.0', port=8000, debug=True)
        else:
            print("Starting HexStrike service...")
            # Fallback: just run the module
            exec(open(os.path.join(parent_dir, 'hexstrike_server.py')).read())
    except ImportError as e:
        print(f"Error importing hexstrike_server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
