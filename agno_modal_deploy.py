"""
Generic Modal deployment script for Agno agents using FastAPIApp.

This script deploys any Agno agent to Modal. Simply edit the AGENT_FILE
variable below to point to your agent implementation file.

Usage:
    1. Edit AGENT_FILE variable below
    2. modal serve agno_modal_deploy.py
    3. modal deploy agno_modal_deploy.py
"""

import modal
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION - Edit this to point to your agent implementation file
# ============================================================================
AGENT_FILE = "financial_agent_app.py"  
# ============================================================================

agent_file_path = Path(AGENT_FILE)

# Validate the agent file exists
if not agent_file_path.exists():
    raise FileNotFoundError(f"Agent file not found: {agent_file_path}")

# Extract configuration from the filename
APP_NAME = agent_file_path.stem  # filename without .py extension
AGENT_MODULE = APP_NAME

print(f"🤖 Agent file: {agent_file_path}")
print(f"📦 Modal app name: {APP_NAME}")

def load_env_file():
    """
    Check if .env file exists and return whether secrets should be loaded.
    """
    env_file_path = Path(__file__).parent / ".env"
    
    if env_file_path.exists():
        print(f"📄 Found .env file at {env_file_path}")
        return True
    else:
        print(f"📄 No .env file found at {env_file_path}")
        print(f"   Create a .env file with your API keys for automatic secret injection")
        return False

# Check if .env file exists
has_env_file = load_env_file()

def load_requirements():
    """
    Load Python dependencies from requirements.txt file.
    Requires requirements.txt to exist - no fallback dependencies.
    """
    requirements_file = Path(__file__).parent / "requirements.txt"
    dependencies = set()
    
    # Always include GitPython for Agno
    dependencies.add("GitPython")
    
    if not requirements_file.exists():
        raise FileNotFoundError(
            f"❌ requirements.txt not found at {requirements_file}\n"
            f"   A requirements.txt file is required for deployment.\n"
            f"   Create one with: pip freeze > requirements.txt"
        )
    
    print(f"📦 Loading dependencies from {requirements_file}")
    try:
        with open(requirements_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Handle -e editable installs (skip them)
                if line.startswith('-e '):
                    print(f"  ⚠️  Line {line_num}: Skipping editable install: {line}")
                    continue
                
                # Handle -r recursive requirements (skip them for now)
                if line.startswith('-r '):
                    print(f"  ⚠️  Line {line_num}: Skipping recursive requirement: {line}")
                    continue
                
                # Clean up the dependency line
                # Remove inline comments
                if '#' in line:
                    line = line.split('#')[0].strip()
                
                if line:
                    dependencies.add(line)
                    print(f"  📋 Added: {line}")
    
    except Exception as e:
        raise RuntimeError(
            f"❌ Error reading requirements.txt: {e}\n"
            f"   Please fix the requirements.txt file and try again."
        )
    
    if len(dependencies) <= 1:  # Only GitPython
        raise ValueError(
            f"❌ No valid dependencies found in requirements.txt\n"
            f"   Please ensure your requirements.txt contains valid package specifications."
        )
    
    # Convert to sorted list for consistent builds
    deps_list = sorted(list(dependencies))
    print(f"📦 Total dependencies: {len(deps_list)}")
    return deps_list

# Load dependencies dynamically
python_dependencies = load_requirements()

# Create Modal app
app = modal.App(APP_NAME)

# Define the container image with dynamic dependencies from requirements.txt
image = (
    modal.Image.debian_slim()
    .apt_install("git") 
    .pip_install(python_dependencies)  # Use dynamic dependencies
    .env({"GIT_PYTHON_REFRESH": "quiet"})  # Suppress git warnings
    .add_local_dir(".", remote_path="/root")  # Include local files
)

@app.function(
    image=image,
    # Deployment configuration - adjust based on your needs
    max_containers=int(os.getenv("MAX_CONTAINERS", "10")),
    min_containers=int(os.getenv("MIN_CONTAINERS", "1")),
    timeout=int(os.getenv("TIMEOUT", "300")),
    # Use Modal's built-in from_dotenv() to automatically load .env file
    secrets=[
        modal.Secret.from_dotenv()
    ] if has_env_file else [],
)
@modal.concurrent(max_inputs=int(os.getenv("MAX_CONCURRENT", "100")))
@modal.asgi_app()
def fastapi_app():
    """
    Auto-configured Modal deployment function for Agno agents using FastAPIApp.
    
    This function automatically detects and imports your agent implementation,
    expecting a self-contained create_fastapi_app() function.
    """
    import importlib
    from agno.app.fastapi.app import FastAPIApp
    
    # Warn if secrets weren't available during deployment
    if not has_env_file:
        print(f"⚠️  Warning: No .env file found during deployment.")
        print(f"   Your agent may not work properly without API keys.")
        print(f"   Create a .env file with your API keys and redeploy.")
    
    try:
        # Dynamically import the agent module
        agent_module = importlib.import_module(AGENT_MODULE)
        
        # Expect a self-contained create_fastapi_app() function
        if hasattr(agent_module, 'create_fastapi_app'):
            print(f"🚀 Loading agent from {AGENT_MODULE}.create_fastapi_app()")
            fastapi_app = agent_module.create_fastapi_app()
            
            if not isinstance(fastapi_app, FastAPIApp):
                raise TypeError(f"create_fastapi_app() must return a FastAPIApp instance, got {type(fastapi_app)}")
            
            return fastapi_app.get_app()
        else:
            raise ImportError(f"Agent module '{AGENT_MODULE}' must have a 'create_fastapi_app()' function that returns a FastAPIApp instance")
    
    except ImportError as e:
        print(f"❌ Failed to import agent module '{AGENT_MODULE}': {e}")
        print(f"   Make sure the file '{AGENT_MODULE}.py' exists and has a create_fastapi_app() function")
        raise
    except Exception as e:
        print(f"❌ Error creating FastAPI app: {e}")
        raise 