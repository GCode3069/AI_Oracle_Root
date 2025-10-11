-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create application user
CREATE USER scarify_app WITH PASSWORD '${SCARIFY_APP_PASSWORD}';

-- Create database schema
CREATE SCHEMA IF NOT EXISTS scarify AUTHORIZATION scarify_app;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA scarify TO scarify_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA scarify TO scarify_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA scarify TO scarify_app;

-- Create initial tables
CREATE TABLE IF NOT EXISTS scarify.projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scarify.videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES scarify.projects(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_path VARCHAR(500),
    status VARCHAR(50) DEFAULT 'pending',
    platform VARCHAR(50),
    upload_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scarify.upload_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES scarify.videos(id),
    platform VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    response_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scarify.revenue_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES scarify.videos(id),
    platform VARCHAR(50) NOT NULL,
    revenue_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_videos_project_id ON scarify.videos(project_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON scarify.videos(status);
CREATE INDEX IF NOT EXISTS idx_upload_logs_video_id ON scarify.upload_logs(video_id);
CREATE INDEX IF NOT EXISTS idx_revenue_tracking_video_id ON scarify.revenue_tracking(video_id);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON scarify.projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_videos_updated_at BEFORE UPDATE ON scarify.videos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
