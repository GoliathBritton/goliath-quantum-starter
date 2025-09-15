-- FLYFOX AI - Calling System Database Schema
-- Production-ready schema for contact management and calling operations

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    purpose TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    priority VARCHAR(20) DEFAULT 'normal',
    
    -- Campaign settings
    max_attempts INTEGER DEFAULT 3,
    retry_interval INTERVAL DEFAULT '24 hours',
    calling_hours_start TIME DEFAULT '08:00:00',
    calling_hours_end TIME DEFAULT '21:00:00',
    timezone VARCHAR(50) DEFAULT 'America/New_York',
    
    -- Compliance settings
    respect_dnc BOOLEAN DEFAULT true,
    require_consent BOOLEAN DEFAULT true,
    record_calls BOOLEAN DEFAULT true,
    
    -- Campaign metrics
    total_contacts INTEGER DEFAULT 0,
    contacts_called INTEGER DEFAULT 0,
    contacts_reached INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5,4) DEFAULT 0.0000,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- User tracking
    created_by UUID,
    updated_by UUID
);

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    
    -- Contact information
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    company VARCHAR(255),
    title VARCHAR(255),
    industry VARCHAR(100),
    
    -- Location and timezone
    timezone VARCHAR(50) DEFAULT 'America/New_York',
    country VARCHAR(2),
    state VARCHAR(50),
    city VARCHAR(100),
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'pending',
    consent_status VARCHAR(50) DEFAULT 'unknown',
    consent_date TIMESTAMP WITH TIME ZONE,
    
    -- Source and metadata
    source VARCHAR(100),
    tags JSONB DEFAULT '[]',
    custom_fields JSONB DEFAULT '{}',
    
    -- Call tracking
    call_attempts INTEGER DEFAULT 0,
    last_call_at TIMESTAMP WITH TIME ZONE,
    next_call_at TIMESTAMP WITH TIME ZONE,
    
    -- Lead scoring
    lead_score INTEGER DEFAULT 5,
    engagement_score DECIMAL(3,2) DEFAULT 0.50,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Call records table
CREATE TABLE IF NOT EXISTS call_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    
    -- Call details
    phone_number VARCHAR(20) NOT NULL,
    twilio_call_sid VARCHAR(100),
    status VARCHAR(50) DEFAULT 'queued',
    outcome VARCHAR(50),
    
    -- Call metrics
    duration INTEGER, -- seconds
    ring_time INTEGER, -- seconds
    talk_time INTEGER, -- seconds
    
    -- Recording and transcription
    recording_url TEXT,
    recording_duration INTEGER,
    transcript TEXT,
    transcript_confidence DECIMAL(3,2),
    
    -- AI analysis
    ai_summary TEXT,
    sentiment_score DECIMAL(3,2),
    emotion_analysis JSONB,
    intent_classification VARCHAR(100),
    
    -- Lead scoring
    lead_score INTEGER,
    conversion_probability DECIMAL(3,2),
    
    -- Follow-up actions
    next_action VARCHAR(100),
    scheduled_callback TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    
    -- Compliance
    consent_confirmed BOOLEAN DEFAULT false,
    opt_out_requested BOOLEAN DEFAULT false,
    dnc_requested BOOLEAN DEFAULT false,
    
    -- Timestamps
    started_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversation turns table
CREATE TABLE IF NOT EXISTS conversation_turns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    call_record_id UUID REFERENCES call_records(id) ON DELETE CASCADE,
    
    -- Turn details
    turn_number INTEGER NOT NULL,
    speaker VARCHAR(20) NOT NULL, -- 'agent' or 'contact'
    
    -- Content
    text TEXT NOT NULL,
    audio_url TEXT,
    duration INTEGER, -- milliseconds
    
    -- AI analysis
    intent VARCHAR(100),
    sentiment VARCHAR(20),
    confidence DECIMAL(3,2),
    entities JSONB DEFAULT '{}',
    
    -- Timestamps
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- DNC (Do Not Call) registry
CREATE TABLE IF NOT EXISTS dnc_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    
    -- DNC details
    source VARCHAR(100), -- 'federal', 'state', 'internal', 'customer_request'
    reason TEXT,
    
    -- Timestamps
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Verification
    verified BOOLEAN DEFAULT false,
    last_checked TIMESTAMP WITH TIME ZONE
);

-- Consent records
CREATE TABLE IF NOT EXISTS consent_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    
    -- Consent details
    consent_type VARCHAR(50) NOT NULL, -- 'explicit', 'implied', 'withdrawn'
    method VARCHAR(50), -- 'phone', 'email', 'web', 'sms'
    purpose TEXT,
    
    -- Legal basis
    legal_basis VARCHAR(100),
    jurisdiction VARCHAR(50),
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    source_url TEXT,
    
    -- Timestamps
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    withdrawn_at TIMESTAMP WITH TIME ZONE
);

-- Call queues for job management
CREATE TABLE IF NOT EXISTS call_queues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    
    -- Queue details
    priority INTEGER DEFAULT 5,
    scheduled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    
    -- Status
    status VARCHAR(50) DEFAULT 'queued', -- 'queued', 'processing', 'completed', 'failed'
    error_message TEXT,
    
    -- Worker assignment
    worker_id VARCHAR(100),
    assigned_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Campaign analytics
CREATE TABLE IF NOT EXISTS campaign_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    
    -- Date for daily aggregation
    date DATE NOT NULL,
    
    -- Call metrics
    calls_attempted INTEGER DEFAULT 0,
    calls_connected INTEGER DEFAULT 0,
    calls_completed INTEGER DEFAULT 0,
    calls_failed INTEGER DEFAULT 0,
    
    -- Outcome metrics
    voicemails INTEGER DEFAULT 0,
    busy_signals INTEGER DEFAULT 0,
    no_answers INTEGER DEFAULT 0,
    opt_outs INTEGER DEFAULT 0,
    
    -- Conversion metrics
    leads_generated INTEGER DEFAULT 0,
    appointments_set INTEGER DEFAULT 0,
    sales_made INTEGER DEFAULT 0,
    
    -- Quality metrics
    average_call_duration DECIMAL(8,2),
    average_sentiment_score DECIMAL(3,2),
    average_lead_score DECIMAL(3,2),
    
    -- Compliance metrics
    dnc_violations INTEGER DEFAULT 0,
    consent_issues INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(campaign_id, date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_contacts_campaign_id ON contacts(campaign_id);
CREATE INDEX IF NOT EXISTS idx_contacts_phone ON contacts(phone);
CREATE INDEX IF NOT EXISTS idx_contacts_status ON contacts(status);
CREATE INDEX IF NOT EXISTS idx_contacts_next_call_at ON contacts(next_call_at);
CREATE INDEX IF NOT EXISTS idx_contacts_lead_score ON contacts(lead_score DESC);

CREATE INDEX IF NOT EXISTS idx_call_records_contact_id ON call_records(contact_id);
CREATE INDEX IF NOT EXISTS idx_call_records_campaign_id ON call_records(campaign_id);
CREATE INDEX IF NOT EXISTS idx_call_records_status ON call_records(status);
CREATE INDEX IF NOT EXISTS idx_call_records_outcome ON call_records(outcome);
CREATE INDEX IF NOT EXISTS idx_call_records_started_at ON call_records(started_at);
CREATE INDEX IF NOT EXISTS idx_call_records_twilio_sid ON call_records(twilio_call_sid);

CREATE INDEX IF NOT EXISTS idx_conversation_turns_call_id ON conversation_turns(call_record_id);
CREATE INDEX IF NOT EXISTS idx_conversation_turns_timestamp ON conversation_turns(timestamp);

CREATE INDEX IF NOT EXISTS idx_dnc_registry_phone ON dnc_registry(phone_number);
CREATE INDEX IF NOT EXISTS idx_dnc_registry_expires_at ON dnc_registry(expires_at);

CREATE INDEX IF NOT EXISTS idx_consent_records_contact_id ON consent_records(contact_id);
CREATE INDEX IF NOT EXISTS idx_consent_records_granted_at ON consent_records(granted_at);

CREATE INDEX IF NOT EXISTS idx_call_queues_campaign_id ON call_queues(campaign_id);
CREATE INDEX IF NOT EXISTS idx_call_queues_status ON call_queues(status);
CREATE INDEX IF NOT EXISTS idx_call_queues_scheduled_at ON call_queues(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_call_queues_priority ON call_queues(priority DESC);

CREATE INDEX IF NOT EXISTS idx_campaign_analytics_campaign_date ON campaign_analytics(campaign_id, date);

-- Full-text search indexes
CREATE INDEX IF NOT EXISTS idx_contacts_search ON contacts USING gin(
    (first_name || ' ' || last_name || ' ' || company) gin_trgm_ops
);

CREATE INDEX IF NOT EXISTS idx_call_records_transcript_search ON call_records USING gin(
    transcript gin_trgm_ops
);

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_call_queues_updated_at BEFORE UPDATE ON call_queues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaign_analytics_updated_at BEFORE UPDATE ON campaign_analytics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE OR REPLACE VIEW active_campaigns AS
SELECT 
    c.*,
    COUNT(co.id) as total_contacts,
    COUNT(CASE WHEN co.status = 'ready' THEN 1 END) as ready_contacts,
    COUNT(CASE WHEN co.status = 'completed' THEN 1 END) as completed_contacts
FROM campaigns c
LEFT JOIN contacts co ON c.id = co.campaign_id
WHERE c.status IN ('active', 'running')
GROUP BY c.id;

CREATE OR REPLACE VIEW call_performance_summary AS
SELECT 
    cr.campaign_id,
    DATE(cr.started_at) as call_date,
    COUNT(*) as total_calls,
    COUNT(CASE WHEN cr.outcome = 'connected' THEN 1 END) as connected_calls,
    COUNT(CASE WHEN cr.outcome = 'voicemail' THEN 1 END) as voicemail_calls,
    COUNT(CASE WHEN cr.outcome = 'no_answer' THEN 1 END) as no_answer_calls,
    COUNT(CASE WHEN cr.outcome = 'busy' THEN 1 END) as busy_calls,
    AVG(cr.duration) as avg_duration,
    AVG(cr.sentiment_score) as avg_sentiment,
    AVG(cr.lead_score) as avg_lead_score
FROM call_records cr
WHERE cr.started_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY cr.campaign_id, DATE(cr.started_at)
ORDER BY call_date DESC;

CREATE OR REPLACE VIEW high_value_contacts AS
SELECT 
    c.*,
    cr.lead_score,
    cr.sentiment_score,
    cr.last_call_at
FROM contacts c
LEFT JOIN (
    SELECT DISTINCT ON (contact_id) 
        contact_id, lead_score, sentiment_score, started_at as last_call_at
    FROM call_records 
    WHERE lead_score >= 7
    ORDER BY contact_id, started_at DESC
) cr ON c.id = cr.contact_id
WHERE c.lead_score >= 7 OR cr.lead_score >= 7
ORDER BY COALESCE(cr.lead_score, c.lead_score) DESC;

-- Functions for common operations
CREATE OR REPLACE FUNCTION get_next_call_time(contact_timezone VARCHAR, calling_hours_start TIME, calling_hours_end TIME)
RETURNS TIMESTAMP WITH TIME ZONE AS $$
DECLARE
    next_time TIMESTAMP WITH TIME ZONE;
    local_time TIME;
BEGIN
    -- Get current time in contact's timezone
    next_time := NOW() AT TIME ZONE contact_timezone;
    local_time := (next_time AT TIME ZONE contact_timezone)::TIME;
    
    -- If within calling hours, return now
    IF local_time BETWEEN calling_hours_start AND calling_hours_end THEN
        RETURN NOW();
    END IF;
    
    -- If after hours, schedule for next day at start time
    IF local_time > calling_hours_end THEN
        next_time := (DATE(next_time) + INTERVAL '1 day' + calling_hours_start::INTERVAL) AT TIME ZONE contact_timezone;
    ELSE
        -- If before hours, schedule for today at start time
        next_time := (DATE(next_time) + calling_hours_start::INTERVAL) AT TIME ZONE contact_timezone;
    END IF;
    
    RETURN next_time AT TIME ZONE 'UTC';
END;
$$ LANGUAGE plpgsql;

-- Sample data for testing (optional)
-- INSERT INTO campaigns (name, description, purpose) VALUES 
-- ('Q1 Lead Generation', 'Quarterly outbound campaign', 'Generate qualified leads for sales team');

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO calling_worker;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO calling_worker;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO calling_worker;