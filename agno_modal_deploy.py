"""
Generic Modal deployment script for Agno agents using FastAPIApp.

This script deploys any Agno agent to Modal. Simply edit the AGENT_FILE
variable below to point to your agent implementation file.

Features:
- Automatic dependency management from requirements.txt
- Optional environment variable injection from .env
- Optional token-based authentication
- Auto-scaling and production-ready configuration

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
# Authentication Configuration
ENABLE_AUTH = False   # Set to False to disable authentication
PROTECT_DOCS = False  # Set to False to make /docs publicly accessible
# ============================================================================

# Sensitive authentication data (keep in .env file)
# Note: AUTH_TOKEN validation happens inside fastapi_app() where .env is loaded
AUTH_TOKEN = None  # Will be loaded from environment when needed

agent_file_path = Path(AGENT_FILE)

# Validate the agent file exists
if not agent_file_path.exists():
    raise FileNotFoundError(f"Agent file not found: {agent_file_path}")

# Extract configuration from the filename
APP_NAME = agent_file_path.stem  # filename without .py extension
AGENT_MODULE = APP_NAME

print(f"🤖 Agent file: {agent_file_path}")
print(f"📦 Modal app name: {APP_NAME}")
if ENABLE_AUTH:
    print(f"🔒 Authentication: ENABLED (token will be validated from .env)")
    print(f"📚 Docs protection: {'ENABLED' if PROTECT_DOCS else 'DISABLED'}")
else:
    print(f"🔓 Authentication: DISABLED (public access)")

def validate_auth_configuration():
    """
    Validate authentication configuration at deployment time.
    This runs before deployment to catch configuration errors early.
    """
    if not ENABLE_AUTH:
        return  # No validation needed if auth is disabled
    
    # Check if .env file exists
    env_file_path = Path(__file__).parent / ".env"
    if not env_file_path.exists():
        raise ValueError(
            "❌ Authentication is enabled (ENABLE_AUTH=True) but no .env file found.\n"
            f"   Create a .env file at {env_file_path} with AUTH_TOKEN=your-token\n"
            "   Or set ENABLE_AUTH=False to disable authentication."
        )
    
    # Check if AUTH_TOKEN is in .env file
    with open(env_file_path, 'r') as f:
        env_content = f.read()
    
    # Look for AUTH_TOKEN in the file (commented or uncommented)
    if 'AUTH_TOKEN=' not in env_content:
        raise ValueError(
            "❌ Authentication is enabled (ENABLE_AUTH=True) but AUTH_TOKEN not found in .env file.\n"
            "   Add AUTH_TOKEN=your-secret-token to your .env file\n"
            "   Or set ENABLE_AUTH=False to disable authentication."
        )
    
    # Check if AUTH_TOKEN is commented out
    active_auth_tokens = [line for line in env_content.split('\n') 
                         if line.strip().startswith('AUTH_TOKEN=') and not line.strip().startswith('#')]
    
    if not active_auth_tokens:
        raise ValueError(
            "❌ Authentication is enabled (ENABLE_AUTH=True) but AUTH_TOKEN is commented out in .env file.\n"
            "   Uncomment the AUTH_TOKEN line in your .env file\n"
            "   Or set ENABLE_AUTH=False to disable authentication."
        )
    
    print(f"✅ Authentication configuration validated successfully")

# Run validation at deployment time
validate_auth_configuration()

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
    
    # Only define middleware class if authentication is enabled
    if ENABLE_AUTH:
        from fastapi import Request
        from fastapi.responses import JSONResponse
        import json
        
        class TokenAuthMiddleware:
            """Token-based authentication middleware using ASGI interface"""
            
            def __init__(self, app, token: str, protect_docs: bool = True):
                self.app = app
                self.token = token
                self.protect_docs = protect_docs
                
                # Endpoints that are always public (no auth required)
                # Note: /openapi.json must always be public for docs UI to work
                self.public_endpoints = {"/health", "/openapi.json"}
                
                # Conditionally add docs endpoints to public list
                if not protect_docs:
                    self.public_endpoints.update({"/docs", "/redoc"})
            
            async def __call__(self, scope, receive, send):
                if scope["type"] != "http":
                    await self.app(scope, receive, send)
                    return
                
                path = scope["path"]
                
                # Allow public endpoints without authentication
                if path in self.public_endpoints:
                    await self.app(scope, receive, send)
                    return
                
                # Check for Authorization header
                headers = dict(scope["headers"])
                auth_header = headers.get(b"authorization")
                
                if not auth_header:
                    await self._send_auth_error(send, "Missing Authorization header")
                    return
                
                # Validate Bearer token format
                auth_str = auth_header.decode("utf-8")
                if not auth_str.startswith("Bearer "):
                    await self._send_auth_error(send, "Invalid Authorization header format. Expected: Bearer <token>")
                    return
                
                # Extract and validate token
                provided_token = auth_str[7:]  # Remove "Bearer " prefix
                if provided_token != self.token:
                    await self._send_auth_error(send, "Invalid authentication token")
                    return
                
                # Token is valid, proceed with request
                await self.app(scope, receive, send)
            
            async def _send_auth_error(self, send, message: str):
                """Send 401 Unauthorized response"""
                response = {
                    "error": "Authentication required",
                    "message": message,
                    "hint": "Include 'Authorization: Bearer <your-token>' header"
                }
                
                response_body = json.dumps(response).encode("utf-8")
                
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        [b"content-type", b"application/json"],
                        [b"content-length", str(len(response_body)).encode()],
                    ],
                })
                await send({
                    "type": "http.response.body",
                    "body": response_body,
                })
    
    try:
        # Dynamically import the agent module
        agent_module = importlib.import_module(AGENT_MODULE)
        
        # Expect a self-contained create_fastapi_app() function
        if hasattr(agent_module, 'create_fastapi_app'):
            print(f"🚀 Loading agent from {AGENT_MODULE}.create_fastapi_app()")
            fastapi_app = agent_module.create_fastapi_app()
            
            if not isinstance(fastapi_app, FastAPIApp):
                raise TypeError(f"create_fastapi_app() must return a FastAPIApp instance, got {type(fastapi_app)}")
            
            # Get the FastAPI instance
            app_instance = fastapi_app.get_app()
            
            # Apply token-based authentication if enabled
            if ENABLE_AUTH:
                # Load AUTH_TOKEN from environment (validated at deployment time)
                AUTH_TOKEN = os.getenv("AUTH_TOKEN")
                
                print(f"🔒 Adding authentication middleware")
                
                # Add security scheme to show lock symbol in docs
                from fastapi.security import HTTPBearer
                from fastapi import Depends
                
                # Create security scheme
                security = HTTPBearer(auto_error=False, description="Enter your authentication token")
                
                # Add security dependency to ALL existing routes to show lock symbols
                from fastapi.dependencies.utils import get_dependant
                
                for route in app_instance.routes:
                    # Only process API routes (not static files, etc.)
                    if hasattr(route, 'dependant') and hasattr(route, 'path'):
                        # Skip public endpoints
                        if route.path in {"/health", "/openapi.json"}:
                            continue
                        if not PROTECT_DOCS and route.path in {"/docs", "/redoc"}:
                            continue
                        
                        # Add security dependency to show lock symbol
                        def auth_dep(token: str = Depends(security)):
                            return token
                        
                        security_dependant = get_dependant(path=route.path, call=auth_dep)
                        
                        # Add to route's dependencies
                        if hasattr(route.dependant, 'dependencies'):
                            route.dependant.dependencies.append(security_dependant)
                
                # Force regenerate OpenAPI schema to include the security scheme
                app_instance.openapi_schema = None
                
                # Wrap the app with ASGI middleware (this does the actual auth)
                app_instance = TokenAuthMiddleware(app_instance, token=AUTH_TOKEN, protect_docs=PROTECT_DOCS)
            
            return app_instance
        else:
            raise ImportError(f"Agent module '{AGENT_MODULE}' must have a 'create_fastapi_app()' function that returns a FastAPIApp instance")
    
    except ImportError as e:
        print(f"❌ Failed to import agent module '{AGENT_MODULE}': {e}")
        print(f"   Make sure the file '{AGENT_MODULE}.py' exists and has a create_fastapi_app() function")
        raise
    except Exception as e:
        print(f"❌ Error creating FastAPI app: {e}")
        raise 