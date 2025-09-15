"""Initial migration - create all tables

Revision ID: 001
Revises: 
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    # Create partners table
    op.create_table('partners',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('company_size', sa.String(length=50), nullable=True),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('tier', sa.String(length=50), nullable=False),
        sa.Column('api_key', sa.String(length=255), nullable=True),
        sa.Column('api_secret_hash', sa.String(length=255), nullable=True),
        sa.Column('webhook_url', sa.String(length=500), nullable=True),
        sa.Column('webhook_secret', sa.String(length=255), nullable=True),
        sa.Column('quantum_credits', sa.Integer(), nullable=False),
        sa.Column('credits_used', sa.Integer(), nullable=False),
        sa.Column('monthly_limit', sa.Integer(), nullable=True),
        sa.Column('stripe_customer_id', sa.String(length=255), nullable=True),
        sa.Column('stripe_account_id', sa.String(length=255), nullable=True),
        sa.Column('billing_email', sa.String(length=255), nullable=True),
        sa.Column('rate_limit_per_minute', sa.Integer(), nullable=False),
        sa.Column('rate_limit_per_hour', sa.Integer(), nullable=False),
        sa.Column('allowed_ips', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('cors_origins', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('white_label_enabled', sa.Boolean(), nullable=False),
        sa.Column('custom_domain', sa.String(length=255), nullable=True),
        sa.Column('brand_colors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('logo_url', sa.String(length=500), nullable=True),
        sa.Column('custom_css', sa.Text(), nullable=True),
        sa.Column('salesforce_enabled', sa.Boolean(), nullable=False),
        sa.Column('salesforce_instance_url', sa.String(length=255), nullable=True),
        sa.Column('salesforce_client_id', sa.String(length=255), nullable=True),
        sa.Column('hubspot_enabled', sa.Boolean(), nullable=False),
        sa.Column('hubspot_portal_id', sa.String(length=100), nullable=True),
        sa.Column('hubspot_api_key_hash', sa.String(length=255), nullable=True),
        sa.Column('zapier_enabled', sa.Boolean(), nullable=False),
        sa.Column('zapier_webhook_url', sa.String(length=500), nullable=True),
        sa.Column('gdpr_compliant', sa.Boolean(), nullable=False),
        sa.Column('ccpa_compliant', sa.Boolean(), nullable=False),
        sa.Column('data_retention_days', sa.Integer(), nullable=False),
        sa.Column('trial_ends_at', sa.DateTime(), nullable=True),
        sa.Column('onboarding_completed', sa.Boolean(), nullable=False),
        sa.Column('onboarding_step', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('pk_partners'),
        sa.UniqueConstraint('uq_partners_slug'),
        sa.UniqueConstraint('uq_partners_email'),
        sa.UniqueConstraint('uq_partners_api_key')
    )
    op.create_index('ix_partners_status', 'partners', ['status'])
    op.create_index('ix_partners_tier', 'partners', ['tier'])
    op.create_index('ix_partners_industry', 'partners', ['industry'])
    op.create_index('ix_partners_country', 'partners', ['country'])
    op.create_index('ix_partners_trial_ends_at', 'partners', ['trial_ends_at'])

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('partner_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=False),
        sa.Column('theme', sa.String(length=20), nullable=False),
        sa.Column('notifications_enabled', sa.Boolean(), nullable=False),
        sa.Column('oauth_provider', sa.String(length=50), nullable=True),
        sa.Column('oauth_id', sa.String(length=255), nullable=True),
        sa.Column('oauth_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('last_login_ip', sa.String(length=45), nullable=True),
        sa.Column('login_count', sa.Integer(), nullable=False),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False),
        sa.Column('locked_until', sa.DateTime(), nullable=True),
        sa.Column('session_token', sa.String(length=255), nullable=True),
        sa.Column('session_expires_at', sa.DateTime(), nullable=True),
        sa.Column('totp_secret', sa.String(length=255), nullable=True),
        sa.Column('totp_enabled', sa.Boolean(), nullable=False),
        sa.Column('backup_codes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('email_verification_token', sa.String(length=255), nullable=True),
        sa.Column('email_verification_expires_at', sa.DateTime(), nullable=True),
        sa.Column('password_reset_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_expires_at', sa.DateTime(), nullable=True),
        sa.Column('api_access_enabled', sa.Boolean(), nullable=False),
        sa.Column('api_rate_limit', sa.Integer(), nullable=True),
        sa.Column('api_last_used_at', sa.DateTime(), nullable=True),
        sa.Column('onboarding_completed', sa.Boolean(), nullable=False),
        sa.Column('onboarding_step', sa.String(length=100), nullable=True),
        sa.Column('training_completed', sa.Boolean(), nullable=False),
        sa.Column('last_training_at', sa.DateTime(), nullable=True),
        sa.Column('gdpr_consent', sa.Boolean(), nullable=True),
        sa.Column('gdpr_consent_date', sa.DateTime(), nullable=True),
        sa.Column('marketing_consent', sa.Boolean(), nullable=False),
        sa.Column('data_processing_consent', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], name='fk_users_partner_id_partners'),
        sa.PrimaryKeyConstraint('pk_users'),
        sa.UniqueConstraint('uq_users_email'),
        sa.UniqueConstraint('uq_users_username')
    )
    op.create_index('ix_users_partner_id', 'users', ['partner_id'])
    op.create_index('ix_users_role', 'users', ['role'])
    op.create_index('ix_users_is_active', 'users', ['is_active'])
    op.create_index('ix_users_last_login_at', 'users', ['last_login_at'])

    # Create leads table
    op.create_table('leads',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('partner_id', sa.String(), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('company_size', sa.String(length=50), nullable=True),
        sa.Column('annual_revenue', sa.String(length=50), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('linkedin_url', sa.String(length=255), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('postal_code', sa.String(length=20), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('stage', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=False),
        sa.Column('temperature', sa.String(length=20), nullable=False),
        sa.Column('qualification_score', sa.Integer(), nullable=True),
        sa.Column('budget_range', sa.String(length=50), nullable=True),
        sa.Column('decision_timeframe', sa.String(length=50), nullable=True),
        sa.Column('pain_points', sa.Text(), nullable=True),
        sa.Column('quantum_score', sa.Numeric(precision=8, scale=4), nullable=True),
        sa.Column('quantum_confidence', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('quantum_last_calculated', sa.DateTime(), nullable=True),
        sa.Column('quantum_factors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('page_views', sa.Integer(), nullable=False),
        sa.Column('email_opens', sa.Integer(), nullable=False),
        sa.Column('email_clicks', sa.Integer(), nullable=False),
        sa.Column('form_submissions', sa.Integer(), nullable=False),
        sa.Column('content_downloads', sa.Integer(), nullable=False),
        sa.Column('webinar_attendance', sa.Integer(), nullable=False),
        sa.Column('demo_requests', sa.Integer(), nullable=False),
        sa.Column('last_activity_at', sa.DateTime(), nullable=True),
        sa.Column('last_email_at', sa.DateTime(), nullable=True),
        sa.Column('last_call_at', sa.DateTime(), nullable=True),
        sa.Column('next_follow_up_at', sa.DateTime(), nullable=True),
        sa.Column('engagement_score', sa.Integer(), nullable=False),
        sa.Column('response_rate', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('custom_fields', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tcpa_consent', sa.Boolean(), nullable=False),
        sa.Column('tcpa_consent_date', sa.DateTime(), nullable=True),
        sa.Column('tcpa_consent_method', sa.String(length=50), nullable=True),
        sa.Column('marketing_consent', sa.Boolean(), nullable=False),
        sa.Column('gdpr_consent', sa.Boolean(), nullable=True),
        sa.Column('estimated_value', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('actual_value', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('probability', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('expected_close_date', sa.DateTime(), nullable=True),
        sa.Column('assigned_to', sa.String(), nullable=True),
        sa.Column('assigned_at', sa.DateTime(), nullable=True),
        sa.Column('assignment_method', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], name='fk_leads_assigned_to_users'),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], name='fk_leads_partner_id_partners'),
        sa.PrimaryKeyConstraint('pk_leads')
    )
    op.create_index('ix_leads_partner_id', 'leads', ['partner_id'])
    op.create_index('ix_leads_external_id', 'leads', ['external_id'])
    op.create_index('ix_leads_email', 'leads', ['email'])
    op.create_index('ix_leads_status', 'leads', ['status'])
    op.create_index('ix_leads_stage', 'leads', ['stage'])
    op.create_index('ix_leads_priority', 'leads', ['priority'])
    op.create_index('ix_leads_quantum_score', 'leads', ['quantum_score'])
    op.create_index('ix_leads_assigned_to', 'leads', ['assigned_to'])

    # Create oracle_queries table
    op.create_table('oracle_queries',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('partner_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('lead_id', sa.String(), nullable=True),
        sa.Column('query_type', sa.String(length=100), nullable=False),
        sa.Column('query_text', sa.Text(), nullable=True),
        sa.Column('query_parameters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('input_hash', sa.String(length=64), nullable=True),
        sa.Column('dynex_job_id', sa.String(length=255), nullable=True),
        sa.Column('qubo_matrix', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('quantum_algorithm', sa.String(length=100), nullable=False),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('prophecy', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('recommended_action', sa.Text(), nullable=True),
        sa.Column('explainability', sa.Text(), nullable=True),
        sa.Column('score', sa.Numeric(precision=8, scale=4), nullable=True),
        sa.Column('probability', sa.Numeric(precision=5, scale=4), nullable=True),
        sa.Column('risk_level', sa.String(length=50), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=False),
        sa.Column('api_version', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False),
        sa.Column('queue_time_ms', sa.Integer(), nullable=True),
        sa.Column('execution_time_ms', sa.Integer(), nullable=True),
        sa.Column('total_time_ms', sa.Integer(), nullable=True),
        sa.Column('quantum_credits_used', sa.Integer(), nullable=False),
        sa.Column('cost_usd', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('cached_result', sa.Boolean(), nullable=False),
        sa.Column('cache_hit', sa.Boolean(), nullable=False),
        sa.Column('cache_expires_at', sa.DateTime(), nullable=True),
        sa.Column('feedback_rating', sa.Integer(), nullable=True),
        sa.Column('feedback_comment', sa.Text(), nullable=True),
        sa.Column('accuracy_verified', sa.Boolean(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('request_id', sa.String(length=255), nullable=True),
        sa.Column('business_impact', sa.String(length=50), nullable=True),
        sa.Column('urgency', sa.String(length=50), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], name='fk_oracle_queries_lead_id_leads'),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], name='fk_oracle_queries_partner_id_partners'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_oracle_queries_user_id_users'),
        sa.PrimaryKeyConstraint('pk_oracle_queries')
    )
    op.create_index('ix_oracle_queries_partner_id', 'oracle_queries', ['partner_id'])
    op.create_index('ix_oracle_queries_user_id', 'oracle_queries', ['user_id'])
    op.create_index('ix_oracle_queries_lead_id', 'oracle_queries', ['lead_id'])
    op.create_index('ix_oracle_queries_query_type', 'oracle_queries', ['query_type'])
    op.create_index('ix_oracle_queries_input_hash', 'oracle_queries', ['input_hash'])
    op.create_index('ix_oracle_queries_dynex_job_id', 'oracle_queries', ['dynex_job_id'])
    op.create_index('ix_oracle_queries_request_id', 'oracle_queries', ['request_id'])

    # Create quantum_credits table
    op.create_table('quantum_credits',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('partner_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('oracle_query_id', sa.String(), nullable=True),
        sa.Column('transaction_type', sa.String(length=50), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('balance_before', sa.Integer(), nullable=False),
        sa.Column('balance_after', sa.Integer(), nullable=False),
        sa.Column('unit_cost_usd', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('total_cost_usd', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('purchase_order_id', sa.String(length=255), nullable=True),
        sa.Column('stripe_payment_intent_id', sa.String(length=255), nullable=True),
        sa.Column('stripe_invoice_id', sa.String(length=255), nullable=True),
        sa.Column('billing_period_start', sa.DateTime(), nullable=True),
        sa.Column('billing_period_end', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('expired', sa.Boolean(), nullable=False),
        sa.Column('refund_amount', sa.Integer(), nullable=True),
        sa.Column('refund_reason', sa.String(length=255), nullable=True),
        sa.Column('refunded_at', sa.DateTime(), nullable=True),
        sa.Column('refund_transaction_id', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('transaction_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('approved_by', sa.String(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], name='fk_quantum_credits_approved_by_users'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], name='fk_quantum_credits_created_by_users'),
        sa.ForeignKeyConstraint(['oracle_query_id'], ['oracle_queries.id'], name='fk_quantum_credits_oracle_query_id_oracle_queries'),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], name='fk_quantum_credits_partner_id_partners'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_quantum_credits_user_id_users'),
        sa.PrimaryKeyConstraint('pk_quantum_credits')
    )
    op.create_index('ix_quantum_credits_partner_id', 'quantum_credits', ['partner_id'])
    op.create_index('ix_quantum_credits_user_id', 'quantum_credits', ['user_id'])
    op.create_index('ix_quantum_credits_transaction_type', 'quantum_credits', ['transaction_type'])
    op.create_index('ix_quantum_credits_expires_at', 'quantum_credits', ['expires_at'])

    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('partner_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('event_category', sa.String(length=50), nullable=False),
        sa.Column('event_description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('resource_type', sa.String(length=100), nullable=True),
        sa.Column('resource_id', sa.String(length=255), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('outcome', sa.String(length=50), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('request_id', sa.String(length=255), nullable=True),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('api_endpoint', sa.String(length=255), nullable=True),
        sa.Column('http_method', sa.String(length=10), nullable=True),
        sa.Column('response_status', sa.Integer(), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('old_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('new_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('changed_fields', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('compliance_flags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('gdpr_relevant', sa.Boolean(), nullable=False),
        sa.Column('pii_involved', sa.Boolean(), nullable=False),
        sa.Column('retention_period_days', sa.Integer(), nullable=False),
        sa.Column('event_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], name='fk_audit_logs_partner_id_partners'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_audit_logs_user_id_users'),
        sa.PrimaryKeyConstraint('pk_audit_logs')
    )
    op.create_index('ix_audit_logs_partner_id', 'audit_logs', ['partner_id'])
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('ix_audit_logs_event_type', 'audit_logs', ['event_type'])
    op.create_index('ix_audit_logs_event_category', 'audit_logs', ['event_category'])
    op.create_index('ix_audit_logs_severity', 'audit_logs', ['severity'])
    op.create_index('ix_audit_logs_resource_type', 'audit_logs', ['resource_type'])
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('ix_audit_logs_outcome', 'audit_logs', ['outcome'])
    op.create_index('ix_audit_logs_request_id', 'audit_logs', ['request_id'])


def downgrade() -> None:
    """Downgrade database schema."""
    op.drop_table('audit_logs')
    op.drop_table('quantum_credits')
    op.drop_table('oracle_queries')
    op.drop_table('leads')
    op.drop_table('users')
    op.drop_table('partners')