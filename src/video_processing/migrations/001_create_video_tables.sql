-- Migration: Create video processing tables
-- Version: 001
-- Description: Initial schema for video metadata, analysis, and collections

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create video_metadata table
CREATE TABLE IF NOT EXISTS video_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id VARCHAR(20) UNIQUE NOT NULL,
    url VARCHAR(500) NOT NULL,
    title TEXT,
    description TEXT,
    channel_name VARCHAR(200),
    duration VARCHAR(20),
    view_count INTEGER,
    upload_date VARCHAR(50),
    thumbnail_url VARCHAR(500),
    processing_status VARCHAR(20) DEFAULT 'pending',
    processing_error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on video_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_video_metadata_video_id ON video_metadata(video_id);
CREATE INDEX IF NOT EXISTS idx_video_metadata_status ON video_metadata(processing_status);
CREATE INDEX IF NOT EXISTS idx_video_metadata_created_at ON video_metadata(created_at);

-- Create video_analysis table
CREATE TABLE IF NOT EXISTS video_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID NOT NULL REFERENCES video_metadata(id) ON DELETE CASCADE,
    quantum_relevance_score REAL DEFAULT 0.0,
    educational_content BOOLEAN DEFAULT FALSE,
    technical_level VARCHAR(20),
    content_type VARCHAR(50),
    keywords JSONB DEFAULT '[]'::jsonb,
    topics JSONB DEFAULT '[]'::jsonb,
    key_concepts JSONB DEFAULT '[]'::jsonb,
    analysis_version VARCHAR(10) DEFAULT '1.0',
    confidence_score REAL DEFAULT 0.0,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for video_analysis
CREATE INDEX IF NOT EXISTS idx_video_analysis_video_id ON video_analysis(video_id);
CREATE INDEX IF NOT EXISTS idx_video_analysis_relevance_score ON video_analysis(quantum_relevance_score);
CREATE INDEX IF NOT EXISTS idx_video_analysis_educational ON video_analysis(educational_content);
CREATE INDEX IF NOT EXISTS idx_video_analysis_technical_level ON video_analysis(technical_level);
CREATE INDEX IF NOT EXISTS idx_video_analysis_keywords ON video_analysis USING GIN(keywords);
CREATE INDEX IF NOT EXISTS idx_video_analysis_topics ON video_analysis USING GIN(topics);

-- Create video_tags table
CREATE TABLE IF NOT EXISTS video_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID NOT NULL REFERENCES video_metadata(id) ON DELETE CASCADE,
    tag_name VARCHAR(100) NOT NULL,
    tag_category VARCHAR(50),
    confidence REAL DEFAULT 1.0,
    auto_generated BOOLEAN DEFAULT TRUE,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for video_tags
CREATE INDEX IF NOT EXISTS idx_video_tags_video_id ON video_tags(video_id);
CREATE INDEX IF NOT EXISTS idx_video_tags_name ON video_tags(tag_name);
CREATE INDEX IF NOT EXISTS idx_video_tags_category ON video_tags(tag_category);
CREATE INDEX IF NOT EXISTS idx_video_tags_verified ON video_tags(verified);

-- Create video_collections table
CREATE TABLE IF NOT EXISTS video_collections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    collection_type VARCHAR(50),
    is_public BOOLEAN DEFAULT FALSE,
    created_by VARCHAR(100),
    video_count INTEGER DEFAULT 0,
    total_duration VARCHAR(20),
    avg_relevance_score REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for video_collections
CREATE INDEX IF NOT EXISTS idx_video_collections_name ON video_collections(name);
CREATE INDEX IF NOT EXISTS idx_video_collections_type ON video_collections(collection_type);
CREATE INDEX IF NOT EXISTS idx_video_collections_public ON video_collections(is_public);
CREATE INDEX IF NOT EXISTS idx_video_collections_created_by ON video_collections(created_by);

-- Create video_collection_items table
CREATE TABLE IF NOT EXISTS video_collection_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    collection_id UUID NOT NULL REFERENCES video_collections(id) ON DELETE CASCADE,
    video_id UUID NOT NULL REFERENCES video_metadata(id) ON DELETE CASCADE,
    order_index INTEGER DEFAULT 0,
    notes TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(collection_id, video_id)
);

-- Create indexes for video_collection_items
CREATE INDEX IF NOT EXISTS idx_video_collection_items_collection_id ON video_collection_items(collection_id);
CREATE INDEX IF NOT EXISTS idx_video_collection_items_video_id ON video_collection_items(video_id);
CREATE INDEX IF NOT EXISTS idx_video_collection_items_order ON video_collection_items(collection_id, order_index);

-- Create processing_jobs table
CREATE TABLE IF NOT EXISTS processing_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    parameters JSONB DEFAULT '{}'::jsonb,
    total_items INTEGER DEFAULT 0,
    processed_items INTEGER DEFAULT 0,
    failed_items INTEGER DEFAULT 0,
    results JSONB DEFAULT '{}'::jsonb,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Create indexes for processing_jobs
CREATE INDEX IF NOT EXISTS idx_processing_jobs_type ON processing_jobs(job_type);
CREATE INDEX IF NOT EXISTS idx_processing_jobs_status ON processing_jobs(status);
CREATE INDEX IF NOT EXISTS idx_processing_jobs_created_at ON processing_jobs(created_at);

-- Create video_statistics table
CREATE TABLE IF NOT EXISTS video_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    period_type VARCHAR(20) NOT NULL,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    total_videos INTEGER DEFAULT 0,
    new_videos INTEGER DEFAULT 0,
    quantum_relevant_videos INTEGER DEFAULT 0,
    educational_videos INTEGER DEFAULT 0,
    avg_relevance_score REAL DEFAULT 0.0,
    processing_success_rate REAL DEFAULT 0.0,
    top_keywords JSONB DEFAULT '[]'::jsonb,
    top_concepts JSONB DEFAULT '[]'::jsonb,
    technical_level_distribution JSONB DEFAULT '{}'::jsonb,
    content_type_distribution JSONB DEFAULT '{}'::jsonb,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(period_type, period_start, period_end)
);

-- Create indexes for video_statistics
CREATE INDEX IF NOT EXISTS idx_video_statistics_period ON video_statistics(period_type, period_start);
CREATE INDEX IF NOT EXISTS idx_video_statistics_calculated_at ON video_statistics(calculated_at);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at column
CREATE TRIGGER update_video_metadata_updated_at
    BEFORE UPDATE ON video_metadata
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_video_collections_updated_at
    BEFORE UPDATE ON video_collections
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE OR REPLACE VIEW quantum_relevant_videos AS
SELECT 
    vm.*,
    va.quantum_relevance_score,
    va.educational_content,
    va.technical_level,
    va.content_type
FROM video_metadata vm
JOIN video_analysis va ON vm.id = va.video_id
WHERE va.quantum_relevance_score >= 0.5;

CREATE OR REPLACE VIEW educational_videos AS
SELECT 
    vm.*,
    va.quantum_relevance_score,
    va.technical_level,
    va.content_type,
    va.key_concepts
FROM video_metadata vm
JOIN video_analysis va ON vm.id = va.video_id
WHERE va.educational_content = TRUE;

CREATE OR REPLACE VIEW video_summary AS
SELECT 
    vm.video_id,
    vm.title,
    vm.channel_name,
    vm.duration,
    vm.view_count,
    va.quantum_relevance_score,
    va.educational_content,
    va.technical_level,
    va.content_type,
    ARRAY_AGG(DISTINCT vt.tag_name) as tags
FROM video_metadata vm
LEFT JOIN video_analysis va ON vm.id = va.video_id
LEFT JOIN video_tags vt ON vm.id = vt.video_id
GROUP BY vm.id, va.id;

-- Insert initial data for testing (optional)
INSERT INTO video_collections (name, description, collection_type, is_public, created_by)
VALUES 
    ('Quantum Computing Fundamentals', 'Basic concepts and principles of quantum computing', 'course', true, 'system'),
    ('Quantum Algorithms', 'Advanced quantum algorithms and implementations', 'topic', true, 'system'),
    ('Quantum Hardware', 'Quantum hardware platforms and technologies', 'topic', true, 'system')
ON CONFLICT DO NOTHING;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO quantum_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO quantum_user;

COMMIT;