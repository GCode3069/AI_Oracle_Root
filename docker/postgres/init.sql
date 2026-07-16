-- Drepseek MCP Server PostgreSQL Initialization Script

-- Create database if it doesn't exist (handled by POSTGRES_DB env var)
-- This script runs after database creation

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS drepseek;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Set search path
SET search_path TO drepseek, public;

-- Proposals table
CREATE TABLE IF NOT EXISTS drepseek.drep_proposals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proposal_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK (status IN ('active', 'passed', 'rejected', 'pending', 'expired')),
    voting_start BIGINT,
    voting_end BIGINT,
    votes_yes BIGINT DEFAULT 0,
    votes_no BIGINT DEFAULT 0,
    votes_abstain BIGINT DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Voting history table
CREATE TABLE IF NOT EXISTS drepseek.voting_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proposal_id TEXT NOT NULL,
    drep_address TEXT NOT NULL,
    vote_type TEXT CHECK (vote_type IN ('yes', 'no', 'abstain')),
    voting_power BIGINT NOT NULL,
    epoch INTEGER,
    tx_hash TEXT,
    timestamp BIGINT NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proposal_id) REFERENCES drepseek.drep_proposals(proposal_id) ON DELETE CASCADE
);

-- Network metrics table
CREATE TABLE IF NOT EXISTS drepseek.network_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_type TEXT NOT NULL,
    metric_value DOUBLE PRECISION,
    metric_data JSONB,
    epoch INTEGER,
    timestamp BIGINT NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Delegations table
CREATE TABLE IF NOT EXISTS drepseek.delegations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    drep_address TEXT NOT NULL,
    delegator_address TEXT NOT NULL,
    amount BIGINT NOT NULL,
    epoch INTEGER NOT NULL,
    tx_hash TEXT,
    timestamp BIGINT NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Drep information table
CREATE TABLE IF NOT EXISTS drepseek.drep_info (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    drep_address TEXT UNIQUE NOT NULL,
    name TEXT,
    description TEXT,
    website TEXT,
    total_voting_power BIGINT DEFAULT 0,
    total_delegators INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Analytics: Daily aggregates
CREATE TABLE IF NOT EXISTS analytics.daily_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    total_proposals INTEGER DEFAULT 0,
    active_proposals INTEGER DEFAULT 0,
    total_votes BIGINT DEFAULT 0,
    total_voting_power BIGINT DEFAULT 0,
    unique_voters INTEGER DEFAULT 0,
    participation_rate DOUBLE PRECISION,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_proposals_status ON drepseek.drep_proposals(status);
CREATE INDEX IF NOT EXISTS idx_proposals_voting_end ON drepseek.drep_proposals(voting_end);
CREATE INDEX IF NOT EXISTS idx_proposals_created_at ON drepseek.drep_proposals(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_voting_history_proposal ON drepseek.voting_history(proposal_id);
CREATE INDEX IF NOT EXISTS idx_voting_history_drep ON drepseek.voting_history(drep_address);
CREATE INDEX IF NOT EXISTS idx_voting_history_timestamp ON drepseek.voting_history(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_voting_history_epoch ON drepseek.voting_history(epoch);

CREATE INDEX IF NOT EXISTS idx_metrics_type ON drepseek.network_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON drepseek.network_metrics(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_epoch ON drepseek.network_metrics(epoch);

CREATE INDEX IF NOT EXISTS idx_delegations_drep ON drepseek.delegations(drep_address);
CREATE INDEX IF NOT EXISTS idx_delegations_delegator ON drepseek.delegations(delegator_address);
CREATE INDEX IF NOT EXISTS idx_delegations_epoch ON drepseek.delegations(epoch DESC);
CREATE INDEX IF NOT EXISTS idx_delegations_timestamp ON drepseek.delegations(timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_drep_info_address ON drepseek.drep_info(drep_address);
CREATE INDEX IF NOT EXISTS idx_drep_info_active ON drepseek.drep_info(active);

-- Full-text search indexes
CREATE INDEX IF NOT EXISTS idx_proposals_search ON drepseek.drep_proposals 
    USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_proposals_updated_at BEFORE UPDATE ON drepseek.drep_proposals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_drep_info_updated_at BEFORE UPDATE ON drepseek.drep_info
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE OR REPLACE VIEW drepseek.active_proposals AS
SELECT * FROM drepseek.drep_proposals
WHERE status = 'active'
ORDER BY voting_end ASC;

CREATE OR REPLACE VIEW drepseek.recent_votes AS
SELECT 
    vh.*,
    dp.title as proposal_title,
    dp.status as proposal_status
FROM drepseek.voting_history vh
JOIN drepseek.drep_proposals dp ON vh.proposal_id = dp.proposal_id
ORDER BY vh.timestamp DESC
LIMIT 1000;

CREATE OR REPLACE VIEW analytics.drep_summary AS
SELECT 
    di.drep_address,
    di.name,
    di.total_voting_power,
    di.total_delegators,
    COUNT(DISTINCT vh.proposal_id) as votes_cast,
    MAX(vh.timestamp) as last_vote_time
FROM drepseek.drep_info di
LEFT JOIN drepseek.voting_history vh ON di.drep_address = vh.drep_address
WHERE di.active = TRUE
GROUP BY di.drep_address, di.name, di.total_voting_power, di.total_delegators;

-- Grant permissions (adjust as needed)
GRANT USAGE ON SCHEMA drepseek TO drepseek;
GRANT USAGE ON SCHEMA analytics TO drepseek;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA drepseek TO drepseek;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO drepseek;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA drepseek TO drepseek;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO drepseek;

-- Insert sample data (optional, for testing)
-- Uncomment below to populate with sample data
/*
INSERT INTO drepseek.drep_proposals (proposal_id, title, description, status, voting_start, voting_end, votes_yes, votes_no, votes_abstain)
VALUES 
    ('prop-001', 'Treasury Withdrawal for Project A', 'Proposal to withdraw 100k ADA for Project A development', 'active', EXTRACT(EPOCH FROM NOW())::BIGINT, EXTRACT(EPOCH FROM NOW() + INTERVAL '7 days')::BIGINT, 150000, 50000, 10000),
    ('prop-002', 'Protocol Parameter Update', 'Update minimum pool cost parameter', 'active', EXTRACT(EPOCH FROM NOW())::BIGINT, EXTRACT(EPOCH FROM NOW() + INTERVAL '5 days')::BIGINT, 200000, 30000, 5000),
    ('prop-003', 'Info Action', 'Informational governance action', 'passed', EXTRACT(EPOCH FROM NOW() - INTERVAL '10 days')::BIGINT, EXTRACT(EPOCH FROM NOW() - INTERVAL '3 days')::BIGINT, 180000, 20000, 8000);

INSERT INTO drepseek.drep_info (drep_address, name, description, total_voting_power, total_delegators, active)
VALUES
    ('drep1abc123xyz', 'Cardano Foundation Drep', 'Official CF representative', 5000000000, 1500, TRUE),
    ('drep1def456uvw', 'Community Drep A', 'Community representative focused on development', 2000000000, 800, TRUE),
    ('drep1ghi789rst', 'Ecosystem Drep', 'Supporting ecosystem growth', 1500000000, 600, TRUE);
*/

-- Maintenance functions
CREATE OR REPLACE FUNCTION drepseek.cleanup_old_metrics(days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM drepseek.network_metrics
    WHERE recorded_at < CURRENT_TIMESTAMP - (days_to_keep || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate participation rate
CREATE OR REPLACE FUNCTION analytics.calculate_participation_rate(proposal_id_param TEXT)
RETURNS DOUBLE PRECISION AS $$
DECLARE
    total_power BIGINT;
    voted_power BIGINT;
BEGIN
    SELECT COALESCE(SUM(total_voting_power), 0) INTO total_power
    FROM drepseek.drep_info WHERE active = TRUE;
    
    SELECT COALESCE(SUM(voting_power), 0) INTO voted_power
    FROM drepseek.voting_history
    WHERE proposal_id = proposal_id_param;
    
    IF total_power > 0 THEN
        RETURN (voted_power::DOUBLE PRECISION / total_power::DOUBLE PRECISION) * 100;
    ELSE
        RETURN 0;
    END IF;
END;
$$ LANGUAGE plpgsql;

COMMENT ON DATABASE drepseek_mcp IS 'Drepseek MCP Server database for Cardano governance data';
COMMENT ON SCHEMA drepseek IS 'Core Drepseek data tables';
COMMENT ON SCHEMA analytics IS 'Analytics and aggregated data';
