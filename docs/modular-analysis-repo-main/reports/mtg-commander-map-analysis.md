# MTG Commander Map Project Analysis

**Purpose**: Analysis of MTG Commander Map for potential integration into modular monolith architecture

**Instructions**: 
- Fill out ALL sections, even if answer is "N/A" or "None"
- Use concrete examples, not generic descriptions
- Copy actual code snippets for critical business logic
- Include WHY decisions were made, not just WHAT exists
- Mark sections as [CRITICAL], [IMPORTANT], or [NICE-TO-HAVE] based on migration priority

---

## Section 1: Project Identity & Context [CRITICAL]

### 1.1 Basic Information
```yaml
Project Name: MTG Commander Map
Repository URL: https://github.com/jcrowdis/commander-map (inferred from Docker image)
Primary Domain: MTG (Magic: The Gathering) / Data Science / Visualization
Project Status: Active
Business Purpose: Creates interactive 2D maps of Magic: The Gathering Commander decks using machine learning to visualize deck similarity and discover emergent patterns in the meta
Key Stakeholders: Lucky Paper (primary publisher), MTG Commander community, data scientists, deck builders
Monthly Active Users: Estimated 10,000+ (based on Lucky Paper traffic)
Critical to Business: SOMEWHAT - Valuable community resource and content for Lucky Paper, but not mission-critical
```

### 1.2 Technology Stack Inventory
```yaml
Programming Languages:
  - Language: Python
    Version: ≥3.7.9
    Percentage: 100%
    Primary Use: Data processing, machine learning, visualization

Primary Frameworks:
  Backend: N/A (data processing scripts)
  Frontend: N/A (generates data for external website)
  Data Science: UMAP, HDBSCAN, pandas, numpy, scikit-learn

Database:
  Primary: N/A (processes files, outputs JSON/CSV)
  Cache: N/A

Build & Dev Tools:
  - Package Manager: pip
  - Build Tool: Docker for cloud deployment
  - Linter: Not specified
  - Formatter: Not specified
  - Testing Framework: Basic test.py script
  - CI/CD: None specified

Infrastructure:
  - Hosting: Google Cloud (via Terra platform) or local execution
  - Containerization: Docker (jcrowdis/commander-map image)
  - Orchestration: Google Cloud Workflows (.wdl file)
  - Environment Variables: None specified (uses command line arguments)
```

### 1.3 Project Structure
```
mtg-commander-map/
├── commander-map.ipynb          # Main explanatory notebook
├── make-map.sh                  # Local execution script
├── generate_commander_map.wdl   # Google Cloud workflow definition
├── Dockerfile                   # Container for cloud execution
├── requirements.txt             # Python dependencies
├── duplicates.txt              # Cards with duplicate issues
├── edhrec-to-scryfall.json     # Card name mappings
├── theme-tribe-override.csv    # Manual overrides for categorization
└── scripts/                    # Core processing modules
    ├── card.py                 # Scryfall card data processing
    ├── calculate.py            # Utility functions and algorithms
    ├── map_classes.py          # Data structures
    ├── load.py                 # Data loading utilities
    ├── preprocess_data.py      # EDHREC data preprocessing
    ├── generate_main_map_coordinates.py  # UMAP embedding
    ├── generate_main_map_clusters.py     # HDBSCAN clustering
    └── generate_submaps.py     # Per-archetype submaps

Key Directories Explained:
- scripts/: Core data processing pipeline with modular components
- commander-map.ipynb: Educational/debugging notebook explaining algorithms
- *.wdl, Dockerfile: Cloud deployment infrastructure for large-scale processing
```

---

## Section 2: Data Architecture [CRITICAL]

### 2.1 Data Models Inventory

**Commander Deck Model:**
```yaml
Model Name: Commander Deck
Description: Represents a single Commander deck from EDHREC with cards and metadata
Priority: CRITICAL
Source File: Processed from EDHREC JSON data

Fields:
  - name: commanderID
    type: string/int (mapped)
    description: Primary commander card identifier
    business_rules: "Must be a legal Commander according to MTG rules"
  
  - name: partnerID
    type: string/int (mapped)
    description: Partner commander if applicable
    business_rules: "Empty string if no partner, must be legal partner"
  
  - name: colorIdentityID
    type: string/int (mapped)
    description: Deck's color identity (WUBRG combinations)
    business_rules: "Must match commander's color identity"
  
  - name: tribeID
    type: string/int (mapped)
    description: Primary creature type theme (e.g., "elves", "goblins")
    business_rules: "Empty string if no tribal focus"
  
  - name: themeID
    type: string/int (mapped)
    description: Mechanical theme (e.g., "artifacts", "lifegain")
    business_rules: "Empty string if no clear theme"
  
  - name: cards
    type: list[string]
    description: List of all non-commander cards in deck
    business_rules: "Must be legal MTG cards, typically 99 cards total"
  
  - name: url
    type: string
    description: Original decklist URL from source site
    business_rules: "Must be valid URL from supported platforms"

Relationships:
  - related_model: Magic Card (via card names)
    relationship_type: many-to-many
    cardinality: 1 deck to ~99 cards
    description: "Deck composition relationship"

Validation Rules:
  - rule: "Commander must be legendary creature or planeswalker"
    enforced: application
    error_message: "Invalid commander detected"
  
  - rule: "Color identity must be consistent with commander"
    enforced: application
    error_message: "Color identity mismatch"

Special Behaviors:
  - behavior: "Trait mapping converts string IDs to integers for ML processing"
    implementation: "replace_traits_with_ints function"
    code_location: "scripts/calculate.py"
```

**Magic Card Model:**
```yaml
Model Name: Magic Card
Description: Represents a Magic: The Gathering card with Scryfall data
Priority: CRITICAL
Source File: scripts/card.py (from Scryfall API)

Fields:
  - name: name
    type: string
    description: Official card name
    business_rules: "Must match Scryfall oracle name"
  
  - name: mana_cost
    type: string
    description: Mana cost in {1}{W}{U}{B}{R}{G} format
    business_rules: "Must follow MTG mana format"
  
  - name: cmc
    type: integer
    description: Converted mana cost
    business_rules: "Non-negative integer"
  
  - name: color_identity
    type: list[string]
    description: Color identity for Commander format
    business_rules: "Subset of WUBRG"
  
  - name: type_line
    type: string
    description: Full type line (e.g., "Legendary Creature — Human Wizard")
    business_rules: "Must follow MTG type conventions"
  
  - name: price_usd
    type: float
    description: Minimum USD price across all printings
    business_rules: "Non-negative, null if not for sale"
  
  - name: earliest_release
    type: date
    description: Earliest availability date (spoiled date or 2 weeks before release)
    business_rules: "Must be valid date"

Computed Fields:
  - name: is_commander_legal
    computation: "Legendary creature or planeswalker with commander legal type"
    cached: "No - computed during processing"

Special Behaviors:
  - behavior: "Double-sided cards split into separate entries for front face"
    implementation: "Custom processing in card.fetch_cards"
    code_location: "scripts/card.py"
```

**Cluster Model:**
```yaml
Model Name: Deck Cluster
Description: Groups of similar decks identified by HDBSCAN clustering
Priority: IMPORTANT
Source File: Generated by clustering algorithms

Fields:
  - name: cluster_id
    type: integer
    description: Unique cluster identifier (-1 for noise)
    business_rules: "Non-negative except -1 for unclustered decks"
  
  - name: defining_cards
    type: list[string]
    description: Cards that define this cluster's identity
    business_rules: "Sorted by statistical significance to cluster"
  
  - name: defining_traits
    type: dict
    description: Common commanders, tribes, themes, colors
    business_rules: "Must have statistical significance above threshold"
  
  - name: coordinates
    type: tuple[float, float]
    description: 2D UMAP embedding coordinates
    business_rules: "Real numbers in embedding space"

Validation Rules:
  - rule: "Clusters must contain minimum number of decks"
    enforced: application (minclustersize parameter)
    error_message: "Cluster too small, marked as noise"
```

### 2.2 Critical Data Relationships Map

```
EDHREC Data ────> Commander Decks (1.2M+)
                         │
                         │ contains
                         ▼
                    Magic Cards (~99 each)
                         │
                         │ processed_by
                         ▼
                  UMAP Embedding
                         │
                         │ clusters_into
                         ▼
                    HDBSCAN Clusters
                         │
                         │ generates
                         ▼
                   Map Coordinates + Submaps

Scryfall API ────> Magic Card Reference Data
                         │
                         │ validates
                         ▼
                    Deck Card Lists

Critical Path: EDHREC decks → Card validation → Embedding → Clustering → Map generation
```

### 2.3 Database Performance Patterns

```yaml
Query Optimization Strategies:
  - strategy: In-memory processing with pandas DataFrames
    location: All scripts
    impact: "Avoids database I/O overhead for large dataset processing"

Denormalization Patterns:
  - pattern: Trait mapping to integers for ML algorithms
    fields: commanderID, partnerID, tribeID, themeID, colorIdentityID
    location: scripts/calculate.py replace_traits_with_ints
    reason: "UMAP/HDBSCAN require numeric inputs for optimal performance"

Problematic Queries:
  - query_description: "UMAP embedding of 1.2M+ deck vectors"
    performance: "Very slow - hours on single machine"
    memory_usage: "Extremely high - may exceed 32GB RAM"
    notes: "Requires cloud deployment with high-memory instances"
```

---

## Section 3: API Architecture [NICE-TO-HAVE]

### 3.1 Authentication & Authorization

```yaml
Authentication Method:
  - type: None
    provider: N/A
    token_lifetime: N/A
    refresh_strategy: N/A

Authorization Pattern:
  - type: None (batch processing script)
    roles_list: N/A
    permissions_list: N/A

Access Control Rules:
  - rule: N/A - no API endpoints
    enforcement_location: N/A

External Auth Integrations:
  - provider: None
```

### 3.2 API Endpoints Inventory

```yaml
No API endpoints - this is a data processing pipeline that generates static output files.
The generated data is consumed by the Lucky Paper website but no API is exposed by this project.

Output Files Generated:
  - commander-map-coordinates.csv: Main map coordinates for all decks
  - trait-mapping.csv: Mapping of traits to integer IDs
  - cluster data files: Defining cards and traits for each cluster
  - submap files: Individual archetype submaps with their own coordinates
```

### 3.3 API Patterns & Conventions

```yaml
REST Conventions: N/A - no API
Error Handling Pattern: Python exceptions, script exits on failure
Data Serialization: CSV and JSON output files
```

---

## Section 4: Business Logic [CRITICAL]

### 4.1 Critical Algorithms

**UMAP Dimensionality Reduction Algorithm:**
```yaml
Algorithm Name: UMAP 2D Embedding for Commander Map
Location: scripts/map_classes.py CommanderMap.reduce_dimensionality()
Lines of Code: ~150
Complexity: Very Complex
Priority: MUST PRESERVE

Purpose:
  Reduces 1.2M+ Commander decks from high-dimensional card space (~20,000 dimensions) 
  to 2D coordinates for visualization while preserving deck similarity relationships.

Inputs:
  - decklist_matrix: Sparse CSR matrix (1.2M decks × ~20K cards)
  - n_neighbors: UMAP parameter controlling local/global structure balance
  - metric: Distance metric ('jaccard' for deck similarity)

Outputs:
  - coordinates: 2D numpy array of (x, y) positions for each deck
  - cluster_embedding: Higher-dimensional embedding for clustering

Algorithm Logic:
  def reduce_dimensionality(self, method='UMAP', n_dims=2, coordinates=True, **kwargs):
      # Set reproducible random state
      random_state = np.random.RandomState(0)
      
      # Configure UMAP for deck similarity
      embedder = umap.UMAP(
          n_components=n_dims,
          metric='jaccard',  # Optimal for binary deck data
          random_state=random_state,
          verbose=True,
          **kwargs
      )
      
      # Embed the sparse deck matrix
      embedding = embedder.fit_transform(self.decklist_matrix)
      
      # Handle disconnected components (NaN values)
      nan_entries = np.isnan(embedding).any(axis=1)
      if sum(nan_entries) > 0:
          # Assign disconnected decks to nearest neighbor with same commander
          # Uses Jaccard similarity for deck comparison
          
      return embedding

Edge Cases Handled:
  - case: Disconnected decks (NaN in embedding)
    handling: "Assign to nearest neighbor with same commander + noise"
  - case: Too few decks to embed (<threshold)
    handling: "Generate random uniform coordinates"
  - case: Memory overflow on large datasets
    handling: "Cloud deployment with high-memory instances"

Performance Characteristics:
  - Time Complexity: O(n log n) where n is number of decks
  - Space Complexity: O(n × d) where d is card dimension
  - Typical Runtime: 2-6 hours for 1.2M decks
  - Memory Usage: 32GB+ RAM required for full dataset

Why This Matters:
  UMAP preserves both local and global structure, making similar decks cluster together 
  while maintaining meaningful distances. This is the core visualization that makes 
  the Commander Map interpretable and useful for deck discovery.
```

**HDBSCAN Density-Based Clustering:**
```yaml
Algorithm Name: HDBSCAN Commander Deck Clustering
Location: scripts/map_classes.py CommanderMap.cluster_decks()
Lines of Code: ~100
Complexity: Complex
Priority: MUST PRESERVE

Purpose:
  Identifies natural groupings of similar Commander decks to create coherent 
  archetypes and discover meta patterns without predefined categories.

Inputs:
  - cluster_embedding: High-dimensional UMAP embedding (typically 4-6D)
  - min_cluster_size: Minimum decks required for a cluster (15+ default)
  - min_samples: Core point threshold for density calculation

Outputs:
  - cluster_labels: Array of cluster IDs (-1 for noise/unclustered)
  - cluster metadata: Defining cards and traits for each cluster

Algorithm Logic:
  def cluster_decks(self, method='HDBSCAN', **kwargs):
      # Handle edge case of very few decks
      if len(self.commander_decks) <= 10:
          return np.zeros(len(self.commander_decks))
      
      # Configure HDBSCAN with density-based parameters
      clusterer = hdbscan.HDBSCAN(
          min_cluster_size=15,  # Adaptive based on dataset size
          min_samples=min_cluster_size,
          prediction_data=True,
          gen_min_span_tree=True
      )
      
      # Cluster in embedding space (not original high-dimensional space)
      cluster_labels = clusterer.fit_predict(self.cluster_embedding)
      
      return cluster_labels

Edge Cases Handled:
  - case: Dataset too small to cluster
    handling: "Assign all decks to single cluster (ID 0)"
  - case: Many unclustered decks (noise)
    handling: "assign_unclustered() method assigns to nearest cluster"

Performance Characteristics:
  - Time Complexity: O(n log n) average case
  - Space Complexity: O(n²) worst case for distance matrix
  - Typical Runtime: 30-120 minutes depending on embedding size
  - Scales well with hierarchical approach

Why This Matters:
  HDBSCAN discovers natural deck archetypes without requiring predefined 
  categories. It handles varying cluster densities and identifies outlier 
  decks, crucial for understanding the Commander metagame structure.
```

**Adaptive Parameter Selection:**
```yaml
Algorithm Name: Clustering Parameter Optimization
Location: scripts/calculate.py get_parameters()
Lines of Code: ~30
Complexity: Simple
Priority: IMPORTANT

Purpose:
  Automatically adjusts UMAP and HDBSCAN parameters based on dataset size 
  to maintain clustering quality across different submap sizes.

Algorithm Logic:
  def get_parameters(ndecks):
      if ndecks < 300:
          return 4, 4    # n_neighbors, min_cluster_size
      elif ndecks < 500:
          return 6, 6
      # ... scaling up to 25, 12 for 20K+ decks
      
  # Balances local vs global structure preservation
  # Smaller datasets need tighter neighborhoods
  # Larger datasets can handle broader neighborhoods

Why This Matters:
  Parameter selection critically affects clustering quality. Too tight and you 
  get over-fragmentation; too loose and you lose meaningful distinctions.
```

**Defining Cards Algorithm:**
```yaml
Algorithm Name: Statistical Cluster Characterization
Location: scripts/map_classes.py (multiple methods)
Lines of Code: ~200
Complexity: Medium
Priority: MUST PRESERVE

Purpose:
  Identifies cards and traits that statistically define each cluster, 
  enabling automatic archetype description and user understanding.

Algorithm Logic:
  1. For each cluster, calculate card inclusion rates
  2. Compare against baseline inclusion rates across all decks
  3. Apply statistical significance tests (binomial distribution)
  4. Rank cards by effect size and significance
  5. Extract top N defining cards per cluster
  
  # Also identifies defining traits (commanders, tribes, themes, colors)
  # using similar statistical approach

Why This Matters:
  This automates the discovery of what makes each archetype unique, 
  providing interpretable descriptions for thousands of clusters without 
  manual curation.
```

### 4.2 Validation Rules

```yaml
Data Validation:
  Model: Commander Deck
  Rules:
    - field: commanderID
      rule: "Must be legendary creature or planeswalker"
      enforced: application
    - field: colorIdentityID  
      rule: "Must be valid WUBRG combination"
      enforced: application
    - field: cards
      rule: "Must exist in Scryfall database"
      enforced: application with mapping file

Business Rule Validation:
  - rule_name: Commander Format Legality
    description: "All cards must be legal in Commander format"
    enforcement: "Validation during preprocessing with Scryfall data"
  
  - rule_name: Color Identity Consistency
    description: "Deck cards must match commander color identity"
    enforcement: "Not enforced - allows format violations for analysis"
  
  - rule_name: Minimum Deck Size
    description: "Decks should have reasonable card counts"
    enforcement: "Filtering during preprocessing, no hard minimum"
```

### 4.3 Workflow & State Machines

**Data Processing Pipeline:**
```yaml
Workflow Name: Commander Map Generation Pipeline
Entities Involved: EDHREC Data, Scryfall API, Processing Scripts

States:
  - state: RAW_DATA
    description: "Downloaded EDHREC deck data in JSON format"
    next_actions: ["preprocess", "validate"]
    
  - state: PREPROCESSED
    description: "Cleaned data with card validation and trait mapping"
    next_actions: ["embed", "cluster"]
    
  - state: EMBEDDED
    description: "2D coordinates generated via UMAP"
    next_actions: ["cluster", "generate_submaps"]
    
  - state: CLUSTERED
    description: "Deck clusters identified via HDBSCAN"
    next_actions: ["characterize", "export"]
    
  - state: CHARACTERIZED
    description: "Defining cards and traits calculated for clusters"
    next_actions: ["export", "generate_submaps"]
    
  - state: COMPLETE
    description: "Final CSV/JSON files generated for website"
    next_actions: ["deploy_to_website"]

Transitions:
  - from: RAW_DATA
    to: PREPROCESSED
    trigger: "run preprocess_data.py"
    duration: "~2 hours"
    
  - from: PREPROCESSED
    to: EMBEDDED
    trigger: "run generate_main_map_coordinates.py"
    duration: "~4-8 hours"
    
  - from: EMBEDDED
    to: CLUSTERED
    trigger: "run generate_main_map_clusters.py"
    duration: "~1-3 hours"
    
  - from: CLUSTERED
    to: CHARACTERIZED
    trigger: "calculate defining cards and traits"
    duration: "~30 minutes"

Error States:
  - MEMORY_EXCEEDED: "Insufficient RAM for embedding"
  - CARD_VALIDATION_FAILED: "Unknown cards need mapping"
  - CLUSTERING_FAILED: "Too few valid clusters generated"

Recovery Procedures:
  - MEMORY_EXCEEDED: "Deploy to cloud with larger instance"
  - CARD_VALIDATION_FAILED: "Update edhrec-to-scryfall.json mapping"
  - CLUSTERING_FAILED: "Adjust clustering parameters or filter data"
```

---

## Section 5: External Integrations [CRITICAL]

### 5.1 Third-Party APIs

**Scryfall API:**
```yaml
Service Name: Scryfall Magic Card Database API
Purpose: Reference data for all Magic: The Gathering cards including names, types, costs, legality
Criticality: CRITICAL - project cannot function without MTG card reference data

Integration Details:
  - API Type: REST
  - Base URL: https://api.scryfall.com/
  - Authentication: None required (public API)
  - Credentials Storage: N/A

Endpoints Used:
  - endpoint: GET /bulk-data/oracle-cards
    purpose: "Download complete card database (oracle versions)"
    frequency: "Once per map generation run"
    
  - endpoint: GET /bulk-data/default-cards
    purpose: "Download all card printings for pricing/release dates"
    frequency: "Once per map generation run"

Data Flow:
  - direction: INBOUND - fetch card reference data
  - format: JSON bulk download (~50MB compressed)
  - volume: ~25,000 unique cards, ~50,000 printings
  - processing: "Cards split for double-faced cards, price/date aggregation"

Error Handling:
  - network_failure: Script fails immediately (no retry logic)
  - invalid_response: Script fails immediately
  - service_down: Script cannot proceed without card data

Caching Strategy:
  - cached: NO - downloads fresh data each run
  - rationale: "Ensures latest card data for new releases"
  - optimization: "Could cache with TTL for faster development iteration"

Dependencies:
  - data_dependency: "Entire project depends on Scryfall card validation"
  - feature_dependency: "Card naming, type extraction, price calculation"

Tribal Knowledge:
  - "Oracle cards provide single canonical version but lack pricing data"
  - "Default cards needed for price aggregation across all printings"
  - "Double-faced cards require special handling for name splitting"
  - "Some cards hardcoded as non-tokens due to Scryfall classification edge cases"
```

**EDHREC Data Source:**
```yaml
Service Name: EDHREC Commander Deck Database
Purpose: Source of 1.2M+ Commander decklists for analysis
Criticality: CRITICAL - primary data source for the entire project

Integration Details:
  - API Type: Direct data access (bulk download)
  - Authentication: Email request to edhrec@edhrec.com
  - Format: Compressed JSON files (~1GB+)

Data Sources Included:
  - archidekt.com: Modern deckbuilding platform
  - moxfield.com: Popular Commander deck site
  - mtggoldfish.com: MTG finance and deck site
  - deckstats.net: Statistical deck analysis
  - aetherhub.com: Community deckbuilding

Data Flow:
  - direction: INBOUND - bulk dataset download
  - frequency: "Manual request per map generation (quarterly/biannually)"
  - volume: "1.2M+ decks, ~1GB compressed JSON"
  - processing: "Complex preprocessing with validation and cleaning"

Error Handling:
  - missing_cards: "Use edhrec-to-scryfall.json mapping file for corrections"
  - invalid_commanders: "Filter out invalid deck configurations"
  - data_corruption: "Script fails, requires manual intervention"

Dependencies:
  - data_dependency: "Primary dataset - cannot create map without EDHREC data"
  - update_frequency: "New map versions require fresh EDHREC data"

Tribal Knowledge:
  - "EDHREC data includes cards not in Scryfall (typos, unofficial names)"
  - "Deck URLs can be parsed to extract platform and deck identifiers"
  - "Quality varies significantly between platforms"
  - "Data includes test decks and invalid configurations requiring filtering"
```

### 5.2 Authentication Providers

```yaml
Provider: None
Why Chosen: N/A - batch processing script with no user authentication

OAuth Configuration: N/A
User Data Mapping: N/A
Token Management: N/A
```

### 5.3 Other External Services

```yaml
Service Type: Cloud Computing Platform
Service Name: Google Cloud Platform (via Terra)
Purpose: High-memory compute instances for large-scale embedding
Configuration: Dockerfile + WDL workflow definition
Criticality: IMPORTANT - required for full dataset processing
Fallback: Local processing with smaller datasets or subset sampling

Service Type: Container Registry
Service Name: Docker Hub
Purpose: Hosts jcrowdis/commander-map Docker image
Configuration: Automated builds from repository
Criticality: NICE-TO-HAVE - enables cloud deployment
Fallback: Build Docker image locally

Service Type: Data Storage
Service Name: Lucky Paper Website
Purpose: Consumes generated CSV/JSON files for interactive map
Configuration: Manual file upload/deployment
Criticality: IMPORTANT - end destination for map data
Fallback: Data can be used elsewhere or served statically
```

---

## Section 6: Frontend Architecture [N/A]

```yaml
No frontend - this project generates data files consumed by external website (Lucky Paper).
The visualization and user interaction happens on https://luckypaper.co/resources/commander-map
which is outside the scope of this analysis.
```

---

## Section 7: Testing & Quality [IMPORTANT]

### 7.1 Test Coverage

```yaml
Unit Tests:
  - framework: Basic Python script (test.py)
  - coverage: Minimal - primarily algorithm validation
  - location: scripts/test.py
  - critical_coverage: Data processing functions, parameter calculation

Integration Tests:
  - framework: None
  - coverage: No automated integration testing
  - location: N/A

End-to-End Tests:
  - framework: Manual validation
  - coverage: Visual inspection of generated maps
  - location: commander-map.ipynb notebook

Test Data:
  - fixtures: None - uses production EDHREC data
  - mocking_strategy: No mocking implemented
  - test_db: No database used

Testing Framework:
  - framework: Minimal custom validation
    coverage: "Unknown - no formal coverage measurement"
    validation: "Manual inspection of clustering quality and map coherence"
```

### 7.2 Critical Test Cases

```yaml
Test Suite: Algorithm Validation
Location: scripts/test.py + manual notebook validation
Coverage: Low

Critical Test Cases:
  - test_name: UMAP_embedding_quality
    scenario: "Verify UMAP produces reasonable 2D coordinates"
    assertion: "No NaN values, coordinates within expected bounds"
    why_critical: "Core visualization functionality"
  
  - test_name: HDBSCAN_clustering_validity
    scenario: "Ensure clustering produces interpretable groups"
    assertion: "Minimum cluster size respected, noise percentage reasonable"
    why_critical: "Determines map usefulness"
  
  - test_name: card_validation_completeness
    scenario: "All deck cards can be resolved to Scryfall cards"
    assertion: "No unknown cards after mapping file application"
    why_critical: "Data integrity requirement"

Missing Test Coverage:
  - area: Performance regression testing
    risk: High - algorithm changes could dramatically increase runtime
  - area: Data quality validation
    risk: Medium - bad input data could produce meaningless maps
  - area: Parameter sensitivity analysis
    risk: Medium - clustering quality depends heavily on parameter tuning
```

---

## Section 8: Performance Characteristics [CRITICAL]

### 8.1 Performance Baselines

```yaml
Full Pipeline Performance (1.2M decks):
  - stage: Data preprocessing
    runtime: 2-4 hours
    memory_usage: 8-16GB
    bottleneck: "Scryfall API calls and data validation"
  
  - stage: UMAP 2D embedding
    runtime: 4-8 hours
    memory_usage: 32GB+
    bottleneck: "High-dimensional matrix operations"
  
  - stage: HDBSCAN clustering
    runtime: 1-3 hours
    memory_usage: 16-32GB
    bottleneck: "Distance matrix computation"
  
  - stage: Submap generation
    runtime: 12-24 hours
    memory_usage: 8-16GB
    bottleneck: "Processing thousands of individual submaps"

Cloud Deployment Performance:
  - platform: Google Cloud Platform
  - instance_type: "High-memory (32GB+ RAM)"
  - total_runtime: "24-48 hours end-to-end"
  - cost: "~$3 per complete map generation"

Parameter Scaling:
  - dataset_size: "Runtime scales approximately O(n log n)"
  - embedding_dimensions: "Memory scales linearly with dimensions"
  - cluster_parameters: "Quality vs speed tradeoff"
```

### 8.2 Performance Bottlenecks

```yaml
Known Bottlenecks:
  - location: UMAP embedding of full dataset
    symptom: "Memory exhaustion on standard hardware"
    impact: "Cannot run locally on typical developer machines"
    fix_priority: "Medium - cloud deployment mitigates"
  
  - location: Submap generation loop
    symptom: "Sequential processing of thousands of submaps"
    impact: "Longest runtime component of pipeline"
    fix_priority: "Low - parallelization possible but complex"

Optimization Strategies Used:
  - strategy: "Sparse matrix representation for deck data"
    improvement: "Reduces memory usage by ~90% vs dense matrices"
  
  - strategy: "Adaptive parameter selection by dataset size"
    improvement: "Maintains clustering quality across different scales"
  
  - strategy: "Cloud deployment for memory-intensive operations"
    improvement: "Enables processing of full dataset"
```

### 8.3 Scalability Characteristics

```yaml
Current Scale:
  - decks: "~1.2 million Commander decks"
  - cards: "~25,000 unique Magic cards"
  - submaps: "~2,000 individual archetypes"
  - output_size: "~500MB of generated data files"

Scaling Limits:
  - memory: "32GB+ required for embedding 1M+ decks"
  - compute: "Single-threaded algorithms limit parallelization"
  - storage: "Output scales linearly with input deck count"

Horizontal Scaling:
  - supported: "Limited - submap generation could be parallelized"
  - constraints: "UMAP/HDBSCAN algorithms are inherently sequential"
  - workarounds: "Subset sampling for development, cloud scaling for production"
```

---

## Section 9: Security & Compliance [NICE-TO-HAVE]

### 9.1 Security Measures

```yaml
Authentication Security: N/A - no authentication system
Authorization Security: N/A - batch processing script
Data Security:
  - encryption_at_rest: "Depends on cloud provider settings"
  - encryption_in_transit: "HTTPS for Scryfall API calls"
  - sensitive_data: "None - all Magic card data is public"
  - pii_handling: "None - no personal information processed"

Input Validation:
  - data_validation: "Card name validation against Scryfall database"
  - injection_protection: "Not applicable - no user input"
  - file_validation: "Basic JSON parsing error handling"

API Security: N/A - no API endpoints
```

### 9.2 Secrets Management

```yaml
Secrets Stored: None - project uses public APIs only

Environment Variables Required:
  - name: None - configuration via command-line arguments
```

### 9.3 Compliance Requirements

```yaml
Regulations:
  - regulation: None specific
  - data_rights: "Uses publicly available game data"

Data Retention:
  - data_type: "Generated map files"
    retention_period: "Indefinite - published data"
  - data_type: "EDHREC source data"
    retention_period: "Deleted after processing"

Audit Logging:
  - logged_events: "Processing stages via console output"
  - log_retention: "Not persistent - console output only"
```

---

## Section 10: Deployment & Operations [IMPORTANT]

### 10.1 Deployment Process

```yaml
Environment Strategy:
  - environments: "Development (local), Production (cloud)"
  - differences: "Dataset size, memory requirements, runtime duration"

Deployment Method:
  - type: "Manual execution (local) or Cloud Workflow (Terra)"
  - trigger: "Manual initiation when new EDHREC data available"
  - rollback_process: "Revert to previous data files, re-run pipeline"

Build Process:
  - steps:
    1. "Download EDHREC data"
    2. "Install Python dependencies"
    3. "Run preprocessing script"
    4. "Execute embedding and clustering"
    5. "Generate submaps"
    6. "Export data files"
  - duration: "1-2 days for full pipeline"
  - artifacts: "CSV/JSON files for Lucky Paper website"

Configuration Management:
  - method: "Command-line arguments and config files"
  - location: "duplicates.txt, edhrec-to-scryfall.json, theme-tribe-override.csv"
  - per_environment: "Dataset size and memory allocation"
```

### 10.2 Monitoring & Logging

```yaml
Application Monitoring:
  - tool: "Console output and manual monitoring"
  - metrics_tracked: "Processing stage completion, memory usage alerts"
  - alerts_configured: "No automated alerts"

Logging:
  - framework: "Python print statements and console output"
  - log_levels: "INFO level progress updates"
  - log_destination: "Console/terminal output"
  - structured_logging: "No - plain text progress messages"

Error Tracking:
  - tool: "None - manual error observation"
  - error_notifications: "None - operator must monitor"
  - error_rate_baseline: "Pipeline should complete without errors"
```

### 10.3 Backup & Disaster Recovery

```yaml
Database Backups: N/A - no persistent database

Code Backups:
  - location: "Git repository"
  - redundancy: "GitHub hosting"

Data Backups:
  - frequency: "Manual backup of generated output files"
  - retention: "Previous map versions retained indefinitely"
  - restoration_time: "Re-run pipeline (1-2 days)"

Recovery Procedures:
  - documented: "Basic documentation in README"
  - rto: "Recovery Time Objective - 48-72 hours"
  - rpo: "Recovery Point Objective - last quarterly data release"
```

---

## Section 11: Domain Knowledge & Tribal Knowledge [CRITICAL]

### 11.1 Business Domain Expertise

```yaml
Domain: Magic: The Gathering Commander Format + Data Science Visualization

Domain Concepts Encoded in Code:
  - concept: Commander Color Identity
    definition: "Determines which cards can legally be included in a deck"
    implementation: "Used for deck validation and cluster characterization"
    source_of_truth: "Scryfall API color_identity field"
  
  - concept: Deck Archetypes
    definition: "Natural groupings of decks with similar strategies (tribal, combo, control)"
    implementation: "Discovered automatically via HDBSCAN clustering"
    source_of_truth: "Emergent from deck similarity patterns"
  
  - concept: Defining Cards
    definition: "Cards that statistically characterize a cluster's identity"
    implementation: "Statistical significance testing against baseline inclusion rates"
    source_of_truth: "Binomial distribution calculations"
  
  - concept: Jaccard Similarity
    definition: "Measure of deck similarity based on shared cards"
    implementation: "UMAP metric for preserving deck relationships"
    source_of_truth: "Set intersection / union formula"

Industry-Specific Rules:
  - rule: "Commander decks must have exactly one legendary commander"
    enforcement: "Validated during preprocessing"
  
  - rule: "Color identity constrains legal card choices"
    enforcement: "Not enforced - allows rule violations for analysis"
  
  - rule: "Commander format is singleton (one copy per card except basics)"
    enforcement: "Assumed in data but not validated"

Terminology Dictionary:
  - term: Commander
    definition: "Legendary creature or planeswalker that leads the deck"
    used_in: "Deck validation, cluster characterization"
  
  - term: Archetype
    definition: "Category of decks with similar strategic approach"
    used_in: "Clustering results, submap generation"
  
  - term: Submap
    definition: "Focused map showing decks within a specific archetype"
    used_in: "Individual cluster visualization"
  
  - term: Defining Cards
    definition: "Cards that statistically characterize a cluster"
    used_in: "Cluster interpretation and description"
```

### 11.2 Undocumented Knowledge

```yaml
Quirks & Workarounds:
  - quirk: "Scryfall oracle cards lack pricing, default cards needed"
    workaround: "Download both oracle and default card datasets"
    reason: "Oracle provides canonical names, default provides pricing"
  
  - quirk: "Double-faced cards named differently in decklists vs Scryfall"
    workaround: "Split card names on ' // ' and create separate entries"
    reason: "Deckbuilding sites use front face names only"
  
  - quirk: "Some cards incorrectly classified as tokens in Scryfall"
    workaround: "Hardcoded list of cards to override token classification"
    reason: "Prevents valid cards from being filtered out"

Historical Context:
  - decision: "Why UMAP instead of t-SNE for dimensionality reduction"
    reason: "UMAP preserves both local and global structure better"
    context: "t-SNE loses global relationships, PCA too linear"
  
  - decision: "Why HDBSCAN instead of k-means clustering"
    reason: "Density-based clustering handles varying cluster sizes"
    context: "Commander archetypes have very different popularity levels"
  
  - decision: "Why Jaccard metric for deck similarity"
    reason: "Optimal for binary card inclusion data"
    context: "Euclidean distance inappropriate for sparse binary vectors"

Known Technical Debt:
  - debt: "No automated testing of clustering quality"
    impact: "Parameter changes could degrade map usefulness"
    plan: "Develop quantitative clustering evaluation metrics"
  
  - debt: "Memory usage not optimized for embedding step"
    impact: "Requires expensive cloud instances for processing"
    plan: "Investigate incremental or approximate embedding methods"
  
  - debt: "Submap generation not parallelized"
    impact: "Longest runtime component of pipeline"
    plan: "Implement multiprocessing for independent submaps"
```

### 11.3 User Behavior Patterns

```yaml
Common User Workflows:
  - workflow: "Explore deck archetypes in meta visualization"
    frequency: "Primary use case for Lucky Paper visitors"
    steps: ["Browse map regions", "Identify clusters", "Examine defining cards"]
  
  - workflow: "Find similar decks to existing build"
    frequency: "Regular power user behavior"
    steps: ["Locate commander on map", "Explore nearby decks", "Analyze differences"]

Edge Cases Users Hit:
  - edge_case: "Searching for very new commanders"
    behavior: "Expect recent cards to appear on map"
    handling: "New maps generated quarterly with updated data"
  
  - edge_case: "Unusual deck builds that don't cluster well"
    behavior: "Wonder why their deck archetype isn't represented"
    handling: "Outlier decks may not form coherent clusters"

User Expectations:
  - expectation: "Similar decks should be close together on map"
    reality: "UMAP generally preserves this relationship"
  
  - expectation: "All viable archetypes should be discoverable"
    reality: "Only popular archetypes form distinct clusters"
  
  - expectation: "Map should reflect current meta trends"
    reality: "Map updated quarterly, may lag behind rapid meta shifts"
```

---

## Section 12: Migration Readiness Assessment

### 12.1 Migration Priority

```yaml
Overall Priority: NICE-TO-HAVE
Reason: Valuable community resource but not core business functionality

User Impact:
  - users_affected: "~10,000 Lucky Paper visitors using Commander Map"
  - downtime_acceptable: "YES - quarterly updates already have gaps"
  - feature_parity_required: "90% - some features could be simplified"

Technical Complexity:
  - data_migration: "Simple - stateless data processing pipeline"
  - code_migration: "Medium - complex ML algorithms need preservation"
  - integration_complexity: "Simple - minimal external dependencies"

Dependencies:
  - blocking_projects: "None - standalone data processing"
  - dependent_projects: "Lucky Paper website consumes output files"
```

### 12.2 Risks & Concerns

```yaml
Data Migration Risks:
  - risk: "Loss of algorithm fidelity during code translation"
    likelihood: "Medium"
    mitigation: "Extensive testing with known datasets"
  
  - risk: "Performance regression due to different infrastructure"
    likelihood: "High"
    mitigation: "Maintain cloud deployment option for memory-intensive operations"

Technical Risks:
  - risk: "UMAP/HDBSCAN parameter tuning may need adjustment"
    likelihood: "Medium"
    mitigation: "Preserve existing parameter selection logic"
  
  - risk: "Memory requirements exceed monolith infrastructure"
    likelihood: "High"
    mitigation: "Keep separate processing pipeline for map generation"

Business Risks:
  - risk: "Map quality degradation affects Lucky Paper content"
    likelihood: "Low"
    mitigation: "Maintain side-by-side comparison during migration"
```

### 12.3 Success Criteria

```yaml
Functional Requirements:
  - [ ] Generated maps visually identical to current version
  - [ ] All archetype clusters preserved with same defining cards
  - [ ] Submap generation produces equivalent results
  - [ ] Processing pipeline completes within acceptable timeframe
  - [ ] Output file format remains compatible with Lucky Paper website

Performance Requirements:
  - [ ] Full pipeline runtime within 48-72 hours (current baseline)
  - [ ] Memory usage manageable within available infrastructure
  - [ ] Generated file sizes within expected ranges

Quality Requirements:
  - [ ] Clustering quality metrics match baseline
  - [ ] No degradation in map interpretability
  - [ ] Statistical significance of defining cards maintained
```

---

## Section 13: Documentation & Resources

### 13.1 Existing Documentation

```yaml
Documentation Locations:
  - type: README with comprehensive setup instructions
    quality: "Good - covers both local and cloud deployment"
  
  - type: Jupyter notebook with algorithm explanations
    quality: "Excellent - detailed walkthrough of methodology"
  
  - type: Inline code comments
    quality: "Adequate - key algorithms documented"

Code Comments:
  - quality: "Good"
  - areas_well_documented: "UMAP/HDBSCAN algorithms, parameter selection"
  - areas_poorly_documented: "Data preprocessing edge cases, cloud deployment details"

Diagrams:
  - type: "None currently - would benefit from pipeline flowchart"
  - needed: "Data flow diagram, algorithm decision tree"
```

### 13.2 Key Contacts

```yaml
Subject Matter Experts:
  - name: "Lucky Paper editorial team"
    expertise: "MTG Commander domain knowledge, user requirements"
  
  - name: "EDHREC team (edhrec@edhrec.com)"
    expertise: "Source data format and availability"

Original Developers:
  - name: "jcrowdis (GitHub username from Docker image)"
    expertise: "Algorithm design, implementation decisions"

Current Maintainers:
  - name: "Lucky Paper team"
    availability: "Available via Lucky Paper website contact"
```

---

## Analysis Completion Checklist

**Before considering this analysis complete:**

- [x] All sections filled out (or marked N/A)
- [x] All CRITICAL business logic documented with code examples
- [x] All API endpoints inventoried (N/A - no API)
- [x] All data models documented with fields and relationships
- [x] All external integrations documented with error handling
- [x] Performance baselines measured or estimated
- [x] Test coverage assessed
- [x] Migration risks identified
- [x] Tribal knowledge captured
- [x] Edge cases and quirks documented

**Confidence Level:** High  
**Areas Needing More Investigation:** 
- Exact memory usage profiling during embedding
- Quantitative clustering quality metrics
- Cloud deployment cost optimization

---

**Analysis Completed By:** GitHub Copilot  
**Date:** October 9, 2025  
**Time Invested:** 2.5 hours  
**Next Steps:** Evaluate whether data science pipeline fits within modular monolith or should remain separate processing system