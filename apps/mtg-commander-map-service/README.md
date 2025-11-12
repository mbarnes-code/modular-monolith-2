# MTG Commander Map Service

A Python-based service for generating the Lucky Paper Commander Map from EDHREC data.

## Overview

This service generates visualizations and data for MTG Commander decks using machine learning techniques including UMAP embedding and HDBSCAN clustering.

## Features

- **Data Processing**: Preprocesses EDHREC commander deck data
- **Embedding**: Uses UMAP to embed deck data into 2D coordinates
- **Clustering**: Applies HDBSCAN clustering to identify deck archetypes
- **Visualization**: Generates interactive commander maps
- **Jupyter Notebook**: Interactive analysis and explanation via `commander-map.ipynb`

## Development

### Prerequisites

- Python ≥ 3.7.9
- Node.js (for NX commands)

### Installation

```bash
# Install Python dependencies
nx run mtg-commander-map-service:install

# Or manually
cd apps/mtg-commander-map-service
pip install -r requirements.txt
```

### Available Commands

```bash
# Install dependencies
nx run mtg-commander-map-service:install

# Generate commander map (requires EDHREC data URL and date)
nx run mtg-commander-map-service:generate-map --edhrec_data=<url> --date=<date>

# Start Jupyter notebook
nx run mtg-commander-map-service:jupyter

# Run tests
nx run mtg-commander-map-service:test

# Lint code
nx run mtg-commander-map-service:lint

# Build Docker image
nx run mtg-commander-map-service:docker:build
```

### Local Map Generation

To create the map locally:

```bash
nx run mtg-commander-map-service:generate-map --edhrec_data=https://fake-edhrec-link.com --date=2022-05-13
```

This accomplishes the 4 main tasks:
1. Preprocesses EDHREC data and calculates submap defining cards and traits
2. Embeds the entire EDHREC data into 2 dimensions using UMAP
3. Clusters the data using HDBSCAN and calculates defining features
4. Generates submaps for each archetype with their own coordinates and clusters

**Note**: The full process takes at least a day to run with over 1.2 million decks and may require substantial RAM.

### Cloud Generation

For faster processing, use the provided Docker and WDL workflow files with Terra/Google Cloud:
- `Dockerfile`: Container for cloud execution
- `generate_commander_map.wdl`: Workflow definition
- Cost: ~$3 per map generation

## Required Files

- `duplicates.txt`: Cards commonly duplicated in decklists
- `edhrec-to-scryfall.json`: Maps incorrect EDHREC names to correct Scryfall names  
- `theme-tribe-override.csv`: Overrides for tribe/theme slugs and images

## Project Structure

```
apps/mtg-commander-map-service/
├── src/
│   └── scripts/           # Core Python modules
│       ├── calculate.py
│       ├── card.py
│       ├── companion.py
│       ├── generate_main_map_clusters.py
│       ├── generate_main_map_coordinates.py
│       ├── generate_submaps.py
│       ├── load.py
│       ├── map_classes.py
│       ├── preprocess_data.py
│       └── test.py
├── tests/                 # Test files
├── commander-map.ipynb    # Interactive notebook
├── make-map.sh           # Main execution script
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container definition
├── duplicates.txt       # Duplicate card list
├── edhrec-to-scryfall.json  # Name mappings
└── theme-tribe-override.csv # Theme/tribe overrides
```

## Tags

`mtg`, `python`, `data-science`, `visualization`
