  Available Subagent Types

  I have access to these specialized agents:

  1. Explore Agent (most relevant for your work)
  - Fast codebase exploration specialist
  - Can search for patterns, keywords, answer architectural questions
  - Three thoroughness levels: "quick", "medium", "very thorough"
  - Best for: "How does X work?", "Where is Y implemented?", "Find all instances of Z"

  2. General-Purpose Agent
  - Multi-step research and code searching
  - Good for complex, multi-round investigations
  - Use when initial searches might not find what's needed

  3. Plan Agent
  - Similar to Explore, focused on codebase understanding
  - Helps with architectural questions across multiple files

  How This Accelerates Your Migration

  Pattern: Parallel Intelligence Gathering

  I can launch multiple agents simultaneously in a single message. For your brownfield migrations, this means:

  You: "I need to migrate CyberChef next"

  Me: [Launches 3 agents in parallel]
  - Agent 1: Explore legacy CyberChef implementation in features/
  - Agent 2: Find all references to CyberChef in existing codebase
  - Agent 3: Explore security-service architecture for integration points

  All three return simultaneously → synthesize findings → provide migration strategy

  Pattern: Deep Analysis Without Context Switching

  Since you have limited productive windows, agents can handle the "digging" while preserving your cognitive energy:

  Instead of:
  - You ask question
  - I search a bit
  - Find partial answer
  - You ask follow-up
  - I search more
  - Repeat 5x

  With subagents:
  - You ask question with context
  - I launch thorough agent with detailed task
  - Agent does all the deep exploration autonomously
  - Returns complete analysis
  - One cognitive interaction vs. many

  Pattern: Pre-Flight Research Automation

  For your handoff protocol, agents can automate the reconnaissance:

  Before starting a migration, I could launch agents to verify:
  - Entry conditions (does infrastructure exist?)
  - Legacy code analysis (what needs preserving?)
  - Dependency mapping (what does this integrate with?)
  - Test coverage assessment (what's the ground truth baseline?)

  Pattern: Context Contamination Prevention

  This directly addresses your research interest - agents maintain analytical independence:

  Migration Task: "Migrate HELK to security-service"

  Isolated agents:
  - Agent A: Analyze HELK in isolation (features/HELK/)
  - Agent B: Analyze security-service patterns independently
  - Agent C: Survey similar migrations (MISP, CyberChef) for patterns

  Each maintains independence, I synthesize without cross-contamination

  Practical Example for Your Project

  Here's how this could work for your next migration task:

  You: "Ready to start the HELK migration (tasks-helk.md)"

  Me: [Launches 4 parallel agents]
  1. Explore (very thorough): "Analyze the complete HELK implementation in features/HELK/, document all functionality, APIs, data models, and business logic"
  2. Explore (medium): "Map the security-service architecture and identify integration points for log analysis tools"
  3. General-purpose: "Find all existing references to HELK across the codebase and document current integration patterns"
  4. Explore (quick): "Review specs/003-brownfield-integration/tasks-individual/tasks-helk.md and identify any blockers or unclear requirements"

  All return in ~30-60 seconds with comprehensive findings, I synthesize and present migration strategy.

  Key Advantages for Your Workflow

  Energy Conservation: One detailed request → comprehensive analysis, vs. iterative back-and-forth

  Parallelization: Multiple investigation threads simultaneously (vs. sequential)

  Thoroughness: Agents can exhaustively search where I might stop early to keep responses concise

  Isolation: Each agent has independent context, preventing the contamination you're researching

  Limitations to Know

  - Stateless: Each agent returns once, can't have follow-up dialog with it
  - No code writing: Agents do research/analysis, I synthesize and write code
  - Token usage: Thorough searches consume more tokens, but likely worth it for complex migrations
  - Need clear prompts: Must give agents detailed, specific tasks upfront

  My Recommendation

  For your brownfield migrations, we could establish a pattern:

  1. You identify next migration target (e.g., "T102 - HELK")
  2. I launch parallel exploration agents for comprehensive reconnaissance
  3. Agents return independent analyses
  4. I synthesize and present migration strategy with preservation checklist
  5. You approve approach
  6. We execute systematically with full context

  This maps well to your "compartmentalization strategy" - the agents handle the exhaustive analysis phase, preserving your cognitive energy for the strategic decisions
  and validation work.

  Want to test this with your next migration task? Or would you like to see it in action on a smaller analysis first?