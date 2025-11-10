"""
Initial database schema migration for Mental Prosthetic Platform.

Creates foundational schemas for all 4 domains:
- Security (13 tools)
- Productivity (8 tools) 
- MTG (4 tools)
- Infrastructure (12 tools)
"""

-- User profile and preferences (executive function accommodations)
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    adhd_accommodations JSONB DEFAULT '{}',
    autism_accommodations JSONB DEFAULT '{}',
    ui_preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cross-domain workflow state management  
CREATE TABLE IF NOT EXISTS workflow_states (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES user_profiles(id),
    current_domain VARCHAR(50) NOT NULL,
    state_data JSONB NOT NULL,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance monitoring for constitutional compliance
CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(50) NOT NULL,
    tool_name VARCHAR(100) NOT NULL,
    operation VARCHAR(100) NOT NULL,
    response_time_ms INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_profiles_username ON user_profiles(username);
CREATE INDEX IF NOT EXISTS idx_workflow_states_user_id ON workflow_states(user_id);
CREATE INDEX IF NOT EXISTS idx_workflow_states_domain ON workflow_states(current_domain);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_domain ON performance_metrics(domain);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_created_at ON performance_metrics(created_at);