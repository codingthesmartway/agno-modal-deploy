"""
Generic Modal deployment script for Agno agents/teams using AG-UI protocol.

This script deploys any Agno agent or team to Modal using the AG-UI standardized 
protocol for front-end integration. Simply edit the AGENT_FILE variable below 
to point to your agent or team implementation file.

The script supports multiple agent/team patterns:
1. Function returning AGUIApp (e.g., create_agui_app())
2. Function returning Agent (e.g., create_agent())  
3. Function returning Team (e.g., create_team())
4. Direct AGUIApp variable export (e.g., app = AGUIApp(...))
5. Direct Agent variable export (e.g., agent = Agent(...))
6. Direct Team variable export (e.g., team = Team(...))

Features:
- AG-UI standardized protocol for front-end integration
- Automatic dependency management from requirements.txt
- Optional environment variable injection from .env
- Auto-scaling and production-ready configuration
- Flexible agent/team detection with multiple patterns
- Single agent OR single team deployment (AG-UI protocol requirement)

Usage:
    1. Edit AGENT_FILE variable below
    2. modal serve agno_modal_deploy_agui.py
    3. modal deploy agno_modal_deploy_agui.py
"""

import modal
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION 
# ============================================================================
# Edit this to point to your agent or team implementation file
AGENT_FILE = "agno_agents/financial_agent_agui_app.py"
# ============================================================================

agent_file_path = Path(AGENT_FILE)

# Validate the agent file exists
if not agent_file_path.exists():
    raise FileNotFoundError(f"Agent file not found: {agent_file_path}")

# Extract configuration from the filename
APP_NAME = agent_file_path.stem + "_agui"  # Add agui suffix to distinguish from FastAPI

# Convert file path to proper Python module import path
if agent_file_path.parent != Path('.'):
    # File is in a subdirectory, create module path with dots
    module_parts = list(agent_file_path.parent.parts) + [agent_file_path.stem]
    AGENT_MODULE = '.'.join(module_parts)
else:
    # File is in root directory
    AGENT_MODULE = agent_file_path.stem

print(f"🤖 Agent/Team file: {agent_file_path}")
print(f"📦 Modal app name: {APP_NAME}")
print(f"🎨 Protocol: AG-UI (standardized front-end integration)")
print(f"🚫 Authentication: DISABLED (AG-UI optimized for front-end use)")

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
    
    # Always include GitPython for Agno and ag-ui-protocol for AG-UI
    dependencies.add("GitPython")
    dependencies.add("ag-ui-protocol")
    
    if not requirements_file.exists():
        raise FileNotFoundError(
            f"❌ requirements.txt not found at {requirements_file}\n"
            f"   A requirements.txt file is required for deployment.\n"
            f"   Create one with: pip freeze > requirements.txt\n"
            f"   Make sure to include 'ag-ui-protocol' for AG-UI support."
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
    
    if len(dependencies) <= 2:  # Only GitPython and ag-ui-protocol
        raise ValueError(
            f"❌ No valid dependencies found in requirements.txt\n"
            f"   Please ensure your requirements.txt contains valid package specifications.\n"
            f"   Make sure to include 'ag-ui-protocol' for AG-UI support."
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

def detect_agui_pattern(agent_module):
    """
    Detect and validate AG-UI patterns in the module with priority-based selection.
    
    Priority order:
    1. Function returning AGUIApp (e.g., create_agui_app())
    2. Function returning Agent (e.g., create_agent())
    3. Function returning Team (e.g., create_team())
    4. Direct AGUIApp variable export
    5. Direct Agent variable export
    6. Direct Team variable export
    
    Returns:
        tuple: (pattern_type, callable_or_object, pattern_name)
        pattern_type: 'agui_function', 'agent_function', 'team_function', 
                     'agui_variable', 'agent_variable', 'team_variable'
    """
    from agno.agent import Agent
    from agno.team import Team
    try:
        from agno.app.agui.app import AGUIApp
    except ImportError:
        raise ImportError(
            "❌ AGUIApp not found. Please install the AG-UI integration:\n"
            "   pip install ag-ui-protocol\n"
            "   Make sure you have the latest version of Agno with AG-UI support."
        )
    
    import inspect
    
    # Get explicitly exported items if __all__ is defined
    if hasattr(agent_module, '__all__'):
        available_names = agent_module.__all__
        print(f"🔍 Found __all__ export list: {available_names}")
    else:
        # Get all non-private attributes
        available_names = [name for name in dir(agent_module) if not name.startswith('_')]
    
    # Collect candidates for each pattern
    agui_functions = []
    agent_functions = []
    team_functions = []
    agui_variables = []
    agent_variables = []
    team_variables = []
    
    for name in available_names:
        try:
            obj = getattr(agent_module, name)
            
            # Check if it's a callable (function) defined in this module
            if callable(obj) and not inspect.isclass(obj):
                # Only consider functions defined in this module (not imports)
                if hasattr(obj, '__module__') and obj.__module__ == agent_module.__name__:
                    func_name_lower = name.lower()
                    
                    # Check for AGUIApp function patterns
                    if name == 'create_agui_app' or (
                        'agui' in func_name_lower and 'app' in func_name_lower and name.startswith('create')
                    ):
                        agui_functions.append((name, obj))
                    # Check for Agent function patterns  
                    elif (
                        'agent' in func_name_lower and name.startswith('create')
                    ) or name == 'create_agent':
                        agent_functions.append((name, obj))
                    # Check for Team function patterns
                    elif (
                        'team' in func_name_lower and name.startswith('create')
                    ) or name == 'create_team':
                        team_functions.append((name, obj))
                
            # Check if it's a direct instance
            elif isinstance(obj, AGUIApp):
                agui_variables.append((name, obj))
            elif isinstance(obj, Agent):
                agent_variables.append((name, obj))
            elif isinstance(obj, Team):
                team_variables.append((name, obj))
                
        except Exception as e:
            # Skip any attributes that can't be accessed
            print(f"  ⚠️  Skipping {name}: {e}")
            continue
    
    # Report findings
    if agui_functions:
        print(f"🎯 Found AGUIApp functions: {[name for name, _ in agui_functions]}")
    if agent_functions:
        print(f"🤖 Found Agent functions: {[name for name, _ in agent_functions]}")
    if team_functions:
        print(f"👥 Found Team functions: {[name for name, _ in team_functions]}")
    if agui_variables:
        print(f"📱 Found AGUIApp variables: {[name for name, _ in agui_variables]}")
    if agent_variables:
        print(f"🔧 Found Agent variables: {[name for name, _ in agent_variables]}")
    if team_variables:
        print(f"⚡ Found Team variables: {[name for name, _ in team_variables]}")
    
    # Priority-based selection
    # 1. Function returning AGUIApp (highest priority)
    if agui_functions:
        if len(agui_functions) > 1:
            names = [name for name, _ in agui_functions]
            raise ValueError(f"❌ Multiple AGUIApp functions found: {names}. Please export only one using __all__ = ['{names[0]}']")
        name, func = agui_functions[0]
        return 'agui_function', func, name
    
    # 2. Function returning Agent
    if agent_functions:
        if len(agent_functions) > 1:
            names = [name for name, _ in agent_functions]
            raise ValueError(f"❌ Multiple Agent functions found: {names}. Please export only one using __all__ = ['{names[0]}']")
        name, func = agent_functions[0]
        return 'agent_function', func, name
    
    # 3. Function returning Team
    if team_functions:
        if len(team_functions) > 1:
            names = [name for name, _ in team_functions]
            raise ValueError(f"❌ Multiple Team functions found: {names}. Please export only one using __all__ = ['{names[0]}']")
        name, func = team_functions[0]
        return 'team_function', func, name
    
    # 4. Direct AGUIApp variable
    if agui_variables:
        if len(agui_variables) > 1:
            names = [name for name, _ in agui_variables]
            raise ValueError(f"❌ Multiple AGUIApp variables found: {names}. Please export only one using __all__ = ['{names[0]}']")
        name, var = agui_variables[0]
        return 'agui_variable', var, name
    
    # 5. Direct Agent variable
    if agent_variables:
        if len(agent_variables) > 1:
            names = [name for name, _ in agent_variables]
            raise ValueError(f"❌ Multiple Agent variables found: {names}. Please export only one using __all__ = ['{names[0]}']")
        name, var = agent_variables[0]
        return 'agent_variable', var, name
    
    # 6. Direct Team variable (lowest priority)
    if team_variables:
        if len(team_variables) > 1:
            names = [name for name, _ in team_variables]
            raise ValueError(f"❌ Multiple Team variables found: {names}. Please export only one using __all__ = ['{names[0]}']")
        name, var = team_variables[0]
        return 'team_variable', var, name
    
    # No valid patterns found
    raise ImportError(
        f"❌ No valid AG-UI pattern found in '{AGENT_MODULE}'. Supported patterns:\n"
        f"   1. Function returning AGUIApp (e.g., def create_agui_app() -> AGUIApp)\n"
        f"   2. Function returning Agent (e.g., def create_agent() -> Agent)\n"
        f"   3. Function returning Team (e.g., def create_team() -> Team)\n"
        f"   4. Direct AGUIApp variable (e.g., app = AGUIApp(agent=agent))\n"
        f"   5. Direct Agent variable (e.g., agent = Agent(...))\n"
        f"   6. Direct Team variable (e.g., team = Team(...))\n"
        f"   Use __all__ = ['function_or_variable_name'] to specify which to use if multiple exist."
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
def agui_app():
    """
    Auto-configured Modal deployment function for Agno agents/teams using AG-UI protocol.
    
    This function automatically detects and imports your agent or team implementation,
    supporting multiple patterns:
    1. Function returning AGUIApp
    2. Function returning Agent  
    3. Function returning Team
    4. Direct AGUIApp variable export
    5. Direct Agent variable export
    6. Direct Team variable export
    """
    import importlib
    from agno.agent import Agent
    from agno.team import Team
    
    try:
        from agno.app.agui.app import AGUIApp
    except ImportError:
        raise ImportError(
            "❌ AGUIApp not found. Please install the AG-UI integration:\n"
            "   pip install ag-ui-protocol\n"
            "   Make sure you have the latest version of Agno with AG-UI support."
        )
    
    # Warn if secrets weren't available during deployment
    if not has_env_file:
        print(f"⚠️  Warning: No .env file found during deployment.")
        print(f"   Your agent/team may not work properly without API keys.")
        print(f"   Create a .env file with your API keys and redeploy.")
    
    try:
        # Dynamically import the agent module
        agent_module = importlib.import_module(AGENT_MODULE)
        
        # Detect the AG-UI pattern
        pattern_type, pattern_object, pattern_name = detect_agui_pattern(agent_module)
        print(f"🎯 Detected pattern: {pattern_type} ({pattern_name})")
        
        # Handle different patterns
        if pattern_type == 'agui_function':
            # Function returning AGUIApp
            print(f"🚀 Loading AGUIApp from {AGENT_MODULE}.{pattern_name}()")
            agui_app_instance = pattern_object()
            
            if not isinstance(agui_app_instance, AGUIApp):
                raise TypeError(f"{pattern_name}() must return an AGUIApp instance, got {type(agui_app_instance)}")
            
            app_instance = agui_app_instance.get_app()
            
        elif pattern_type == 'agent_function':
            # Function returning Agent
            print(f"🚀 Loading Agent from {AGENT_MODULE}.{pattern_name}() and wrapping in AGUIApp")
            agent_instance = pattern_object()
            
            if not isinstance(agent_instance, Agent):
                raise TypeError(f"{pattern_name}() must return an Agent instance, got {type(agent_instance)}")
            
            # Wrap agent in AGUIApp
            agui_app_instance = AGUIApp(agent=agent_instance)
            app_instance = agui_app_instance.get_app()
            
        elif pattern_type == 'team_function':
            # Function returning Team
            print(f"🚀 Loading Team from {AGENT_MODULE}.{pattern_name}() and wrapping in AGUIApp")
            team_instance = pattern_object()
            
            if not isinstance(team_instance, Team):
                raise TypeError(f"{pattern_name}() must return a Team instance, got {type(team_instance)}")
            
            # Wrap team in AGUIApp
            agui_app_instance = AGUIApp(team=team_instance)
            app_instance = agui_app_instance.get_app()
            
        elif pattern_type == 'agui_variable':
            # Direct AGUIApp variable
            print(f"🚀 Loading AGUIApp from {AGENT_MODULE}.{pattern_name}")
            agui_app_instance = pattern_object
            app_instance = agui_app_instance.get_app()
            
        elif pattern_type == 'agent_variable':
            # Direct Agent variable
            print(f"🚀 Loading Agent from {AGENT_MODULE}.{pattern_name} and wrapping in AGUIApp")
            agent_instance = pattern_object
            
            # Wrap agent in AGUIApp
            agui_app_instance = AGUIApp(agent=agent_instance)
            app_instance = agui_app_instance.get_app()
            
        elif pattern_type == 'team_variable':
            # Direct Team variable
            print(f"🚀 Loading Team from {AGENT_MODULE}.{pattern_name} and wrapping in AGUIApp")
            team_instance = pattern_object
            
            # Wrap team in AGUIApp
            agui_app_instance = AGUIApp(team=team_instance)
            app_instance = agui_app_instance.get_app()
            
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        print(f"✅ AG-UI app successfully configured")
        print(f"🎨 Protocol: AG-UI standardized (POST /agui endpoint)")
        print(f"🔓 Authentication: DISABLED (optimized for front-end integration)")
        
        return app_instance
        
    except ImportError as e:
        print(f"❌ Failed to import agent/team module '{AGENT_MODULE}': {e}")
        print(f"   Make sure the file '{AGENT_MODULE}.py' exists and has a valid AG-UI pattern")
        raise
    except Exception as e:
        print(f"❌ Error creating AG-UI app: {e}")
        raise 