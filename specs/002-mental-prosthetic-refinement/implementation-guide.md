# Implementation Guide: Repository Restructure Commands

## Summary of Required Changes

Based on your current structure and the hybrid domain-based architecture decision, here are the **specific changes** needed:

### Current State → Target State:

| Current | Target | Action |
|---------|--------|--------|
| `apps/jane-orchestrator/` | Split into 4 domain services | Remove & distribute |
| `features/` (37 tools) | Domain services | Migrate all tools |
| Single orchestrator | n8n workflow service | Create new service |
| `apps/code-llm-server/` | `apps/infrastructure-llm-server/` | Rename |

## Step-by-Step Implementation

### 1. Create New Domain Services

```bash
# Create the 5 new services using NX generators
npx nx generate @nx/node:application n8n-workflow-service --framework=express
npx nx generate @nx/node:application security-service --framework=express  
npx nx generate @nx/node:application productivity-service --framework=express
npx nx generate @nx/node:application mtg-service --framework=express
npx nx generate @nx/node:application infrastructure-service --framework=express

# Rename existing AI server for consistency
mv apps/code-llm-server apps/infrastructure-llm-server
```

### 2. Set Up Domain Service Structure

Each domain service needs the same internal structure:

```bash
# Function to create domain service structure
create_domain_structure() {
    local service_name=$1
    mkdir -p "apps/${service_name}/src/api"
    mkdir -p "apps/${service_name}/src/data"
    mkdir -p "apps/${service_name}/src/services"
    mkdir -p "apps/${service_name}/src/ai"
    mkdir -p "apps/${service_name}/src/domains"
    
    # Create FastAPI main.py for each service
    cat > "apps/${service_name}/src/main.py" << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="{SERVICE_NAME} API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "{SERVICE_NAME} is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
EOF
}

# Apply structure to all domain services
create_domain_structure "security-service"
create_domain_structure "productivity-service"
create_domain_structure "mtg-service"
create_domain_structure "infrastructure-service"
```

### 3. Set Up n8n Workflow Service

```bash
# Create specialized n8n service structure
mkdir -p "apps/n8n-workflow-service/src/workflows"
mkdir -p "apps/n8n-workflow-service/src/ai"
mkdir -p "apps/n8n-workflow-service/src/orchestration"
mkdir -p "apps/n8n-workflow-service/src/api"

# Create AI enhancement modules
cat > "apps/n8n-workflow-service/src/ai/pattern_detection.py" << 'EOF'
"""
Pattern detection for adaptive workflow creation
Monitors user requests and identifies workflow opportunities
"""
from typing import List, Dict
import asyncio
from datetime import datetime, timedelta

class WorkflowPatternDetector:
    def __init__(self):
        self.request_history = []
        self.pattern_threshold = 3  # Create workflow after 3 similar requests
        self.time_window = timedelta(days=7)  # Within 7 days
    
    async def analyze_request(self, user_request: str) -> Dict:
        """Analyze user request for workflow generation opportunity"""
        # Add to history
        self.request_history.append({
            'request': user_request,
            'timestamp': datetime.now(),
            'workflow_exists': await self.check_existing_workflow(user_request)
        })
        
        # Check for patterns
        similar_requests = await self.find_similar_requests(user_request)
        
        if len(similar_requests) >= self.pattern_threshold:
            return {
                'should_create_workflow': True,
                'pattern_requests': similar_requests,
                'confidence': len(similar_requests) / self.pattern_threshold
            }
        
        return {'should_create_workflow': False}
    
    async def check_existing_workflow(self, request: str) -> bool:
        """Check if workflow already exists for this request pattern"""
        # Implementation to check n8n workflow database
        return False
    
    async def find_similar_requests(self, request: str) -> List[Dict]:
        """Find similar requests within time window"""
        cutoff_time = datetime.now() - self.time_window
        return [
            req for req in self.request_history 
            if req['timestamp'] > cutoff_time and not req['workflow_exists']
        ]
EOF

cat > "apps/n8n-workflow-service/src/ai/workflow_generator.py" << 'EOF'
"""
AI-powered workflow generation
Creates n8n workflows based on detected patterns
"""
from typing import Dict, List
import json

class WorkflowGenerator:
    def __init__(self):
        self.domain_services = {
            'security': 'http://security-service:8000',
            'productivity': 'http://productivity-service:8000',
            'mtg': 'http://mtg-service:8000',
            'infrastructure': 'http://infrastructure-service:8000'
        }
    
    async def generate_workflow(self, pattern_data: Dict) -> Dict:
        """Generate n8n workflow from pattern analysis"""
        workflow_definition = {
            "name": f"Auto-generated workflow {datetime.now().isoformat()}",
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {}
        }
        
        # Analyze pattern to determine required tools/domains
        required_domains = await self.analyze_domains_needed(pattern_data)
        
        # Generate nodes for each domain
        for domain in required_domains:
            node = await self.create_domain_node(domain, pattern_data)
            workflow_definition["nodes"].append(node)
        
        return workflow_definition
    
    async def analyze_domains_needed(self, pattern_data: Dict) -> List[str]:
        """Determine which domain services are needed"""
        # Simple keyword-based analysis (can be enhanced with LLM)
        keywords = {
            'security': ['malware', 'threat', 'scan', 'vulnerability', 'attack'],
            'productivity': ['task', 'schedule', 'budget', 'recipe', 'incident'],
            'mtg': ['deck', 'combo', 'commander', 'card'],
            'infrastructure': ['server', 'container', 'deploy', 'monitor']
        }
        
        domains_needed = []
        request_text = ' '.join([req['request'].lower() for req in pattern_data['pattern_requests']])
        
        for domain, domain_keywords in keywords.items():
            if any(keyword in request_text for keyword in domain_keywords):
                domains_needed.append(domain)
        
        return domains_needed
    
    async def create_domain_node(self, domain: str, pattern_data: Dict) -> Dict:
        """Create n8n node for specific domain service"""
        return {
            "parameters": {
                "url": self.domain_services[domain],
                "authentication": "genericCredentialType",
                "options": {}
            },
            "name": f"{domain.title()} Service",
            "type": "n8n-nodes-base.httpRequest",
            "position": [250, 300],
            "credentials": {}
        }
EOF
```

### 4. Migrate Tools from features/ to Domain Services

```bash
# Create migration script
cat > "migrate_tools.sh" << 'EOF'
#!/bin/bash

echo "Migrating 37 tools from features/ to domain services..."

# Security Domain (13 tools)
echo "Migrating Security Domain tools..."
mv features/misp/ apps/security-service/src/domains/misp/
mv features/HELK/ apps/security-service/src/domains/helk/
mv features/yara-x/ apps/security-service/src/domains/yara/
mv features/CyberChef/ apps/security-service/src/domains/cyberchef/
mv features/Nemesis/ apps/security-service/src/domains/nemesis/
mv features/Ghostwriter/ apps/security-service/src/domains/ghostwriter/
mv features/maltrail/ apps/security-service/src/domains/maltrail/
mv features/securityonion/ apps/security-service/src/domains/securityonion/
mv features/rita/ apps/security-service/src/domains/rita/
mv features/blackarch/ apps/security-service/src/domains/blackarch/
mv features/onex/ apps/security-service/src/domains/onex/
mv features/Brute-Ratel-C4-Community-Kit/ apps/security-service/src/domains/brute-ratel/
mv features/apiscout/ apps/security-service/src/domains/apiscout/

# Productivity Domain (8 tools)
echo "Migrating Productivity Domain tools..."
mv features/actual/ apps/productivity-service/src/domains/actual-budget/
mv features/mealie/ apps/productivity-service/src/domains/mealie/
mv features/dispatch/ apps/productivity-service/src/domains/dispatch/
mv features/firecrawl/ apps/productivity-service/src/domains/firecrawl/
mv features/goose/ apps/productivity-service/src/domains/goose/
mv features/inspector/ apps/productivity-service/src/domains/inspector/
mv features/it-tools/ apps/productivity-service/src/domains/it-tools/

# MTG Domain (4 tools)
echo "Migrating MTG Domain tools..."
mv features/commander-spellbook-backend/ apps/mtg-service/src/domains/commander-spellbook-backend/
mv features/commander-spellbook-site/ apps/mtg-service/src/domains/commander-spellbook-site/ 
mv features/mtg-commander-map/ apps/mtg-service/src/domains/mtg-commander-map/
mv features/mtg-scripting-toolkit/ apps/mtg-service/src/domains/mtg-scripting-toolkit/

# Infrastructure Domain (12 tools)
echo "Migrating Infrastructure Domain tools..."
mv features/KasmVNC/ apps/infrastructure-service/src/domains/kasmvnc/
mv features/kong/ apps/infrastructure-service/src/domains/kong/
mv features/lscript/ apps/infrastructure-service/src/domains/lscript/
mv features/software-forensic-kit/ apps/infrastructure-service/src/domains/software-forensic-kit/
mv features/meterpreter/ apps/infrastructure-service/src/domains/meterpreter/
mv features/hexstrike-ai/ apps/infrastructure-service/src/domains/hexstrike-ai/

# MCP Servers to Infrastructure
echo "Migrating MCP servers..."
mkdir -p apps/infrastructure-service/src/domains/mcp-servers/
mv features/chroma-mcp/ apps/infrastructure-service/src/domains/mcp-servers/chroma-mcp/
mv features/FileScopeMCP/ apps/infrastructure-service/src/domains/mcp-servers/filescope-mcp/
mv features/firecrawl-mcp-server/ apps/infrastructure-service/src/domains/mcp-servers/firecrawl-mcp/
mv features/MalwareBazaar_MCP/ apps/infrastructure-service/src/domains/mcp-servers/malwarebazaar-mcp/
mv features/mcp-virustotal/ apps/infrastructure-service/src/domains/mcp-servers/mcp-virustotal/

# Move n8n to central workflow service
echo "Migrating n8n to central workflow service..."
mv features/n8n/ apps/n8n-workflow-service/src/workflows/n8n/
mv features/n8n-mcp-server/ apps/n8n-workflow-service/src/ai/n8n-mcp/
mv features/securityonion-n8n-workflows/ apps/n8n-workflow-service/src/workflows/security-workflows/

echo "Migration complete! Checking features/ directory..."
ls -la features/

if [ -z "$(ls -A features/)" ]; then
   echo "✅ SUCCESS: features/ directory is empty - all 37 tools migrated!"
else
   echo "⚠️  WARNING: features/ directory still contains:"
   ls -la features/
fi
EOF

chmod +x migrate_tools.sh
```

### 5. Update NX Configuration

```bash
# Update nx.json to include new services
cat > update_nx_config.py << 'EOF'
import json

# Read current nx.json
with open('nx.json', 'r') as f:
    nx_config = json.load(f)

# Add new projects
new_projects = [
    "n8n-workflow-service",
    "security-service", 
    "productivity-service",
    "mtg-service",
    "infrastructure-service"
]

for project in new_projects:
    if 'projects' not in nx_config:
        nx_config['projects'] = {}
    
    nx_config['projects'][project] = f"apps/{project}"

# Write updated config
with open('nx.json', 'w') as f:
    json.dump(nx_config, f, indent=2)

print("✅ Updated nx.json with new domain services")
EOF

python update_nx_config.py
```

### 6. Create Docker Configuration

```bash
# Update docker-compose.yml for hybrid architecture
cat > infrastructure/docker/docker-compose.yml << 'EOF'
version: '3.8'

services:
  # Central Orchestration
  n8n-workflow-service:
    build: 
      context: ../../
      dockerfile: ./apps/n8n-workflow-service/Dockerfile
    ports:
      - "8010:8000"
    environment:
      - NODE_ENV=development
    volumes:
      - ../../apps/n8n-workflow-service:/app
    depends_on:
      - postgres
      - redis

  # Domain Services  
  security-service:
    build:
      context: ../../
      dockerfile: ./apps/security-service/Dockerfile
    ports:
      - "8011:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/security_db
    depends_on:
      - postgres

  productivity-service:
    build:
      context: ../../
      dockerfile: ./apps/productivity-service/Dockerfile
    ports:
      - "8012:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/productivity_db
    depends_on:
      - postgres

  mtg-service:
    build:
      context: ../../
      dockerfile: ./apps/mtg-service/Dockerfile
    ports:
      - "8013:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/mtg_db
    depends_on:
      - postgres

  infrastructure-service:
    build:
      context: ../../
      dockerfile: ./apps/infrastructure-service/Dockerfile
    ports:
      - "8014:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/infrastructure_db
    depends_on:
      - postgres

  # Frontend
  jane-ui:
    build:
      context: ../../
      dockerfile: ./apps/jane-ui/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_N8N_SERVICE_URL=http://n8n-workflow-service:8000
      - NEXT_PUBLIC_SECURITY_SERVICE_URL=http://security-service:8000
      - NEXT_PUBLIC_PRODUCTIVITY_SERVICE_URL=http://productivity-service:8000
      - NEXT_PUBLIC_MTG_SERVICE_URL=http://mtg-service:8000
      - NEXT_PUBLIC_INFRASTRUCTURE_SERVICE_URL=http://infrastructure-service:8000

  # AI Servers
  cyber-llm-server:
    build:
      context: ../../
      dockerfile: ./apps/cyber-llm-server/Dockerfile
    ports:
      - "8001:8000"
    environment:
      - SECURITY_SERVICE_URL=http://security-service:8000

  mtg-llm-server:
    build:
      context: ../../
      dockerfile: ./apps/mtg-llm-server/Dockerfile
    ports:
      - "8002:8000"
    environment:
      - MTG_SERVICE_URL=http://mtg-service:8000

  infrastructure-llm-server:
    build:
      context: ../../
      dockerfile: ./apps/infrastructure-llm-server/Dockerfile
    ports:
      - "8003:8000"
    environment:
      - INFRASTRUCTURE_SERVICE_URL=http://infrastructure-service:8000

  # Infrastructure
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: jane_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
EOF
```

### 7. Cleanup and Validation

```bash
# Remove old jane-orchestrator (after migration is complete)
echo "After successful migration, remove jane-orchestrator:"
echo "rm -rf apps/jane-orchestrator/"

# Validation script
cat > validate_migration.sh << 'EOF'
#!/bin/bash

echo "🔍 Validating hybrid architecture migration..."

# Check if all services exist
services=("n8n-workflow-service" "security-service" "productivity-service" "mtg-service" "infrastructure-service")
for service in "${services[@]}"; do
    if [ -d "apps/$service" ]; then
        echo "✅ $service directory exists"
    else
        echo "❌ $service directory missing"
    fi
done

# Check if features/ is empty
if [ -z "$(ls -A features/)" ]; then
   echo "✅ features/ directory is empty - migration complete!"
else
   echo "⚠️  features/ directory still contains files:"
   ls -la features/
fi

# Check if NX can build all services
echo "🔨 Testing NX builds..."
npx nx run-many --target=build --all --parallel=3

echo "🏁 Migration validation complete!"
EOF

chmod +x validate_migration.sh
```

## Execution Order

Run these commands in order:

```bash
# 1. Create services
npx nx generate @nx/node:application n8n-workflow-service --framework=express
npx nx generate @nx/node:application security-service --framework=express
npx nx generate @nx/node:application productivity-service --framework=express  
npx nx generate @nx/node:application mtg-service --framework=express
npx nx generate @nx/node:application infrastructure-service --framework=express

# 2. Set up structures (run the create_domain_structure function)

# 3. Migrate tools
./migrate_tools.sh

# 4. Update configurations
python update_nx_config.py

# 5. Validate migration
./validate_migration.sh

# 6. Test with Docker
cd infrastructure/docker && docker-compose up --build
```

## Success Criteria

✅ **5 new services created** in apps/ directory
✅ **features/ directory empty** (all 37 tools migrated)  
✅ **All services build successfully** with NX
✅ **Docker Compose runs all services** without errors
✅ **n8n workflow service** operational with AI enhancement
✅ **API communication** working between services

This restructure transforms your skeleton into the hybrid domain-based architecture optimized for your AI-first workflow patterns with n8n orchestration.