import asyncio
import sys
import os
import logging
import sys
import os

# Get the same logger instance used in server.py
# Configuration is handled in server.py
logger = logging.getLogger("excel-mcp")

# 添加父目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

try:
    # 嘗試導入 run_server
    from excel_mcp.server import run_server
except ImportError:
    # 如果導入失敗，使用直接導入
    import importlib.util
    server_path = os.path.join(current_dir, 'server.py')
    spec = importlib.util.spec_from_file_location('server', server_path)
    server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server)
    run_server = server.run_server

async def main(): # Make main async
    """Start the Excel MCP server."""
    try:
        # These logs should now go to excel-mcp.log via the "excel-mcp" logger
        logger.info("Excel MCP Server")
        if logger.handlers: logger.handlers[0].flush() # Flush after logging
        logger.info("---------------")
        if logger.handlers: logger.handlers[0].flush() # Flush after logging
        logger.info("Starting server... Press Ctrl+C to exit")
        if logger.handlers: logger.handlers[0].flush() # Flush after logging
        logger.info(f"Python path: {sys.path}")
        if logger.handlers: logger.handlers[0].flush() # Flush after logging
        # Directly await run_server since mcp.run() handles the loop for stdio
        await run_server()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        if logger.handlers: logger.handlers[0].flush() # Flush on exit
        pass # Keep the process quiet on exit
    except Exception as e:
        # Use logger.exception to include traceback information automatically
        logger.exception(f"Error: {e}")
        if logger.handlers: logger.handlers[0].flush() # Flush on error
        # traceback.print_exc() is no longer needed as logger.exception handles it
    finally:
        logger.info("Server stopped.")
        if logger.handlers: logger.handlers[0].flush() # Flush in finally
        pass # Keep the process quiet on exit

if __name__ == "__main__":
    # Run the async main function
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # Handle potential loop-already-running errors if script is run in certain environments
        if "Cannot run the event loop while another loop is running" in str(e):
            # If a loop is already running, just run the main coroutine in the existing loop
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise # Re-raise other RuntimeErrors
    except Exception as e:
        # Use logger.exception to include traceback information automatically
        logger.exception(f"Top-level error during script execution: {e}")
        if logger.handlers: # Check if handlers exist before flushing
            for handler in logger.handlers: handler.flush()
    # No finally block needed here unless specific cleanup is required
