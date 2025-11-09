---
description: "DDD-based asset relocation for Goose AI agent developer tool"
parent_task: "../tasks.md#TXXX"
parent_phase: "Phase X: Productivity Migrations"
return_to: "../tasks.md#TXXX"
domain: "productivity"
target_service: "apps/productivity-service/src/"
legacy_path: "features/goose"
estimated_hours: 280
---

# Tasks: [MIGRATION: Goose - AI Developer Agent]

**⬆️ PARENT TASK**: [`tasks.md#TXXX`](../tasks.md#TXXX)  
**⬇️ RETURN TO**: [`tasks.md#TXXX`](../tasks.md#TXXX)

---

## Handoff Context

**Called From**: `tasks.md` Phase X, Task TXXX  
**Entry Condition**: Productivity service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark TXXX complete in parent `tasks.md`, proceed to next task

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/productivity-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/goose/` accessible (Rust toolchain installed)
- [ ] Project analysis report completed and validated (goose-analysis.md)

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Goose Domain Architecture Overview

**Platform Purpose**: Local AI developer agent - automates engineering tasks through LLM-powered conversation with tool integration

**Identified Bounded Contexts (DDD)**:

1. **Conversation Management**: Message handling, conversation state, context management
2. **Agent Orchestration**: LLM interaction, tool execution, workflow coordination
3. **Extension/Tool Management (MCP)**: Dynamic tool discovery, permission management, external integration
4. **Provider Abstraction**: Multi-LLM provider support (OpenAI, Anthropic, Google, etc.)
5. **Recipe/Automation Engine**: Task automation, workflow orchestration, sub-recipe management
6. **Security & Permissions**: Tool execution authorization, permission inspection

**Cross-Cutting Concerns**:

- Asynchronous execution (Tokio runtime)
- Model Context Protocol (MCP) integration
- OAuth 2.0 authentication for external services
- Real-time streaming (SSE for web UI)
- Performance monitoring and benchmarking

**Legacy Structure** (Rust Workspace):

```text
features/goose/crates/
├── goose/                 # Core agent library (all bounded contexts)
│   ├── agents/           # Agent orchestration
│   ├── conversation/     # Conversation management
│   ├── providers/        # LLM provider abstraction
│   ├── recipe/           # Recipe engine
│   ├── permission/       # Security & permissions
│   └── mcp_utils/        # MCP integration
├── goose-cli/            # CLI interface
├── goose-server/         # HTTP server (web UI backend)
├── goose-mcp/            # MCP server implementation
├── goose-bench/          # Benchmarking tools
└── goose-test/           # Test utilities
```

**Target Structure** (Modular Monolith with Python/FastAPI):

```text
apps/productivity-service/src/
├── domains/
│   ├── conversation/          # Conversation BC (port from Rust)
│   ├── agent_orchestration/   # Agent BC (port from Rust)
│   ├── tool_management/       # Extension/MCP BC (port from Rust)
│   ├── llm_providers/         # Provider abstraction BC
│   ├── automation/            # Recipe/workflow BC
│   └── shared/                # Cross-domain types
├── api/                       # FastAPI endpoints
├── services/                  # Domain services
├── integrations/              # MCP client, OAuth handlers
└── data/                      # Data models
```

**Migration Strategy**: Port Rust business logic to Python while preserving algorithms and maintaining MCP protocol compatibility

**Critical Note**: This is a **Rust-to-Python** migration - requires careful algorithm preservation and performance validation

**Critical Note**: This is a **Rust-to-Python** migration - requires careful algorithm preservation and performance validation

---

## Phase 1: Foundation & Analysis Validation

**Purpose**: Validate analysis, setup Rust test environment, establish Python foundation

- [ ] T001 [Analysis: Section.1] Validate project analysis completeness for all 6 bounded contexts
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Rust Edition 2021, Tokio, rmcp, Axum
- [ ] T003 [Ground Truth] Setup Rust legacy test environment: Cargo workspace with all crates
- [ ] T004 [Ground Truth] Run Rust test suite: Validate all tests passing in legacy system
- [ ] T005 [Analysis: Section.8.1] Performance baseline: Measure Rust agent response times, tool execution latency
- [ ] T006 [P] Create Python domain directory structure in `apps/productivity-service/src/domains/`
- [ ] T007 [P] Initialize Python async infrastructure: FastAPI, asyncio, aiohttp
- [ ] T008 [Analysis: Section.7.1] Setup pytest infrastructure with async support

**Checkpoint**: Foundation ready with validated Rust baseline and Python infrastructure

---

## Phase 2: Core Data Models & Shared Kernel

**Purpose**: Port fundamental data structures from Rust to Python with preservation of behavior

### Phase 2a: Message and Conversation Models

- [ ] T009 [Analysis: Section.2.1] [Logic: goose/src/conversation/message.rs::Message] Port Message model to Python (Pydantic)
- [ ] T010 [Analysis: Section.2.1] [Logic: goose/src/conversation/message.rs::Role] Port Role enum (User, Assistant, System, Tool)
- [ ] T011 [Analysis: Section.2.1] [Logic: goose/src/conversation/message.rs::MessageContent] Port MessageContent variants (text, image, tool_call)
- [ ] T012 [P] [Logic: goose/src/conversation/message.rs::unicode_tag_sanitizer] Port Unicode tag sanitization logic
- [ ] T013 [Analysis: Section.2.1] [Logic: goose/src/conversation/mod.rs::Conversation] Port Conversation model with message ordering
- [ ] T014 [Ground Truth] Message model tests: Serialization, validation, sanitization
- [ ] T015 [Ground Truth] Conversation tests: Message appending, deduplication, state management

### Phase 2b: Agent Configuration and State

- [ ] T016 [Analysis: Section.2.1] [Logic: goose/src/config/mod.rs] Port configuration models (AgentConfig, ProviderConfig)
- [ ] T017 [P] [Logic: goose/src/session/mod.rs::Session] Port Session model for agent state persistence
- [ ] T018 [P] Database schema: Create tables for conversations, messages, sessions
- [ ] T019 [Ground Truth] Configuration tests: Validation, loading, environment variable handling

**Checkpoint**: Core data models ported with validated behavior parity

---

## Phase 3: Domain 1 - Conversation Management BC 🎯 MVP

**Business Value**: Foundation for all AI agent interactions

**Analysis Reference**: Section.2.1 (Conversation/Message models), Section.4.1 (Conversation management algorithm)

### Phase 3a: Conversation State Management

- [ ] T020 [Analysis: Section.4.1] [Logic: goose/src/conversation/mod.rs::Conversation::push] Port message appending with deduplication
- [ ] T021 [Analysis: Section.4.1] [Logic: goose/src/conversation/mod.rs::Conversation::pop_last_message] Port message removal logic
- [ ] T022 [P] [Logic: goose/src/conversation/mod.rs::Conversation::add_user_message] Port user message handling
- [ ] T023 [P] [Logic: goose/src/conversation/mod.rs::Conversation::add_assistant_message] Port assistant message handling
- [ ] T024 [Analysis: Section.2.2] Message repair logic: Handle malformed tool responses
- [ ] T025 [Ground Truth] Conversation management tests: All operations match Rust behavior

### Phase 3b: Context Management

- [ ] T026 [Analysis: Section.4.1] [Logic: goose/src/context_mgmt/mod.rs] Port conversation context window management
- [ ] T027 [Logic: goose/src/context_mgmt/mod.rs::trim_context] Port context trimming algorithm (token limits)
- [ ] T028 [Analysis: Section.4.2] Token counting: Port token calculation for context management
- [ ] T029 [Ground Truth] Context management tests: Token limits, trimming behavior

### Phase 3c: Conversation API

- [ ] T030 [Analysis: Section.3.2] FastAPI endpoints: Conversation CRUD operations
- [ ] T031 [P] SSE streaming: Real-time conversation updates
- [ ] T032 [Analysis: Section.3.2] WebSocket support: Alternative real-time transport
- [ ] T033 [Ground Truth] API tests: Conversation endpoints, streaming, WebSocket

**Checkpoint**: Conversation management operational with real-time streaming

---

## Phase 4: Domain 2 - LLM Provider Abstraction BC

**Business Value**: Multi-provider LLM support prevents vendor lock-in

**Analysis Reference**: Section.4.1 (Multi-provider management), Section.5.1 (LLM provider integrations)

### Phase 4a: Provider Interface

- [ ] T034 [Analysis: Section.4.1] [Logic: goose/src/providers/base.rs::Provider trait] Port Provider trait to Python ABC
- [ ] T035 [Analysis: Section.4.1] [Logic: goose/src/providers/base.rs::ProviderUsage] Port usage tracking (tokens, cost)
- [ ] T036 [P] [Logic: goose/src/providers/errors.rs] Port provider error handling
- [ ] T037 [Ground Truth] Provider interface tests: Contract validation

### Phase 4b: OpenAI Provider

- [ ] T038 [Analysis: Section.5.1] [Logic: goose/src/providers/openai.rs::OpenAiProvider] Port OpenAI provider implementation
- [ ] T039 [Analysis: Section.5.1] [Logic: goose/src/providers/openai.rs::complete] Port completion API with streaming
- [ ] T040 [P] [Logic: goose/src/providers/openai.rs::tool_calling] Port OpenAI tool/function calling
- [ ] T041 [Ground Truth] OpenAI provider tests: Completions, streaming, tool calls

### Phase 4c: Anthropic Provider

- [ ] T042 [Analysis: Section.5.1] [Logic: goose/src/providers/anthropic.rs::AnthropicProvider] Port Anthropic Claude provider
- [ ] T043 [Analysis: Section.5.1] [Logic: goose/src/providers/anthropic.rs::complete] Port Claude completion with streaming
- [ ] T044 [P] [Logic: goose/src/providers/anthropic.rs::tool_use] Port Anthropic tool use protocol
- [ ] T045 [Ground Truth] Anthropic provider tests: Claude-specific features

### Phase 4d: Additional Providers

- [ ] T046 [P] [Analysis: Section.5.1] [Logic: goose/src/providers/google.rs] Port Google Gemini provider
- [ ] T047 [P] [Analysis: Section.5.1] [Logic: goose/src/providers/databricks.rs] Port Databricks provider
- [ ] T048 [P] Port remaining providers: Azure, Groq, Ollama, etc. (20+ total)
- [ ] T049 [Analysis: Section.4.1] [Logic: goose/src/providers/factory.rs] Port provider factory and selection logic
- [ ] T050 [Ground Truth] Multi-provider tests: Failover, capability-based selection

**Checkpoint**: LLM provider abstraction operational with 20+ providers

---

## Phase 5: Domain 3 - Extension/Tool Management BC (MCP) [CRITICAL]

**Business Value**: Core differentiator - dynamic tool integration via Model Context Protocol

**Analysis Reference**: Section.4.1 (Extension discovery), Section.5.2 (MCP integration)

### Phase 5a: MCP Client Integration

- [ ] T051 [Analysis: Section.5.2] [Logic: goose/src/agents/extension_manager.rs] Port ExtensionManager to Python
- [ ] T052 [Analysis: Section.5.2] Python MCP client library selection/integration (replace rmcp crate)
- [ ] T053 [Analysis: Section.4.1] [Logic: goose/src/agents/extension_manager.rs::initialize_extensions] Port extension initialization
- [ ] T054 [Analysis: Section.4.1] [Logic: goose/src/agents/extension_manager.rs::discover_tools] Port tool discovery via MCP
- [ ] T055 [Analysis: Section.4.1] [Logic: goose/src/agents/extension_manager.rs::discover_resources] Port resource discovery
- [ ] T056 [Ground Truth] MCP integration tests: Extension startup, tool discovery

### Phase 5b: Tool Execution Framework

- [ ] T057 [Analysis: Section.4.1] [Logic: goose/src/agents/extension_manager.rs::call_tool] Port tool execution with async handling
- [ ] T058 [Analysis: Section.4.2] [Logic: goose/src/tool_inspection.rs] Port tool call inspection and validation
- [ ] T059 [P] [Logic: goose/src/tool_monitor.rs] Port tool execution monitoring
- [ ] T060 [Analysis: Section.4.1] Error handling: Tool failures, timeouts, retries
- [ ] T061 [Ground Truth] Tool execution tests: Success, failures, edge cases

### Phase 5c: Permission System

- [ ] T062 [Analysis: Section.4.1] [Logic: goose/src/permission/inspector.rs::PermissionInspector] Port permission inspection
- [ ] T063 [Analysis: Section.4.1] [Logic: goose/src/permission/judge.rs] Port permission judgment logic
- [ ] T064 [P] [Logic: goose/src/permission/mod.rs::check_tool_permission] Port tool permission checking
- [ ] T065 [Analysis: Section.3.1] User confirmation flow: Interactive permission prompts
- [ ] T066 [Ground Truth] Permission tests: Approval workflows, dangerous operation detection

### Phase 5d: OAuth Integration for Tools

- [ ] T067 [Analysis: Section.5.3] [Logic: goose/src/oauth/mod.rs] Port OAuth 2.0 flow for external services
- [ ] T068 [Analysis: Section.5.3] [Logic: goose/src/oauth/callback.rs] Port OAuth callback handling
- [ ] T069 [P] [Logic: goose/src/oauth/token_storage.rs] Port secure token storage
- [ ] T070 [Ground Truth] OAuth tests: Authorization flows, token refresh

**Checkpoint**: MCP integration operational with tool execution and permissions

---

## Phase 6: Domain 4 - Agent Orchestration BC

**Business Value**: Core AI agent logic - orchestrates LLM, tools, and workflows

**Analysis Reference**: Section.4.1 (Agent algorithms), Section.4.3 (Agent lifecycle workflow)

### Phase 6a: Core Agent Logic

- [ ] T071 [Analysis: Section.4.1] [Logic: goose/src/agents/agent.rs::Agent] Port Agent struct/class
- [ ] T072 [Analysis: Section.4.1] [Logic: goose/src/agents/agent.rs::Agent::reply] Port main agent reply loop
- [ ] T073 [Analysis: Section.4.3] [Logic: goose/src/agents/agent.rs::process_turn] Port conversation turn processing
- [ ] T074 [Analysis: Section.4.1] [Logic: goose/src/agents/agent.rs::handle_tool_calls] Port tool call orchestration
- [ ] T075 [Analysis: Section.4.1] Streaming response: Port SSE streaming for real-time updates
- [ ] T076 [Ground Truth] Agent orchestration tests: Complete conversation cycles

### Phase 6b: Execution Engine

- [ ] T077 [Analysis: Section.4.1] [Logic: goose/src/execution/mod.rs] Port execution context management
- [ ] T078 [P] [Logic: goose/src/execution/executor.rs] Port async execution coordinator
- [ ] T079 [Analysis: Section.4.2] Backpressure handling: Manage concurrent tool executions
- [ ] T080 [Ground Truth] Execution tests: Concurrency, backpressure, cancellation

### Phase 6c: Agent Configuration

- [ ] T081 [Analysis: Section.4.2] [Logic: goose/src/agents/capabilities.rs] Port agent capability management
- [ ] T082 [P] [Logic: goose/src/agents/system_prompt.rs] Port system prompt generation
- [ ] T083 [P] [Logic: goose/src/prompt_template.rs] Port prompt templating system
- [ ] T084 [Ground Truth] Configuration tests: Capability selection, prompt generation

**Checkpoint**: Agent orchestration operational with tool integration

---

## Phase 7: Domain 5 - Recipe/Automation Engine BC

**Business Value**: Automated workflows and reproducible multi-step tasks

**Analysis Reference**: Section.4.1 (Recipe execution), Section.2.1 (Recipe model)

### Phase 7a: Recipe Configuration

- [ ] T085 [Analysis: Section.2.1] [Logic: goose/src/recipe/mod.rs::Recipe] Port Recipe model (YAML/JSON parsing)
- [ ] T086 [Analysis: Section.2.1] [Logic: goose/src/recipe/mod.rs::SubRecipe] Port SubRecipe for nested workflows
- [ ] T087 [P] [Logic: goose/src/recipe/validation.rs] Port recipe validation logic
- [ ] T088 [Ground Truth] Recipe parsing tests: YAML validation, schema compliance

### Phase 7b: Recipe Execution

- [ ] T089 [Analysis: Section.4.1] [Logic: goose/src/recipe/executor.rs] Port recipe execution engine
- [ ] T090 [Analysis: Section.4.1] [Logic: goose/src/agents/sub_recipe_manager.rs] Port sub-recipe orchestration
- [ ] T091 [P] [Logic: goose/src/recipe/context.rs] Port recipe context and variable substitution
- [ ] T092 [Analysis: Section.4.1] Dependency resolution: Port recipe dependency graph execution
- [ ] T093 [Ground Truth] Recipe execution tests: Simple and complex workflows

### Phase 7c: Task Management

- [ ] T094 [Analysis: Section.4.1] [Logic: goose/src/agents/tasks_manager.rs] Port task queue management
- [ ] T095 [P] Task scheduling: Port async task scheduling logic
- [ ] T096 [Ground Truth] Task management tests: Scheduling, dependencies, failures

**Checkpoint**: Recipe engine operational with automated workflows

---

## Phase 8: Cross-Domain Integration

**Purpose**: Wire domains together for complete agent functionality

### Phase 8a: Agent-to-Conversation Integration

- [ ] T097 [Analysis: Section.2.2] Agent conversation lifecycle: Wire agent to conversation management
- [ ] T098 [Logic: goose/src/agents/agent.rs::conversation_loop] Port conversation loop integration
- [ ] T099 [Ground Truth] Integration tests: Complete agent conversations

### Phase 8b: Agent-to-Tool Integration

- [ ] T100 [Analysis: Section.2.2] Tool call flow: Agent → ExtensionManager → MCP → Tool execution
- [ ] T101 [Logic: goose/src/agents/agent.rs::execute_tools] Port tool execution integration
- [ ] T102 [Ground Truth] Integration tests: Agent tool usage workflows

### Phase 8c: Recipe-to-Agent Integration

- [ ] T103 [Analysis: Section.2.2] Recipe execution: Wire recipes to agent orchestration
- [ ] T104 [Logic: goose/src/recipe/agent_integration.rs] Port recipe-agent integration
- [ ] T105 [Ground Truth] Integration tests: Recipe-driven agent workflows

**Checkpoint**: Cross-domain workflows operational

---

## Phase 9: CLI and Server Interfaces

**Purpose**: Port user interfaces (CLI and HTTP server)

### Phase 9a: CLI Interface

- [ ] T106 [Analysis: Section.6.1] [Logic: goose-cli/src/main.rs] Port CLI application structure
- [ ] T107 [Analysis: Section.6.1] [Logic: goose-cli/src/commands/mod.rs] Port command handlers (session, run, etc.)
- [ ] T108 [P] [Logic: goose-cli/src/profile.rs] Port profile management
- [ ] T109 [P] [Logic: goose-cli/src/history.rs] Port command history
- [ ] T110 [Analysis: Section.6.2] Interactive REPL: Port conversational CLI loop
- [ ] T111 [Ground Truth] CLI tests: Command execution, interactive mode

### Phase 9b: HTTP Server (Web UI Backend)

- [ ] T112 [Analysis: Section.3.2] [Logic: goose-server/src/server.rs] Port Axum server to FastAPI
- [ ] T113 [Analysis: Section.3.2] [Logic: goose-server/src/routes/mod.rs] Port HTTP routes
- [ ] T114 [P] [Logic: goose-server/src/routes/sessions.rs] Port session endpoints
- [ ] T115 [P] [Logic: goose-server/src/routes/messages.rs] Port message endpoints
- [ ] T116 [Analysis: Section.3.3] SSE streaming: Port server-sent events for real-time updates
- [ ] T117 [Analysis: Section.3.1] Authentication: Port X-Secret-Key authentication
- [ ] T118 [Ground Truth] Server tests: HTTP endpoints, SSE streams

### Phase 9c: Desktop UI Integration

- [ ] T119 [Analysis: Section.6.1] Desktop app backend: Ensure HTTP server compatible with desktop UI
- [ ] T120 [P] Desktop launch integration: Port desktop app spawning logic
- [ ] T121 [Ground Truth] Desktop integration tests: UI-backend communication

**Checkpoint**: CLI and server interfaces operational

---

## Phase 10: MCP Server Implementation

**Purpose**: Expose Goose itself as an MCP server for integration with other tools

### Phase 10a: MCP Server Core

- [ ] T122 [Analysis: Section.5.2] [Logic: goose-mcp/src/main.rs] Port goose-mcp server application
- [ ] T123 [Analysis: Section.5.2] [Logic: goose-mcp/src/handlers.rs] Port MCP request handlers
- [ ] T124 [P] Tool definitions: Expose Goose capabilities as MCP tools
- [ ] T125 [Ground Truth] MCP server tests: Protocol compliance, tool invocation

### Phase 10b: MCP Server Tools

- [ ] T126 [Analysis: Section.5.2] [Logic: goose-mcp/src/tools/session.rs] Port session management tools
- [ ] T127 [P] [Logic: goose-mcp/src/tools/ask.rs] Port ask/query tools
- [ ] T128 [Ground Truth] MCP tool tests: All exposed tools functional

**Checkpoint**: MCP server operational

---

## Phase 11: Performance Optimization & Async Runtime

**Purpose**: Optimize Python async performance to approach Rust baselines

### Phase 11a: Async Infrastructure Optimization

- [ ] T129 [Analysis: Section.8.1] Async runtime optimization: Ensure efficient asyncio usage
- [ ] T130 [Analysis: Section.8.1] Connection pooling: HTTP clients, MCP connections
- [ ] T131 [Analysis: Section.8.2] Memory management: Minimize allocations in hot paths
- [ ] T132 [Ground Truth] Performance tests: Compare Python vs Rust response times

### Phase 11b: Caching Strategy

- [ ] T133 [Analysis: Section.2.3] [Logic: goose/src/providers/cache.rs] Port LRU cache for LLM responses
- [ ] T134 [P] Cache key generation: Port cache key hashing logic
- [ ] T135 [Ground Truth] Caching tests: Hit rates, invalidation

### Phase 11c: Benchmarking

- [ ] T136 [Analysis: Section.7.1] [Logic: goose-bench/src/] Port benchmarking suite to Python
- [ ] T137 [Analysis: Section.8.1] Performance baselines: Validate Python implementation meets targets
- [ ] T138 [Ground Truth] Benchmark comparison: Python vs Rust performance analysis

**Checkpoint**: Performance optimized and validated

---

## Phase 12: Security Hardening

**Purpose**: Ensure security best practices for AI agent system

### Phase 12a: Tool Execution Security

- [ ] T139 [Analysis: Section.9.1] [Logic: goose/src/security/mod.rs] Port security validation logic
- [ ] T140 [Analysis: Section.9.1] Sandboxing: Tool execution isolation (if applicable)
- [ ] T141 [P] Input validation: Sanitize all user inputs and tool outputs
- [ ] T142 [Ground Truth] Security tests: Injection attempts, privilege escalation

### Phase 12b: Secret Management

- [ ] T143 [Analysis: Section.9.1] API key storage: Secure credential management
- [ ] T144 [P] OAuth token security: Encrypted storage, secure refresh
- [ ] T145 [Ground Truth] Secret management tests: Storage, retrieval, rotation

### Phase 12c: Audit Logging

- [ ] T146 [Analysis: Section.9.1] [Logic: goose/src/logging.rs] Port audit logging for sensitive operations
- [ ] T147 [P] Tool execution logs: Track all tool invocations with permissions
- [ ] T148 [Ground Truth] Audit log tests: Completeness, tamper resistance

**Checkpoint**: Security hardened and validated

---

## Phase 13: Testing & Quality Assurance

**Purpose**: Comprehensive testing for production readiness

### Phase 13a: Test Coverage

- [ ] T149 [Analysis: Section.7.1] Achieve 80%+ unit test coverage across all domains
- [ ] T150 [Analysis: Section.7.2] Port critical Rust tests to Python equivalents
- [ ] T151 [Analysis: Section.7.3] Integration test suite: All bounded context interactions
- [ ] T152 [Ground Truth] Test parity validation: Python tests match Rust test coverage

### Phase 13b: End-to-End Testing

- [ ] T153 [Analysis: Section.7.4] E2E test suite: Complete agent workflows
- [ ] T154 [Analysis: Section.7.4] Recipe execution E2E: Complex automation scenarios
- [ ] T155 [Analysis: Section.7.4] Multi-provider E2E: Test all LLM providers
- [ ] T156 [Ground Truth] E2E validation: All user workflows functional

### Phase 13c: MCP Compatibility Testing

- [ ] T157 [Analysis: Section.5.2] MCP protocol compliance: Validate against spec
- [ ] T158 [P] Cross-tool compatibility: Test with common MCP tools
- [ ] T159 [Ground Truth] MCP integration tests: Tool discovery, execution, errors

**Checkpoint**: Testing complete with validated parity

---

## Phase 14: Documentation & Knowledge Transfer

**Purpose**: Capture domain knowledge and migration details

### Phase 14a: Domain Documentation

- [ ] T160 [Analysis: Section.11.1] Conversation Management domain: APIs, patterns, edge cases
- [ ] T161 [Analysis: Section.11.1] Agent Orchestration domain: Workflow, algorithms, optimization
- [ ] T162 [Analysis: Section.11.1] Tool Management domain: MCP integration, permissions, security
- [ ] T163 [Analysis: Section.11.1] Provider Abstraction domain: Multi-provider patterns
- [ ] T164 [Analysis: Section.11.1] Recipe Engine domain: YAML syntax, execution model
- [ ] T165 [P] API documentation: All FastAPI endpoints, SSE streams

### Phase 14b: Migration Documentation

- [ ] T166 [Analysis: Section.11.2] Rust-to-Python migration guide: Key differences, gotchas
- [ ] T167 [Analysis: Section.11.2] Performance comparison: Rust vs Python benchmarks
- [ ] T168 [Analysis: Section.11.2] Algorithm preservation notes: Critical logic ports
- [ ] T169 [P] Developer guide: Setup, testing, debugging

### Phase 14c: Operational Documentation

- [ ] T170 Deployment guide: Docker, environment variables, dependencies
- [ ] T171 Admin guide: Configuration, monitoring, troubleshooting
- [ ] T172 User guide: CLI usage, recipe authoring, tool integration

**Checkpoint**: Documentation complete

---

## Phase 15: Migration Validation & Cutover

**Purpose**: Final validation before production deployment

### Phase 15a: Functional Validation

- [ ] T173 [Analysis: Section.12.3] Full regression suite: All tests passing
- [ ] T174 [Analysis: Section.4.1] Algorithm parity: All critical algorithms validated
- [ ] T175 [Analysis: Section.5.2] MCP compatibility: All MCP tools working
- [ ] T176 [Analysis: Section.11.3] User workflow parity: All Rust workflows functional in Python
- [ ] T177 [Ground Truth] Side-by-side comparison: Rust vs Python agent behavior

### Phase 15b: Performance Validation

- [ ] T178 [Analysis: Section.8.1] Response time validation: Agent reply latency acceptable
- [ ] T179 [Analysis: Section.8.1] Tool execution latency: Within acceptable thresholds
- [ ] T180 [Analysis: Section.8.1] Streaming performance: SSE latency comparable to Rust
- [ ] T181 [Analysis: Section.8.3] Memory usage: Python memory overhead acceptable

### Phase 15c: Production Deployment

- [ ] T182 Production environment setup: FastAPI server, dependencies, MCP clients
- [ ] T183 Configuration validation: Environment variables, API keys, OAuth
- [ ] T184 Smoke tests: Critical workflows in production environment
- [ ] T185 Monitoring setup: Application metrics, error tracking, performance
- [ ] T186 Stakeholder sign-off: User acceptance testing passed

### Phase 15d: Legacy Asset Retirement

- [ ] T187 [Analysis: Section.12.2] Legacy asset archive: Full Rust codebase backup
- [ ] T188 Post-migration monitoring: 30-day observation period
- [ ] T189 Performance monitoring: Validate sustained performance
- [ ] T190 User feedback collection: Address any migration issues
- [ ] T191 Delete legacy asset: Remove `features/goose/` after validation complete

**Checkpoint**: Migration complete, production operational

---

## Dependencies & Execution Order

### Sequential Foundation (Must Complete First)

**Phase 1-2 (Foundation)**: MANDATORY sequential completion
- Phase 1 establishes foundation service boundaries
- Phase 2 creates shared libraries for all domains
- **Blocking**: ALL domain-specific phases (3-12) depend on Phase 1-2 completion

### Parallel Domain Migration (After Foundation)

**Phases 3-7 (Domain Bounded Contexts)**: Can execute in parallel once foundation complete
- Phase 3: Conversation Management domain
- Phase 4: Agent Orchestration domain  
- Phase 5: Tool Management domain (MCP integration)
- Phase 6: Provider Abstraction domain
- Phase 7: Recipe Engine domain

**Dependencies within parallel phases**:
- Each domain is self-contained (bounded context isolation)
- Shared libraries (Phase 2) provide cross-domain contracts
- Domain teams can work independently with minimal coordination

### Sequential Integration (After Domains)

**Phases 8-9 (Cross-Domain Integration)**: Sequential after all domain phases
- Phase 8: Agent-Tool integration requires Phases 4-5 complete
- Phase 9: Full workflow integration requires Phases 3-7 complete

### Final Sequential Phases

**Phases 10-15 (Quality & Deployment)**: Sequential progression
- Phase 10: API & interfaces (requires all domains migrated)
- Phase 11: CLI migration (requires API complete)
- Phase 12: Security hardening (requires all logic migrated)
- Phase 13: Testing & QA (validates all previous phases)
- Phase 14: Documentation (documents complete system)
- Phase 15: Production cutover (final validation & deployment)

### Critical Path for MVP

**Minimum viable agent** (conversation + single provider + no tools):
1. Phase 1-2 (foundation) → ~24 hours
2. Phase 3 (conversation management) → ~32 hours  
3. Phase 6a only (OpenAI provider) → ~8 hours
4. Phase 10a (basic API) → ~8 hours
5. Phase 11a (basic CLI) → ~4 hours
**MVP Timeline**: ~76 hours (2 weeks with 1 developer)

**Full-featured agent** (all domains):
- Foundation + All domains + Integration + Polish: ~280 hours (7 weeks with 1 developer)
- Parallel execution (3 developers): ~120 hours (3 weeks)

### Risk Mitigation Strategy

**Rust-to-Python validation gates**:
- Ground truth tests MUST pass before any domain phase completes
- Algorithm preservation validated incrementally (not at the end)
- Performance baselines measured continuously, not just Phase 15

**Rollback points**:
- After Phase 2: Can abort with minimal sunk cost
- After Phase 9: Partial agent functionality available (fallback option)
- After Phase 13: All logic validated, only deployment remains

---

## Implementation Strategy: Rust-to-Python Migration

### Language Migration Approach

**Critical Principle**: Preserve algorithmic behavior, not language idioms

1. **Rust Baseline Establishment** (Phase 1):
   - Run full Rust test suite: `cargo test --workspace`
   - Document Rust performance baselines: `cargo bench`
   - Capture Rust behavior as ground truth (golden outputs)

2. **Algorithm Preservation Strategy**:
   - Port Rust logic to Python focusing on **functional equivalence**, not line-by-line translation
   - Async patterns: Tokio → asyncio translation (event loop semantics differ)
   - Memory safety: Rust ownership → Python reference counting (document lifetime assumptions)
   - Type safety: Rust traits → Python protocols/ABCs (preserve interface contracts)

3. **Performance Validation** (each domain phase):
   - Python performance must be "acceptable", not "identical" to Rust
   - Target: <3x Rust latency for critical paths (conversation loop, tool execution)
   - Document tradeoffs: Python flexibility vs Rust performance

### Bounded Context Isolation

**Domain Independence** (enables parallel migration):
- Each domain is a separate Python module with clear interfaces
- Shared contracts defined in `libs/shared/` (Phase 2)
- Cross-domain communication through service adapters only

**Example**:
```
apps/jane-orchestrator/src/domains/
├── conversation/       # Phase 3 (independent)
├── agent/              # Phase 4 (independent)
├── tool_management/    # Phase 5 (independent)
├── providers/          # Phase 6 (independent)
└── recipe/             # Phase 7 (independent)
```

### Incremental Delivery Milestones

**Milestone 1: Foundation** (Phase 1-2, ~24 hours)
- FastAPI server skeleton running
- Shared libraries established
- **Deliverable**: Empty service with endpoints, no logic

**Milestone 2: Core Agent** (Phase 3-4, ~56 hours)
- Conversation management + Agent orchestration complete
- **Deliverable**: Agent can hold conversation, execute workflow (no tools/recipes)

**Milestone 3: Tool Integration** (Phase 5, ~24 hours)
- MCP protocol integration complete
- **Deliverable**: Agent can discover and execute MCP tools

**Milestone 4: Multi-Provider** (Phase 6, ~32 hours)
- All 20+ LLM providers integrated
- **Deliverable**: Agent works with OpenAI, Anthropic, Google, local models

**Milestone 5: Automation** (Phase 7, ~24 hours)
- Recipe engine complete
- **Deliverable**: Agent executes multi-step automation workflows

**Milestone 6: Production** (Phase 8-15, ~120 hours)
- Integration, API, CLI, security, testing, docs
- **Deliverable**: Full production-ready system

### Rust-Specific Migration Challenges

**Async Runtime Translation**:
- **Rust**: Tokio multi-threaded runtime with work-stealing scheduler
- **Python**: asyncio single-threaded event loop
- **Strategy**: Validate concurrency behavior in ground truth tests, accept different internal scheduling

**Error Handling**:
- **Rust**: Result<T, E> with explicit error propagation
- **Python**: Exceptions with try/except
- **Strategy**: Preserve error semantics (fail-fast vs graceful degradation), not error mechanisms

**Type System**:
- **Rust**: Compile-time guarantees with ownership/borrowing
- **Python**: Runtime validation with type hints + mypy
- **Strategy**: Use Pydantic for runtime validation, mypy for static checks

**MCP Protocol Fidelity**:
- **Rust**: `rmcp` crate (custom implementation)
- **Python**: Official `mcp` SDK (standard implementation)
- **Strategy**: Validate protocol compatibility in integration tests (Phase 5c)

### Quality Gates (Every Domain Phase)

**Pre-Completion Checklist**:
1. ✅ Ground truth tests pass (Rust behavior reproduced)
2. ✅ Unit tests achieve 80%+ coverage
3. ✅ Performance within acceptable thresholds (<3x Rust latency)
4. ✅ Integration tests pass (domain interfaces validated)
5. ✅ No regressions in previously migrated domains

**Validation Command** (per domain):
```bash
# Example for Conversation domain (Phase 3)
pytest tests/productivity/domains/conversation/ -v --cov
pytest tests/productivity/integration/test_conversation_rust_parity.py
```

### Risk-Minimized Parallel Execution

**Team Organization** (3 developers):
- **Developer A**: Foundation (Phase 1-2) → Conversation (Phase 3) → Integration (Phase 8)
- **Developer B**: Agent (Phase 4) → Tool Management (Phase 5) → API (Phase 10)
- **Developer C**: Providers (Phase 6) → Recipe (Phase 7) → CLI (Phase 11)

**Synchronization Points**:
- After Phase 2: All developers sync on shared library contracts
- After Phase 7: All developers sync for integration testing (Phase 8-9)
- After Phase 13: All developers participate in final validation

**Branch Strategy**:
- `main`: Always deployable (foundation only initially)
- `migration/conversation`, `migration/agent`, etc: Domain-specific branches
- Merge to `main` only after domain phase complete + validated

---

## Brownfield Migration Methodology Notes

**Task Completion Criteria:**
- **[P] tasks**: Different bounded contexts, no dependencies (parallel execution safe)
- **[Analysis] references**: Trace to Goose analysis report findings (evidence-based migration)
- **[Logic: file::function]**: Rust source reference for algorithm preservation (e.g., `[Logic: crates/goose/src/agents/mod.rs::Agent::run]`)
- **[Ground Truth]**: Rust test suite establishes behavioral baseline
- **Completion sequence**: Ground Truth (Rust) → Analysis Cross-Reference → Port Logic (Python) → Validate (Python test passes) → Integrate

**Quality Gates:**
- Every phase has explicit checkpoints requiring validation before proceeding
- All critical algorithms must have Rust-to-Python parity tests
- Performance baselines: <3x Rust latency for critical paths, <5x for background tasks
- MCP protocol compliance: 100% compatibility with official spec

**Rust-to-Python Migration Rules:**
1. **Never assume Python idioms are better** - preserve Rust algorithmic patterns
2. **Validate incrementally** - don't wait until Phase 15 to test Rust parity
3. **Document semantic gaps** - where Python can't match Rust behavior (e.g., memory safety guarantees)
4. **Performance tradeoffs are acceptable** - within documented thresholds

**Success Validation:**
- **Functional parity**: Python agent behaves identically to Rust agent (validated by ground truth tests)
- **Performance parity**: <3x Rust latency for user-facing operations
- **Integration parity**: MCP tools, LLM providers work without changes
- **Algorithm parity**: Critical logic (agent execution, tool orchestration, provider abstraction) functions identically

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent task complete**:

- [ ] All tasks T001-T191 marked complete above
- [ ] Rust baseline tests documented: `cargo test --workspace` results captured
- [ ] Python test suite passes: `pytest tests/productivity/ -v --cov`
- [ ] Integration tests pass: `pytest tests/productivity/test_goose_integration.py`
- [ ] Performance baselines met: <3x Rust latency for critical paths (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity: Python agent behavior matches Rust agent
- [ ] MCP protocol compliance validated: All MCP tools from Rust version work in Python
- [ ] Legacy `features/goose/` backed up to `archive/goose-rust-baseline/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] No regressions in existing productivity domain functionality
- [ ] Security audit passed: OAuth flows, API key storage, tool permissions validated
- [ ] All 20+ LLM providers tested and functional

**Rust-Specific Validation**:
- [ ] Async runtime behavior validated (asyncio vs Tokio semantic differences documented)
- [ ] Error handling parity confirmed (Result<T,E> semantics preserved in Python)
- [ ] Type safety validated (mypy + Pydantic runtime checks equivalent to Rust compile-time checks)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run full validation suite: `pytest tests/productivity/ -v --cov && cargo test --manifest-path features/goose/Cargo.toml`
3. Document completion in `migration-validation.md`
4. Archive Rust baseline: `mv features/goose/ archive/goose-rust-baseline/`
5. Mark parent task (TXXX in `tasks.md`) complete
6. Proceed to next project migration

**Documentation Update Required**:
```markdown
# In migration-validation.md

### Goose Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: 280
- **Actual Hours**: [ACTUAL]
- **Language Migration**: Rust Edition 2021 → Python 3.12 + FastAPI
- **Tests**: [X] passed, 0 failed
- **Performance**: <3x Rust latency (critical paths), <5x Rust latency (background tasks)
- **Rust Baseline**: Archived to `archive/goose-rust-baseline/`
- **Ground Truth Tests**: [X] Rust-Python parity tests passed
- **MCP Compatibility**: All MCP tools validated functional
- **Provider Coverage**: 20+ LLM providers tested and operational
- **Notes**: [Any notable achievements, performance tradeoffs, or challenges]
```

