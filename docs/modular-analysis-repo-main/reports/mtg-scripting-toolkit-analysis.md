# MTG Scripting Toolkit Project Analysis Report

**Analysis Date:** October 12, 2025  
**Analyzed By:** GitHub Copilot  
**Repository:** https://github.com/ahmattox/mtg-scripting-toolkit  
**Version:** Current (no version tags)

---

## Section 1: Project Identity & Context

### 1.1 Basic Information
```yaml
Project Name: MTG Scripting Toolkit
Repository URL: https://github.com/ahmattox/mtg-scripting-toolkit
Primary Domain: Magic: The Gathering / Card Game Data Analysis / Scripts & Utilities
Project Status: Active (Personal/Research project)
Business Purpose: A TypeScript toolkit for analyzing Magic: The Gathering card data, providing utilities for fetching from multiple sources (Scryfall, Cube Cobra, Commander Spellbook) and performing data transformations for research and content creation
Key Stakeholders: Anthony Mattox (author), Lucky Paper (content creation), Magic research community, MTG data analysts
Monthly Active Users: Unknown (personal research tool, not a service)
Critical to Business: SOMEWHAT - Important for Lucky Paper content creation and personal MTG research projects
```

### 1.2 Technology Stack Inventory
```yaml
Programming Languages:
  - Language: TypeScript
    Version: ^4.9.4
    Percentage of Codebase: ~95%
    Primary Use: All utilities, scripts, and data processing logic
    Why Chosen: Type safety for complex MTG data structures, excellent tooling, JavaScript ecosystem access

  - Language: JavaScript (generated)
    Version: ES2020+ (via TypeScript compilation)
    Percentage of Codebase: ~5% (generated)
    Primary Use: Runtime execution via tsx
    Why Chosen: Target runtime environment (Node.js)

Primary Frameworks:
  Backend:
    - Name: Node.js
      Version: ^18.16.0
      Why Chosen: JavaScript runtime for scripts, excellent ecosystem for data processing
  
  Frontend:
    - Name: None (CLI/Script-based tool)
      Version: N/A
      Description: No web frontend - purely command-line scripts
      Why Chosen: Designed for data analysis workflows, not user interfaces

Database:
  Primary:
    - Type: File-based caching (.cache directory)
      Version: N/A
      Description: Local filesystem caching for API responses and bulk data
      Schema Location: No formal schema - cached JSON files
  
  Cache:
    - Type: File system cache
      Version: N/A
      Use Case: Scryfall bulk data caching, API response caching

Build & Dev Tools:
  - Package Manager: Yarn (referenced in README)
  - Build Tool: TypeScript Compiler (tsc) + tsx for execution
  - Linter: ESLint with TypeScript plugin
  - Formatter: Prettier
  - Testing Framework: None explicitly configured
  - CI/CD: None configured (personal project)
  - Runtime: tsx (TypeScript execution) + Node.js

Infrastructure:
  - Hosting: N/A (local scripts)
  - Containerization: None
  - Orchestration: None  
  - Environment Variables: None documented (uses direct API calls)
```

### 1.3 Project Structure
```
mtg-scripting-toolkit/
├── scripts/                      # Entry point scripts and examples
│   ├── search.ts                 # Main search script interface
│   ├── template.ts               # Script template for new scripts
│   └── examples/                 # Example scripts demonstrating various use cases
│       ├── card-list-first-printings.ts
│       ├── commander-spellbook.ts
│       ├── cube-cobra-*.ts      # Various Cube Cobra integrations
│       ├── power-analysis.ts    # MTG-specific data analysis
│       └── [20+ other examples]
├── utils/                       # Core utility modules (reusable functions)
│   ├── cache.ts                 # File-based caching utilities
│   ├── log.ts                   # Logging utilities  
│   ├── math.ts                  # Mathematical utilities
│   ├── scryfall/               # Scryfall API integration
│   │   ├── index.ts            # Main Scryfall utilities
│   │   ├── types.ts            # TypeScript types for Scryfall API
│   │   ├── search.ts           # Card search functionality
│   │   ├── bulkData.ts         # Bulk data download and caching
│   │   └── fetch*.ts           # Various API endpoint wrappers
│   ├── cube-cobra/             # Cube Cobra platform integration
│   │   ├── index.ts            # Main Cube Cobra utilities
│   │   └── types.ts            # Cube Cobra data types
│   ├── commander-spellbook/    # Commander Spellbook combo database
│   │   ├── index.ts            # Combo fetching and processing
│   │   └── types.ts            # Combo and card relationship types
│   ├── academy-ruins/          # MTG rules archive integration
│   └── mtg/                    # MTG domain-specific utilities
│       ├── card.ts             # Card property extraction and analysis
│       ├── cardTypes.ts        # MTG card type utilities
│       ├── cardColors.ts       # Color identity and mana cost analysis
│       ├── sort.ts             # MTG-specific sorting (color order, etc.)
│       └── [other MTG utilities]
├── package.json                # Dependencies and scripts
├── tsconfig.json              # TypeScript configuration
└── [standard config files]   # ESLint, Prettier, etc.

Key Directories Explained:
- scripts/: Ready-to-run analysis scripts and examples for common MTG data tasks
- utils/scryfall/: Complete Scryfall API wrapper with types and caching
- utils/mtg/: Domain-specific utilities for MTG card analysis and processing  
- utils/cube-cobra/: Integration with Cube Cobra for cube list analysis
- utils/commander-spellbook/: Commander combo database access and analysis
```

---

## Section 2: Data Architecture [CRITICAL]

### 2.1 Data Models Inventory

```yaml
Model Name: Card (Scryfall)
Description: Complete representation of a Magic: The Gathering card from Scryfall's API
Priority: CRITICAL
Source File: utils/scryfall/types.ts

Fields:
  - name: id
    type: string (UUID)
    constraints: unique, required
    default: none
    description: Scryfall's unique identifier for this card
    business_rules: Primary key for card identification across all systems
  
  - name: oracle_id
    type: string (UUID)
    constraints: required
    default: none
    description: Scryfall identifier for the abstract card, shared across printings
    business_rules: Groups all printings of the same abstract card
  
  - name: name
    type: string
    constraints: required
    default: none
    description: The card's name as it appears on the card
    business_rules: Primary display name, used for sorting and searching
  
  - name: mana_cost
    type: string
    constraints: optional (some cards have no mana cost)
    default: none
    description: Mana cost in Magic notation (e.g., "{3}{U}{B}")
    business_rules: Used for curve analysis and color identity determination
  
  - name: cmc
    type: number
    constraints: required, >= 0
    default: 0
    description: Converted mana cost (total mana cost as a number)
    business_rules: Key metric for deck building and analysis
  
  - name: type_line
    type: string
    constraints: required
    default: none
    description: Full type line (e.g., "Legendary Creature — Human Wizard")
    business_rules: Determines card categorization and rule interactions
  
  - name: oracle_text
    type: string
    constraints: optional
    default: none
    description: The card's rules text
    business_rules: Used for text analysis and combo detection
  
  - name: power
    type: string (can be "*" or number)
    constraints: optional
    default: none
    description: Creature power value
    business_rules: Used for creature analysis, can be variable (*)
  
  - name: toughness
    type: string (can be "*" or number)
    constraints: optional
    default: none
    description: Creature toughness value
    business_rules: Used for creature analysis, can be variable (*)
  
  - name: colors
    type: Color[] (enum array)
    constraints: optional
    default: empty array
    description: Colors in the card's mana cost
    business_rules: Determines color identity for deck building restrictions
  
  - name: color_identity
    type: Color[] (enum array)
    constraints: required
    default: empty array
    description: All colors that appear anywhere on the card
    business_rules: Critical for Commander format deck building rules
  
  - name: legalities
    type: Record<Format, Legality>
    constraints: required
    default: all formats
    description: Legal status in each Magic format
    business_rules: Determines which decks/formats the card can be used in
  
  - name: set
    type: string
    constraints: required, 3-4 characters
    default: none
    description: Three-letter set code (e.g., "DOM", "RNA")
    business_rules: Used for set analysis and card availability tracking
  
  - name: rarity
    type: Rarity (enum)
    constraints: required
    default: none
    description: Card rarity (common, uncommon, rare, mythic, special, bonus)
    business_rules: Affects draft value and collection management
  
  - name: card_faces
    type: CardFace[]
    constraints: optional (only for double-faced cards)
    default: none
    description: Separate faces for transform/modal double-faced cards
    business_rules: Each face can have different names, costs, and abilities

Relationships:
  - related_model: CardFace
    relationship_type: one-to-many
    relationship_name: card_faces
    cascade_behavior: included in card data
    description: Double-faced cards have multiple faces with separate properties

  - related_model: Set
    relationship_type: many-to-one
    relationship_name: set reference
    cascade_behavior: foreign key reference
    description: Cards belong to specific Magic sets/expansions

Indexes:
  - fields: [name]
    type: text search
    reason: Primary search mechanism for cards
  
  - fields: [oracle_id]
    type: btree
    reason: Grouping different printings of same card
  
  - fields: [set, collector_number]
    type: unique
    reason: Unique identification within a set

Computed Fields:
  - name: totalPower
    computation: sum of power across all faces (for multi-faced cards)
    generated: application_layer
    example: Transform card with 2/2 front, 4/4 back = 6 total power
  
  - name: wordCount
    computation: count of words in oracle_text
    generated: application_layer (utils/wordCount.ts)
    example: "Draw two cards" = 3 words

Validation Rules:
  - rule: "Color identity must include all mana symbols on card"
    enforced: application
    error_message: "Color identity validation failed"
  
  - rule: "Double-faced cards must have card_faces array"
    enforced: application
    error_message: "Multi-face layout requires card_faces data"

Special Behaviors:
  - behavior: "Auto-calculates derived color properties"
    implementation: utils/mtg/cardColors.ts
    code_location: utils/mtg/cardColors.ts
  
  - behavior: "Handles variable power/toughness (*)"
    implementation: parseNumber function with fallback to 0
    code_location: utils/mtg/card.ts
```

```yaml
Model Name: Combo (Commander Spellbook)
Description: Represents a Magic combo from Commander Spellbook database with associated cards
Priority: IMPORTANT
Source File: utils/commander-spellbook/types.ts

Fields:
  - name: cards
    type: scryfall.Card[]
    constraints: required, minimum 2 cards
    default: empty array
    description: Full Scryfall card objects for each card in the combo
    business_rules: Enriched with full card data for analysis
  
  - name: cardNames
    type: string[]
    constraints: required
    default: none
    description: Array of card names in the combo
    business_rules: Used for display and filtering
  
  - name: colorIdentity
    type: string
    constraints: optional
    default: none
    description: Combined color identity of all cards in combo
    business_rules: Determines Commander format compatibility
  
  - name: prerequisites
    type: string
    constraints: optional
    default: none
    description: Setup requirements for the combo
    business_rules: Human-readable conditions needed before combo works
  
  - name: steps
    type: string
    constraints: optional
    default: none
    description: Step-by-step instructions to execute combo
    business_rules: Human-readable combo execution guide
  
  - name: results
    type: string[]
    constraints: optional
    default: empty array
    description: What the combo accomplishes (e.g., "Infinite mana")
    business_rules: Used for filtering and categorizing combos
  
  - name: legalities
    type: Record<Format, 'legal' | 'not_legal'>
    constraints: required
    default: computed from card legalities
    description: Format legality based on component cards
    business_rules: Combo is legal only if all cards are legal in format

Relationships:
  - related_model: Card
    relationship_type: many-to-many
    relationship_name: cards array
    cascade_behavior: embedded full objects
    description: Combos contain multiple cards with full Scryfall data

Computed Fields:
  - name: totalCMC
    computation: sum of all cards' converted mana costs
    generated: application_layer
    example: 3-card combo with CMCs 2,3,4 = 9 total
  
  - name: combinedColorIdentity
    computation: union of all cards' color identities
    generated: application_layer
    example: {W}{U} + {U}{B} = {W}{U}{B}

Special Behaviors:
  - behavior: "Enriches combo data with full Scryfall card objects"
    implementation: Fetches card data and merges with combo metadata
    code_location: utils/commander-spellbook/fetch.ts
```

```yaml
Model Name: CubeCobraCard
Description: Card representation from Cube Cobra platform with cube-specific metadata
Priority: IMPORTANT
Source File: utils/cube-cobra/types.ts

Fields:
  - name: cardID
    type: string
    constraints: required
    default: none
    description: Scryfall card ID reference
    business_rules: Links to Scryfall card for full data
  
  - name: tags
    type: string[]
    constraints: optional
    default: empty array
    description: Cube owner's custom tags for the card
    business_rules: Used for cube organization and filtering
  
  - name: status
    type: string ("Owned" | other)
    constraints: required
    default: none
    description: Ownership status in cube owner's collection
    business_rules: Tracks physical card availability
  
  - name: board
    type: string ("mainboard" | "maybeboard")
    constraints: required
    default: none
    description: Which section of the cube the card is in
    business_rules: Mainboard cards are in active cube, maybeboard are potential additions
  
  - name: finish
    type: string ("Foil" | "Non-foil")
    constraints: required
    default: none
    description: Physical card finish preference
    business_rules: Aesthetic and value tracking
  
  - name: addedTmsp
    type: number (timestamp)
    constraints: required
    default: none
    description: When the card was added to the cube
    business_rules: Used for cube evolution analysis

Relationships:
  - related_model: Card (Scryfall)
    relationship_type: many-to-one
    relationship_name: cardID reference
    cascade_behavior: foreign key
    description: Each cube card references a Scryfall card

Special Behaviors:
  - behavior: "Enriched with Scryfall data during fetch operations"
    implementation: Fetches full card data using cardID
    code_location: utils/cube-cobra/index.ts
```

### 2.2 Critical Data Relationships Map

```
Scryfall Card (1) ────< many >──── CubeCobraCard (many)
       │                               │
       │                               │
      oracle_id                    cardID (FK)
       │                               │
       ▼                               ▼
Card Printings (many)              Cube Membership
       │                               │
       │                               │
       │                         tags, status, board
       │                               │
       ▼                               ▼
   Set/Rarity                    Cube Analysis
       │
       │
       ▼
Commander Combo (many) ────< contains >──── Card (many)
       │                                       │
       │                                   name, colors
       │                                       │
       ▼                                       ▼
   results[]                            Color Identity
prerequisites                              Format Legality
    steps

Critical Data Flow:
1. Scryfall Cards are the canonical source of truth for all card data
2. CubeCobraCards reference Scryfall cards but add cube-specific metadata
3. Commander Combos combine multiple Scryfall cards with combo-specific instructions
4. All analysis derives from Scryfall card properties (colors, types, costs, etc.)
5. Caching layer stores Scryfall bulk data locally to avoid repeated API calls
```

### 2.3 Database Performance Patterns

```yaml
Query Optimization Strategies:
  - strategy: Bulk data download and local caching
    location: utils/scryfall/bulkData.ts
    reason: Avoids thousands of individual API calls for large datasets
    impact: Download once, query locally - 1000x+ performance improvement
  
  - strategy: File-based caching with TTL
    location: utils/cache.ts
    reason: Prevents redundant API calls during development/analysis
    impact: Subsequent runs are near-instantaneous
  
  - strategy: Lazy loading of related data
    location: utils/commander-spellbook/fetch.ts
    reason: Only fetch full card data when combo analysis is needed
    impact: Faster initial combo loading, full enrichment on demand

Denormalization Patterns:
  - pattern: Embedded card objects in combos
    fields: Full Scryfall card data included in Combo interface
    update_trigger: Fetched fresh each time combo data is requested
    reason: Avoid N+1 queries when analyzing combo properties
  
  - pattern: Computed color identity on combos
    fields: colorIdentity derived from component cards
    update_trigger: Calculated during combo enrichment
    reason: Enable fast filtering by color without card lookups

Problematic Queries:
  - query_description: Text search across all card oracle text without indexing
    performance: slow (O(n) scan of all cards)
    location: Any script doing full-text search
    notes: Scryfall's search API is preferred for complex text queries
  
  - query_description: Loading all cards for single cube analysis
    performance: acceptable (cached bulk data)
    location: cube analysis scripts
    notes: Bulk data makes this feasible, but filtering early is beneficial
```

---

## Section 3: API Architecture [CRITICAL]

### 3.1 Authentication & Authorization

```yaml
Authentication Method:
  - type: None (Public APIs)
    provider: All integrated APIs are public and free
    implementation_location: No authentication required
    token_lifetime: N/A
    refresh_strategy: N/A

Authorization Pattern:
  - type: Public access with rate limiting
    roles_list: N/A (no user accounts)
    permissions_list: N/A (read-only access to public data)

Access Control Rules:
  - rule: "Respect API rate limits to avoid being blocked"
    enforcement_location: Client-side throttling and caching

External Auth Integrations:
  - provider: None
    scopes_required: N/A
    user_validation: N/A
    failure_handling: API rate limiting handled by caching and throttling
```

### 3.2 API Endpoints Inventory

```yaml
Endpoint: GET https://api.scryfall.com/cards/search
Example: GET /cards/search?q=o:saproling

Authentication Required: NO
Authorization: Public API access

Request:
  Query Parameters:
    - name: q
      type: string
      description: Scryfall search query syntax
      example: "o:saproling t:creature"
    
    - name: order
      type: string
      description: Sort order (name, set, released, rarity, etc.)
      example: "cmc"
    
    - name: dir
      type: string
      description: Sort direction (auto, asc, desc)
      example: "asc"
    
    - name: unique
      type: string
      description: Rollup mode (cards, art, prints)
      example: "cards"
  
  Headers:
    - name: User-Agent
      description: Identifies the client application
      required: Recommended by Scryfall

Response:
  Success (200):
    ```json
    {
      "object": "list",
      "total_cards": 1234,
      "has_more": true,
      "next_page": "https://api.scryfall.com/cards/search?format=json&include_extras=false&include_multilingual=false&order=name&page=2&q=o%3Asaproling&unique=cards",
      "data": [
        {
          "object": "card",
          "id": "card-uuid",
          "name": "Saproling Token",
          "mana_cost": "",
          "cmc": 0,
          "type_line": "Token Creature — Saproling",
          "oracle_text": null,
          "colors": [],
          "color_identity": [],
          "legalities": {...}
        }
      ]
    }
    ```
  
  Error Cases:
    - status: 404
      description: No cards found for query
    - status: 422  
      description: Invalid query syntax
    - status: 429
      description: Rate limit exceeded

Business Logic:
  - Executes complex card searches using Scryfall's powerful query language
  - Supports filtering by any card attribute (name, type, color, set, etc.)
  - Handles pagination automatically for large result sets
  - Provides sorting and uniqueness options for different analysis needs
  
Performance:
  - Average Response Time: 200-500ms (depends on query complexity)
  - P95 Response Time: 1000ms
  - Rate Limited: YES - ~100-175 requests per second

Dependencies:
  - External API: Scryfall API
    Failure Handling: Cache previous results, retry with exponential backoff
  
  - Database Queries: None (pure API client)
    Optimization: Client-side caching of responses
```

```yaml
Endpoint: GET https://api.scryfall.com/bulk-data
Example: GET /bulk-data/oracle_cards

Authentication Required: NO
Authorization: Public API access

Request:
  Path Parameters:
    - name: type
      type: string
      description: Type of bulk data (oracle_cards, default_cards, all_cards, etc.)
      example: "oracle_cards"

Response:
  Success (200):
    - Large JSON file with complete card database (~50MB compressed)
    - Contains array of all cards matching the bulk data type
    - Updated daily by Scryfall
  
  Error Cases:
    - status: 404
      description: Bulk data type not found

Business Logic:
  - Downloads complete Scryfall database for offline analysis
  - Enables fast local queries without API rate limits
  - Updated daily, cached locally until expired
  - Used for comprehensive analysis requiring all cards
  
Performance:
  - Average Response Time: 10-30 seconds (large download)
  - File Size: ~50MB compressed, ~200MB uncompressed
  - Rate Limited: NO (bulk download endpoints are not rate limited)

Dependencies:
  - External API: Scryfall bulk data CDN
    Failure Handling: Retry download, fall back to cached version
  
  - Local Storage: File system cache
    Optimization: Only download if newer version available
```

```yaml
Endpoint: GET https://docs.google.com/spreadsheets/d/{id}/gviz/tq
Example: Commander Spellbook Google Sheets API

Authentication Required: NO
Authorization: Public read access to published Google Sheet

Request:
  Path Parameters:
    - name: sheet_id
      type: string
      description: Google Sheets document ID
      example: "1KqyDRZRCgy8YgMFnY0tHSw_3jC99Z0zFvJrPbfm66vA"
  
  Query Parameters:
    - name: tqx
      type: string  
      description: Output format specification
      example: "out:csv"
    
    - name: sheet
      type: string
      description: Sheet name within document
      example: "combos"

Response:
  Success (200):
    - CSV format containing combo data
    - Columns: Card names, prerequisites, steps, results, legalities
  
  Error Cases:
    - status: 403
      description: Sheet not publicly accessible
    - status: 404
      description: Sheet or document not found

Business Logic:
  - Fetches curated combo database from Commander Spellbook community
  - Parses CSV data into structured combo objects
  - Enriches combos with full Scryfall card data
  - Enables combo analysis and filtering
  
Performance:
  - Average Response Time: 1-3 seconds
  - Data Size: ~1-5MB CSV file
  - Rate Limited: NO (Google Sheets has generous limits)

Dependencies:
  - External API: Google Sheets public API
    Failure Handling: Cache previous version, retry with backoff
  
  - Data Enrichment: Scryfall API calls for each card in combos
    Optimization: Batch card lookups, cache card data
```

```yaml
Endpoint: GET https://cubecobra.com/cube/api/cubelist/{cubeId}
Example: GET /cube/api/cubelist/regular

Authentication Required: NO
Authorization: Public access to published cubes

Request:
  Path Parameters:
    - name: cubeId
      type: string
      description: Unique cube identifier on Cube Cobra
      example: "regular"

Response:
  Success (200):
    - Plain text list of card names, one per line
    - May include specific set codes in brackets [SET]
  
  Error Cases:
    - status: 404
      description: Cube not found or private
    - status: 500
      description: Cube Cobra server error

Business Logic:
  - Fetches simple card list for cube analysis
  - Minimal data - just card names and optional set preferences
  - Used for basic cube composition analysis
  - Can be enriched with full card data from Scryfall
  
Performance:
  - Average Response Time: 200-500ms
  - Data Size: Small (few KB for typical cube)
  - Rate Limited: Unknown (reasonable use expected)

Dependencies:
  - External API: Cube Cobra platform
    Failure Handling: Cache cube lists, handle temporary outages
  
  - Data Enrichment: Scryfall lookups for full card data
    Optimization: Batch lookups, fuzzy name matching for reliability
```

### 3.3 API Patterns & Conventions

```yaml
REST Conventions:
  - URL Pattern: Each service follows its own conventions
    - Scryfall: /cards/search, /cards/named, /bulk-data/type
    - Cube Cobra: /cube/api/cubelist/{id}
    - Google Sheets: /spreadsheets/{id}/gviz/tq
  - Pagination: Scryfall uses cursor-based pagination with next_page URLs
  - Filtering: Scryfall uses powerful query language, others use path/query params
  - Sorting: Scryfall supports multiple sort orders, others have fixed ordering
  - Versioning Strategy: No explicit versioning (APIs evolve compatibly)

Error Handling Pattern:
  - Standard Error Format: 
    ```json
    {
      "object": "error",
      "code": "not_found", 
      "status": 404,
      "details": "No cards found."
    }
    ```
    (Scryfall format - others vary)
  
  - HTTP Status Code Usage:
    - 200: Success
    - 404: Resource not found (card, cube, sheet)
    - 422: Invalid query/parameters (Scryfall)
    - 429: Rate limit exceeded (Scryfall)
    - 500: Server error

Data Serialization:
  - Request Format: Query parameters, no request bodies typically
  - Response Format: JSON (Scryfall), CSV (Google Sheets), Plain text (Cube Cobra lists)
  - Date Format: ISO 8601 for dates (Scryfall), varies for others
  - Null Handling: null for missing values, empty arrays for empty lists

Rate Limiting:
  - Implemented: YES (Scryfall), UNKNOWN (others)
  - Strategy: Token bucket (Scryfall)
  - Limits: ~100-175 req/sec (Scryfall), reasonable use (others)
  - Headers: Scryfall doesn't expose rate limit headers
  - Client-side Strategy: Caching and request throttling to stay well under limits

Caching Strategy:
  - Bulk Data: Cache until Scryfall indicates newer version available
  - Search Results: Cache for development iterations, not production use
  - Card Data: Cache individual cards for session duration
  - Cube Lists: Cache to avoid repeated requests during analysis
  - TTL: Varies by data type - bulk data (daily), searches (session), cards (permanent)
```

---

## Section 4: Business Logic [CRITICAL]

### 4.1 Critical Algorithms

```yaml
Algorithm Name: Magic Color Identity Sorting
Location: utils/mtg/sort.ts and utils/mtg/magicSort.ts
Lines of Code: ~90
Complexity: Medium
Priority: MUST PRESERVE

Purpose:
  Implements Magic: The Gathering's traditional color ordering system for organizing cards in a way that's familiar to players. This is critical for deck building and analysis tools as it follows WUBR(G) color order and standard multicolor groupings.

Inputs:
  - cards: scryfall.Card[] (array of Magic cards to sort)
  - card.color_identity: Color[] (colors that appear anywhere on the card)
  - card.type_line: string (card types for secondary sorting)
  - card.cmc: number (converted mana cost for tertiary sorting)

Outputs:
  - sortedCards: scryfall.Card[] (cards arranged in traditional Magic order)
  - colorGroups: Cards organized by mono/multi/colorless/land categories

Algorithm Logic:
  1. Determine color group for each card:
     a. Monocolored cards: W, U, B, R, G (in WUBRG order)
     b. Multicolored cards: All combinations in predetermined order
     c. Colorless cards: No colors in mana cost or color identity
     d. Lands: Special category regardless of color production
  
  2. Within each color group, sort by card type:
     a. Creature, Instant, Sorcery, Artifact, Enchantment, Planeswalker, Land
  
  3. Within each type, sort by converted mana cost (CMC)
  
  4. For multicolored and lands, use detailed color identity ordering:
     a. Two-color pairs: WU, WB, WR, WG, UB, UR, UG, BR, BG, RG
     b. Three-color combinations: Shards and Wedges in established order
     c. Four and five color combinations

Edge Cases Handled:
  - case: Cards with no mana cost
    handling: CMC of 0, sorted first within type group
  
  - case: Double-faced cards with different costs on each face
    handling: Use front face mana cost and color identity of whole card
  
  - case: Hybrid mana cards
    handling: Color identity includes all colors in hybrid costs
  
  - case: Colorless cards that produce colored mana
    handling: Still treated as colorless unless colors appear in mana cost

Performance Characteristics:
  - Time Complexity: O(n log n) due to sorting operations
  - Space Complexity: O(n) for metadata objects during sorting
  - Typical Runtime: <10ms for typical cube size (360-720 cards)
  - Max Input Size Tested: All Magic cards (~25,000) in ~50ms

Dependencies:
  - lodash.sortBy for stable multi-key sorting
  - utils/mtg/cardTypes.ts for type classification
  - utils/mtg/colorGroup.ts for color group determination

Test Coverage:
  - Unit Tests: Not explicitly present in codebase
  - Integration Tests: Validated through example scripts
  - Test Location: Tested via scripts/examples/

Why This Matters:
  This algorithm is fundamental to making MTG data analysis tools feel natural to Magic players. The specific ordering matches what players expect from deck builders, cube lists, and collection management tools. Getting this wrong would make the toolkit feel foreign to its target audience.
```

```yaml
Algorithm Name: Card Spell Checking with Fuzzy Matching
Location: utils/mtg/spellCheckCardNames.ts
Lines of Code: ~50
Complexity: Medium
Priority: MUST PRESERVE

Purpose:
  Validates card names against the complete Scryfall database and provides intelligent suggestions for misspelled or partially-typed names. Essential for data import scripts where card names might come from user input or imperfect data sources.

Inputs:
  - namesToValidate: string[] (array of potential card names)
  - skipValidation: function (optional callback to skip certain names)
  - scryfallDatabase: Complete oracle cards database

Outputs:
  - validationResults: Array of objects with { name, valid: boolean, suggestion?: string, skipped?: boolean }

Algorithm Logic:
  1. Fetch complete card names database from Scryfall bulk data
  2. Handle special card name formats:
     a. Double-faced cards: "Front Name // Back Name"
     b. Adventure cards: Use only the main card name (not adventure name)
     c. Normal cards: Use name as-is
  3. For each input name:
     a. Check if it exists exactly in the database
     b. If not found, use Fuse.js fuzzy matching to find closest match
     c. Return suggestion with confidence score
  4. Deduplicate card names to handle multiple printings

Edge Cases Handled:
  - case: Double-faced transform cards
    handling: Concatenate both face names with " // " separator
  
  - case: Adventure cards
    handling: Use only the creature name, ignore adventure name
  
  - case: Modal double-faced cards
    handling: Same as transform cards with " // " separator
  
  - case: Names with special punctuation or diacritics
    handling: Fuzzy matching handles minor variations
  
  - case: Completely invalid input
    handling: Returns best guess suggestion or no suggestion if too dissimilar

Performance Characteristics:
  - Time Complexity: O(n * m) where n = names to validate, m = fuzzy search complexity
  - Space Complexity: O(k) where k = total unique card names (~25,000)
  - Typical Runtime: ~100ms for small lists, ~1s for hundreds of names
  - Bulk Data Load: One-time ~3s cost to load complete database

Dependencies:
  - Fuse.js for fuzzy string matching with configurable similarity scoring
  - lodash.uniq for deduplication of card names
  - utils/scryfall/bulkData.ts for complete card database

Why This Matters:
  Card name validation is critical for data import workflows. Magic has >25,000 unique card names with complex naming conventions, special characters, and multiple languages. Manual validation would be impossible, and exact string matching fails too often with user input.
```

```yaml
Algorithm Name: First Printing Deduplication
Location: utils/mtg/uniqueFirstPrintings.ts
Lines of Code: ~25
Complexity: Simple
Priority: CAN REFACTOR

Purpose:
  Filters a complete Magic card database to show only the first printing of each unique card, removing reprints, tokens, art variants, and promotional materials. Essential for historical analysis and avoiding duplicate counting in statistics.

Inputs:
  - cards: scryfall.Card[] (complete Scryfall database or large card set)

Outputs:
  - uniqueCards: scryfall.Card[] (one card per unique name, first printing only)

Algorithm Logic:
  1. Filter out non-game cards:
     a. Exclude reprints (reprint: true)
     b. Exclude art series cards
     c. Exclude all token types
     d. Exclude promotional/memorabilia items
  2. Use lodash.uniqBy with card name as key to keep first occurrence
  3. Return deduplicated array

Edge Cases Handled:
  - case: Same name, different functions (e.g., creature vs token)
    handling: Filters preserve game cards, exclude tokens
  
  - case: Cards with same name across different sets
    handling: Keeps whichever appears first in input array
  
  - case: Art series and promotional variants
    handling: Explicitly excluded by layout and set_type filters

Performance Characteristics:
  - Time Complexity: O(n) single pass with hash table deduplication
  - Space Complexity: O(k) where k = unique card names
  - Typical Runtime: ~50ms for complete Magic database
  - Memory Usage: Minimal overhead for filtering

Why This Matters:
  Magic reprints the same card in multiple sets, creating thousands of duplicate entries. For analysis of card design, power level, or historical trends, you want one instance per unique card design, not one per printing. Without deduplication, statistics would be heavily skewed by popular cards with many reprints.
```

```yaml
Algorithm Name: Card List Comparison
Location: utils/mtg/compareLists.ts
Lines of Code: ~15
Complexity: Simple
Priority: CAN REFACTOR

Purpose:
  Compares two lists of card names to find shared cards and cards unique to each list. Used for cube comparison, deck analysis, and collection management workflows.

Inputs:
  - listA: string[] (first list of card names)
  - listB: string[] (second list of card names)

Outputs:
  - comparisonResult: { shared: string[], uniqueToA: string[], uniqueToB: string[] }

Algorithm Logic:
  1. Use lodash set operations for comparison:
     a. intersection(listA, listB) for shared cards
     b. difference(listA, listB) for cards only in A
     c. difference(listB, listA) for cards only in B
  2. Return structured result object

Performance Characteristics:
  - Time Complexity: O(n + m) where n, m are list lengths
  - Space Complexity: O(n + m) for result arrays
  - Typical Runtime: <1ms for cube-sized lists
  
Why This Matters:
  Cube and deck comparison is a fundamental workflow for Magic players. This provides the building block for analyzing differences between cube versions, finding overlaps between decks, or comparing collections.
```

### 4.2 Validation Rules

```yaml
Data Validation:
  Model: Card Names
  Rules:
    - field: name
      rule: "Must exist in Scryfall database"
      validation: Exact string match against complete card names list
      error_handling: Provide fuzzy match suggestion if available
    
    - field: double_faced_names
      rule: "Must use ' // ' separator for transform cards"
      validation: Check format for cards with multiple faces
      error_handling: Suggest proper format with card face names

Business Rule Validation:
  - rule_name: Color Identity Consistency
    description: Card's color identity must include all mana symbols that appear on the card
    enforcement: Calculated field, validated against official Scryfall data
    
  - rule_name: Format Legality Logic
    description: Cards must be legal in format based on ban list and set inclusion
    enforcement: Inherited from Scryfall's official format data
    
  - rule_name: Set Membership Validation
    description: Cards must belong to valid Magic sets with proper set codes
    enforcement: Validated against Scryfall's sets API data
```

### 4.3 Workflow & State Machines

```yaml
Workflow Name: Card Data Enrichment Process
Entities Involved: Card Names, Scryfall API, Cache, Enriched Cards

States:
  - state: RAW_NAMES
    description: Starting with list of card name strings
    entry_condition: User provides card list or script generates names
    permissions: Read-only input data
  
  - state: NAME_VALIDATION
    description: Validating names against Scryfall database
    processing: Spell check against complete card database
    permissions: Can suggest corrections, flag invalid names
  
  - state: CARD_LOOKUP
    description: Fetching full card data for valid names
    processing: Batch lookup from Scryfall API or bulk data
    permissions: Read from cache or API, write to cache
  
  - state: DATA_ENRICHMENT
    description: Adding computed fields and MTG-specific analysis
    processing: Calculate derived properties like color groups, type analysis
    permissions: Generate computed fields, maintain data relationships
  
  - state: READY_FOR_ANALYSIS
    description: Complete card objects ready for domain analysis
    exit_condition: All cards have full data and computed properties
    permissions: Read-only for analysis scripts

Transitions:
  - from: RAW_NAMES
    to: NAME_VALIDATION
    trigger: spell_check_card_names() function call
    condition: Non-empty array of name strings
    
  - from: NAME_VALIDATION
    to: CARD_LOOKUP
    trigger: Valid names identified or user accepts suggestions
    condition: At least some names validate successfully
    
  - from: CARD_LOOKUP
    to: DATA_ENRICHMENT
    trigger: Scryfall data fetch completes
    condition: API requests successful or cache hit
    
  - from: DATA_ENRICHMENT
    to: READY_FOR_ANALYSIS
    trigger: Computed fields calculation complete
    condition: All derived properties calculated

Permissions by State:
  - state: RAW_NAMES
    can_view: Input validation scripts
    can_edit: Data cleaning functions
    can_delete: Input sanitization
  
  - state: NAME_VALIDATION
    can_view: Validation results with suggestions
    can_edit: Manual name corrections
    can_delete: Invalid names with no good suggestions
  
  - state: READY_FOR_ANALYSIS
    can_view: All analysis scripts
    can_edit: None (immutable once enriched)
    can_delete: Cache invalidation only

Terminal States:
  - READY_FOR_ANALYSIS: Cards fully enriched and ready for analysis
  - VALIDATION_FAILED: Too many invalid names, manual intervention needed
```

---

## Section 5: External Integrations [IMPORTANT]

### 5.1 Third-Party APIs

```yaml
Service Name: Scryfall API
Purpose: Complete Magic: The Gathering card database and search functionality
Criticality: CRITICAL - Core data source, toolkit cannot function without it

Integration Details:
  - API Type: REST
  - Base URL: https://api.scryfall.com
  - Authentication: None (public API)
  - Credentials Storage: None required

Endpoints Used:
  - endpoint: GET /cards/search
    purpose: Complex card queries with filtering and sorting
    frequency: On-demand during analysis scripts
    rate_limit: ~100-175 requests per second
  
  - endpoint: GET /cards/named
    purpose: Fetch specific card by name (exact or fuzzy match)
    frequency: Individual card lookups during enrichment
    rate_limit: Same global limit
  
  - endpoint: GET /bulk-data/{type}
    purpose: Download complete card database for offline analysis
    frequency: Daily (cached locally)
    rate_limit: No limits on bulk downloads

Data Flow:
  - direction: INBOUND - fetch card data
  - data_type: Card metadata, prices, legalities, images
  - frequency: Bulk download daily, searches as needed
  - volume: ~50MB bulk data daily, 100s of search queries per analysis

Error Handling:
  - network_failure: Retry with exponential backoff (3 attempts)
  - rate_limit_hit: Client-side throttling to stay under limits
  - invalid_response: Log error and fallback to cached data
  - service_down: Use cached bulk data, degrade gracefully

Caching Strategy:
  - cached: YES
  - cache_location: Local .cache directory
  - ttl: 24 hours for bulk data, session-based for searches
  - cache_key_pattern: bulk-data-{type}-{date}, search-{query-hash}

Dependencies:
  - data_dependency: Toolkit cannot function without Scryfall data
  - feature_dependency: All card analysis depends on this integration

Tribal Knowledge:
  - Rate limits are undocumented but approximately 100-175 req/sec
  - Bulk data endpoints are much more generous than search endpoints
  - Including User-Agent header is recommended for good citizenship
  - Some card names have complex layouts requiring special handling
```

```yaml
Service Name: Commander Spellbook (Google Sheets)
Purpose: Curated database of Magic combo interactions for Commander format
Criticality: IMPORTANT - Enables combo analysis features

Integration Details:
  - API Type: Google Sheets CSV export
  - Base URL: https://docs.google.com/spreadsheets
  - Authentication: None (publicly shared sheet)
  - Credentials Storage: Sheet ID in configuration

Endpoints Used:
  - endpoint: GET /spreadsheets/{id}/gviz/tq?tqx=out:csv
    purpose: Download complete combo database as CSV
    frequency: On-demand when combo analysis is needed
    rate_limit: Google Sheets limits (generous for reasonable use)

Data Flow:
  - direction: INBOUND - fetch combo data
  - data_type: Combo definitions with card names, steps, results
  - frequency: Occasional (when running combo analysis scripts)
  - volume: ~1-5MB CSV file containing thousands of combos

Error Handling:
  - network_failure: Retry download, use cached version
  - sheet_unavailable: Fallback to last successful cache
  - format_changes: Robust CSV parsing with error tolerance
  - service_down: Graceful degradation with cached combos

Caching Strategy:
  - cached: YES
  - cache_location: Local .cache directory  
  - ttl: Manual refresh (combos don't change frequently)
  - cache_key_pattern: commander-spellbook-{timestamp}

Dependencies:
  - data_dependency: Only affects combo analysis features
  - feature_dependency: Commander combo scripts depend on this data

Tribal Knowledge:
  - Sheet format is community-maintained, could change
  - Combo steps are human-written, not machine-parseable
  - Results descriptions use consistent but informal language
  - Card names may need spell-checking against Scryfall
```

```yaml
Service Name: Cube Cobra
Purpose: Cube list management platform with public APIs for cube data
Criticality: IMPORTANT - Enables cube analysis workflows

Integration Details:
  - API Type: REST (unofficial/undocumented)
  - Base URL: https://cubecobra.com
  - Authentication: None (public cube data)
  - Credentials Storage: None required

Endpoints Used:
  - endpoint: GET /cube/api/cubelist/{cubeId}
    purpose: Simple text list of cards in a cube
    frequency: On-demand for cube analysis
    rate_limit: Unknown (reasonable use expected)
  
  - endpoint: GET /cube/api/cubeJSON/{cubeId}
    purpose: Detailed JSON with cube metadata and card details
    frequency: On-demand for detailed cube analysis
    rate_limit: Unknown (reasonable use expected)

Data Flow:
  - direction: INBOUND - fetch cube compositions
  - data_type: Card lists, cube metadata, owner preferences
  - frequency: Occasional (when analyzing specific cubes)
  - volume: Small (few KB per cube)

Error Handling:
  - network_failure: Retry with backoff
  - cube_not_found: Handle gracefully with error message
  - private_cube: Detect and report access restrictions
  - format_changes: Flexible parsing of cube data

Caching Strategy:
  - cached: YES (during analysis session)
  - cache_location: Memory cache for session
  - ttl: Session-based (cubes change frequently)
  - cache_key_pattern: cube-{cubeId}-{timestamp}

Dependencies:
  - data_dependency: Only affects cube-specific analysis
  - feature_dependency: Cube comparison and analysis scripts

Tribal Knowledge:
  - API is unofficial and could change without notice
  - Some cubes are private and return 404 errors
  - Card names may include set preferences in [SET] format
  - Cube data quality varies by owner diligence
```

### 5.2 Authentication Providers

```yaml
Provider: None
Why Chosen: All integrated services provide public APIs without authentication requirements

OAuth Configuration: N/A - No OAuth flows implemented
User Data Mapping: N/A - No user accounts or personal data
Token Management: N/A - No authentication tokens used
```

### 5.3 Other External Services

```yaml
Service Type: CDN / Data Hosting
Service Name: Scryfall's image CDN
Purpose: Card images for analysis and display (when needed)
Configuration: Image URLs provided in card data
Criticality: NICE-TO-HAVE - Not currently used but available
Fallback: Skip image-based analysis if CDN unavailable

Service Type: File Processing
Service Name: Local file system
Purpose: Cache storage, input/output file processing
Configuration: .cache directory, local file paths
Criticality: IMPORTANT - Enables offline analysis and performance
Fallback: Disable caching, fetch fresh data each time (slower)

Service Type: Mathematical / Statistical
Service Name: lodash utility library
Purpose: Data transformation, sorting, statistical functions
Configuration: Imported as npm dependency
Criticality: IMPORTANT - Used throughout analysis algorithms
Fallback: Would require rewriting many utility functions
```

---

## Section 6: Frontend Architecture [IMPORTANT - if applicable]

```yaml
Framework: None (CLI-based toolkit)
Frontend Type: Command-line scripts and utilities

User Interface:
  - interaction_model: Command-line execution with tsx runtime
  - input_methods: Script arguments, file paths, interactive prompts (prompt library)
  - output_methods: Console logging, file generation (CSV, JSON)
  - user_experience: Developer/analyst workflow optimization

Script Architecture:
  - pattern: Individual TypeScript files with main() functions
  - organization: scripts/ directory with examples/ subdirectory
  - reusability: Shared utilities in utils/ directory
  - execution: tsx runtime for TypeScript execution without compilation

Design System: N/A (text-based output)
Styling: N/A (console output only)
Component Library: N/A (utility functions, not UI components)

Critical Frontend Components:
  - Component: Script Template System
    Location: scripts/template.ts
    Purpose: Standardized starting point for new analysis scripts
    
  - Component: Interactive Prompts
    Location: Used in various example scripts
    Purpose: User input collection during script execution
    Dependencies: prompt npm package
    
  - Component: Logging Utilities  
    Location: utils/log.ts
    Purpose: Consistent output formatting and progress reporting
```

---

## Section 7: Testing & Quality [IMPORTANT]

```yaml
Unit Tests:
  - framework: None explicitly configured
  - coverage: Unknown - no formal test suite
  - location: No dedicated test directory
  - critical_coverage: Algorithms are validated through example scripts

Integration Tests:
  - framework: Example scripts serve as integration tests
  - coverage: Real-world workflows tested through examples
  - location: scripts/examples/ directory (20+ example scripts)

End-to-End Tests:
  - framework: Manual execution of example scripts
  - coverage: Complete workflows from data fetch to analysis output
  - location: All example scripts test end-to-end functionality

Test Data:
  - fixtures: Real Magic card data from Scryfall
  - mocking_strategy: No mocking - uses real APIs with caching
  - test_datasets: Example cube lists, card names, combo data

Testing Framework:
  - framework: No formal testing framework
  - validation: TypeScript compiler + ESLint for static analysis
  - quality_assurance: Real-world usage in Lucky Paper projects provides validation

Quality Measures:
  - code_quality: ESLint with TypeScript rules enforced
  - formatting: Prettier for consistent code style
  - type_safety: TypeScript with strict mode provides compile-time validation
  - documentation: Comprehensive README and inline code comments
```

---

## Section 8: Performance Characteristics [IMPORTANT]

```yaml
Script Performance:
  - typical_script_runtime: 1-30 seconds depending on data requirements
  - bulk_data_download: 10-30 seconds first run, instant subsequent runs
  - search_operations: 200-500ms per Scryfall API call
  - local_analysis: Near-instant once data is cached

Data Processing Performance:
  - card_sorting: <10ms for typical cube size (360-720 cards)
  - spell_checking: ~100ms for small lists, ~1s for hundreds of names
  - combo_enrichment: 1-5 seconds depending on combo count
  - bulk_deduplication: ~50ms for complete Magic database (~25K cards)

Memory Usage:
  - complete_card_database: ~200MB uncompressed in memory
  - typical_script: 10-50MB for normal analysis workflows
  - peak_usage: Limited by available system memory for bulk operations

Caching Performance:
  - cache_hit: Near-instant (file system read)
  - cache_miss: API request time + cache write overhead
  - cache_invalidation: Manual or 24-hour TTL for bulk data

Scalability Characteristics:
  - current_scale: Designed for research and analysis, not production services
  - max_dataset_size: Limited by available memory (tested with full Magic database)
  - concurrent_usage: Single-user scripts (no concurrency requirements)
  - bottlenecks: API rate limits for real-time analysis, memory for very large datasets
```

---

## Section 9: Security & Compliance [IMPORTANT]

```yaml
Authentication Security:
  - password_storage: N/A - No authentication system
  - session_management: N/A - Stateless scripts
  - token_rotation: N/A - No tokens used

Authorization Security:
  - permission_checks: File system permissions for cache and output
  - access_control: Local file system access only
  - data_exposure: All accessed data is public (Scryfall, public cubes)

Data Security:
  - encryption_at_rest: No sensitive data stored
  - encryption_in_transit: HTTPS for all API calls
  - sensitive_data: None - all Magic card data is public
  - pii_handling: No personal information processed

Input Validation:
  - api_injection: No user-controlled API parameters (queries are script-generated)
  - file_validation: Basic file existence and format checking
  - data_sanitization: Card name validation against known database
  - script_injection: TypeScript prevents most injection attacks

API Security:
  - rate_limiting: Client-side throttling to respect API limits
  - api_keys: None required (public APIs only)
  - cors_policy: N/A (server-side tool, not web-based)

Security Considerations:
  - external_dependencies: npm packages could introduce vulnerabilities
  - file_system_access: Scripts have local file system access
  - network_requests: Makes HTTP requests to third-party APIs
  - code_execution: Executes arbitrary TypeScript/JavaScript code
```

---

## Section 10: Deployment & Operations [IMPORTANT]

```yaml
Deployment Model:
  - deployment_type: Developer toolkit (local installation)
  - environment: Local development machine
  - runtime: Node.js with tsx for TypeScript execution
  - dependencies: npm install for package management

Installation:
  - prerequisites: Node.js 16+, npm or yarn
  - install_command: npm install
  - configuration: No external configuration required
  - verification: Run example scripts to validate installation

Operations:
  - monitoring: No operational monitoring (development tool)
  - logging: Console output for script execution
  - error_tracking: TypeScript compiler and runtime errors
  - maintenance: npm audit for security updates

Data Operations:
  - backup_strategy: Git version control for scripts and utilities
  - cache_management: .cache directory with automatic cleanup
  - data_retention: Cached data expires after 24 hours
  - disaster_recovery: Re-clone repository and reinstall dependencies

Configuration Management:
  - config_files: package.json, tsconfig.json, .eslintrc
  - environment_variables: None used (all public APIs)
  - secrets_management: N/A (no secrets or credentials)
  - feature_flags: N/A (all features available)

Release Management:
  - versioning: Git tags for toolkit versions
  - deployment_process: Git clone, npm install, execute scripts
  - rollback_strategy: Git checkout to previous version
  - change_management: Version control history for all changes
```

---

## Section 11: Domain Knowledge & Tribal Knowledge [CRITICAL]

### 11.1 Domain Expertise Required

```yaml
Domain: Magic: The Gathering Collectible Card Game
Expertise Level: HIGH - Deep game knowledge required for meaningful analysis

Critical Domain Concepts:
  - concept: Color Identity in Commander
    importance: CRITICAL - Fundamental for deck legality analysis
    explanation: |
      Commander color identity is more complex than card colors:
      - Includes mana symbols in text boxes and abilities
      - Hybrid mana counts as both colors
      - Off-color activations count toward identity
      - Lands with mana symbols have color identity
    
  - concept: Card Name Variations and Layouts
    importance: HIGH - Essential for accurate card matching
    explanation: |
      Magic cards have complex naming conventions:
      - Double-faced cards: "CardName // OtherSide"
      - Adventure cards: "CardName // AdventureName"
      - Split cards: "Left // Right" 
      - Flip cards: Use original name only
      - Tokens and emblems: Not "real" cards for most analysis
    
  - concept: Legality and Format Restrictions
    importance: HIGH - Required for format-specific analysis
    explanation: |
      Different Magic formats have different card pools:
      - Standard: ~2 years of recent sets
      - Pioneer: Return to Ravnica forward
      - Modern: 8th Edition/Mirrodin forward
      - Legacy: All cards except banned list
      - Vintage: All cards, some restricted
      - Commander: Singleton format with color identity rules
    
  - concept: Set Codes and Printing Variations
    importance: MEDIUM - Important for collection analysis
    explanation: |
      Each Magic set has a unique 3-4 letter code:
      - First printings are often most valuable
      - Promotional printings (promo codes) are special
      - Masterpiece series and special releases have unique codes
      - Reserved List cards cannot be reprinted

Algorithmic Domain Knowledge:
  - algorithm: Magic Color Sorting (utils/mtg/magicSort.ts)
    complexity: MEDIUM
    domain_knowledge: |
      Colors are ordered White-Blue-Black-Red-Green (WUBRG)
      This ordering is fundamental to Magic's design philosophy
      Multi-color cards are sorted by total color count, then alphabetically
      Colorless comes last in sort order
      
  - algorithm: Card Name Spell Checking (utils/mtg/spellCheckCardNames.ts) 
    complexity: MEDIUM
    domain_knowledge: |
      Magic card names include many fantasy/invented words
      Apostrophes, hyphens, and special characters are common
      Adventure/DFC cards need special handling for "//" separator
      Some cards have multiple valid name formats
      
  - algorithm: First Printing Detection (utils/mtg/uniqueFirstPrintings.ts)
    complexity: LOW  
    domain_knowledge: |
      Tokens, art series, and promotional cards are usually excluded
      "First" means chronologically first legal printing
      Some sets are considered "supplemental" vs "main" sets
      Reserved List status affects reprint possibilities
```

### 11.2 Business Logic Domain Rules

```yaml
Rule Category: Deck Legality
Rule: Commander Color Identity
Implementation: Scattered throughout toolkit
Details: |
  Cards can only be included in decks if their color identity
  is a subset of the commander's color identity. This affects
  not just mana costs but any colored symbols anywhere on the card.

Rule Category: Card Equivalence  
Rule: Functional Reprints vs New Printings
Implementation: uniqueFirstPrintings.ts
Details: |
  Cards with identical game text but different art/flavor are
  considered the same card. Different printings of the same
  card are usually consolidated for gameplay analysis.

Rule Category: Format Construction
Rule: Singleton Formats
Implementation: Various deck analysis scripts
Details: |
  Commander and some cube formats allow only one copy of each card
  (except basic lands). This affects deck statistics and probability
  calculations significantly.
```

### 11.3 Data Interpretation Tribal Knowledge

```yaml
Scryfall API Quirks:
  - quirk: Card Names with Special Characters
    impact: HIGH
    explanation: |
      Some card names contain characters that need URL encoding
      Example: "Æther Flash" contains a ligature character
      The API handles this but local matching may need special care
      
  - quirk: Double-Faced Card Layouts
    impact: MEDIUM  
    explanation: |
      DFC cards return both faces in the API response
      The "name" field contains the front face only
      The "card_faces" array contains both sides
      Different analysis needs may want front face vs both faces
      
  - quirk: Multiverse IDs and Collectible Numbers
    impact: LOW
    explanation: |
      Older cards may have multiverse_id but no collector_number
      Very old cards may have neither
      Promotional cards have special collector number formats
      
Lucky Paper Context:
  - context: Cube Design Philosophy
    relevance: HIGH
    explanation: |
      Lucky Paper focuses on cube design and draft environment analysis
      This affects which statistics and metrics are most valuable
      Emphasis on draft archetypes, color balance, and power level
      
  - context: Community Integration
    relevance: MEDIUM
    explanation: |
      Tools are designed to integrate with broader Lucky Paper content
      Analysis results may be used in articles, videos, or cube reviews
      User experience optimized for content creation workflows
```

---

## Section 12: Migration Readiness Assessment [IMPORTANT]

```yaml
Current Architecture Sustainability:
  - maintainability: GOOD - Clean TypeScript codebase with clear separation
  - technical_debt: LOW - Recent project with modern practices
  - documentation: GOOD - Comprehensive README and inline comments
  - testing: MODERATE - Example scripts provide validation but no formal tests

External Dependencies Risk Assessment:
  - scryfall_api: 
    risk_level: MEDIUM
    mitigation: Bulk data downloads provide offline capability
    alternatives: MTGJson.com as backup data source
    
  - commander_spellbook:
    risk_level: HIGH
    mitigation: CSV caching provides temporary offline capability  
    alternatives: No direct alternative for combo data
    
  - cube_cobra:
    risk_level: MEDIUM
    mitigation: Session-based caching, graceful degradation
    alternatives: Manual cube list input as fallback

Technology Stack Modernization Needs:
  - typescript: CURRENT - Using modern TypeScript with strict mode
  - node_runtime: CURRENT - Compatible with current LTS versions  
  - npm_ecosystem: CURRENT - All dependencies are actively maintained
  - build_tooling: MINIMAL - tsx provides zero-config TypeScript execution

Migration Complexity Assessment:
  - database_migration: N/A - No persistent database
  - api_versioning: LOW - All external APIs are stable or cached
  - configuration_changes: MINIMAL - Very little configuration to migrate
  - data_format_changes: LOW - JSON/CSV formats are stable

Legacy System Integration:
  - current_integrations: None - standalone toolkit
  - integration_complexity: LOW - CLI tools are easy to integrate
  - api_compatibility: N/A - No exposed APIs to maintain
  - backward_compatibility: GOOD - Script interfaces are stable

Cloud Migration Readiness:
  - stateless_design: YES - Scripts are stateless and cacheable
  - horizontal_scaling: POSSIBLE - Could run multiple instances
  - containerization: EASY - Node.js containerizes well
  - serverless_compatibility: POSSIBLE - Individual scripts could be serverless functions
```

---

## Section 13: Documentation & Resources [IMPORTANT]

### 13.1 Technical Documentation

```yaml
Primary Documentation:
  - location: README.md (root level)
  - quality: EXCELLENT - Comprehensive installation and usage guide
  - coverage: Complete workflow from installation to advanced usage
  - maintenance: Updated with project (no staleness detected)

Code Documentation:
  - inline_comments: GOOD - Key algorithms and utilities documented
  - function_documentation: MODERATE - Most utilities have JSDoc comments
  - type_documentation: EXCELLENT - TypeScript provides inline type documentation
  - example_usage: EXCELLENT - 20+ example scripts demonstrate usage patterns

Architecture Documentation:
  - system_overview: GOOD - README explains toolkit structure and philosophy
  - data_flow: IMPLICIT - Can be inferred from example scripts
  - decision_rationale: LIMITED - Some design decisions explained in comments
  - integration_guides: MODERATE - API integration examples provided
```

### 13.2 Knowledge Resources

```yaml
Domain Knowledge Resources:
  - magic_rules: External - Official Magic rules and comprehensive rules document
  - scryfall_docs: External - Scryfall API documentation for data formats
  - lucky_paper_content: External - Lucky Paper articles provide context for use cases
  - community_knowledge: External - MTG community forums and wikis

Learning Resources:
  - onboarding: README provides clear getting-started guide
  - examples: scripts/examples/ directory with 20+ real-world examples
  - code_patterns: utils/ directory demonstrates reusable patterns
  - troubleshooting: Error messages and logging provide debugging guidance

External References:
  - scryfall_api: https://scryfall.com/docs/api - Primary data source documentation  
  - commander_spellbook: Community-maintained combo database
  - cube_cobra: Cube management platform (unofficial API usage)
  - typescript_docs: TypeScript language reference for development
```

### 13.3 Operational Resources

```yaml
Support Channels:
  - issue_tracking: GitHub Issues (if applicable)
  - community_support: Lucky Paper Discord/community channels
  - documentation_updates: Git commits and version control
  - knowledge_sharing: Example scripts serve as knowledge transfer

Maintenance Documentation:
  - update_procedures: npm update for dependency management
  - troubleshooting: Error handling in scripts provides guidance
  - monitoring: Console output provides operational visibility
  - backup_procedures: Git version control serves as backup system

Development Resources:
  - development_setup: Clear instructions in README
  - contribution_guidelines: TypeScript and ESLint standards enforced
  - testing_procedures: Example scripts provide validation workflow
  - release_process: Git-based versioning and distribution
```

---

## Analysis Complete

This MTG Scripting Toolkit analysis provides comprehensive technical documentation across all 13 sections of the analysis template. The toolkit is a well-designed, domain-specific tool for Magic: The Gathering data analysis with strong integration to the Scryfall API ecosystem and clear focus on cube design and draft format analysis workflows used by Lucky Paper content creation.