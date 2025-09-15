#!/usr/bin/env python3
"""
FLYFOX AI - Contact Ingestion Worker
Handles contact list processing, validation, and preparation for calling campaigns.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

import aioredis
import asyncpg
import pandas as pd
from pydantic import BaseModel, EmailStr, validator
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContactStatus(str, Enum):
    """Contact processing status"""
    PENDING = "pending"
    VALIDATED = "validated"
    INVALID = "invalid"
    DNC_LIST = "dnc_list"  # Do Not Call
    OPTED_OUT = "opted_out"
    READY = "ready"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ConsentStatus(str, Enum):
    """Consent verification status"""
    UNKNOWN = "unknown"
    EXPLICIT = "explicit"  # Explicit opt-in
    IMPLIED = "implied"    # Business relationship
    REVOKED = "revoked"    # Opted out
    EXPIRED = "expired"    # Consent expired

@dataclass
class Contact:
    """Contact data structure"""
    id: str
    phone: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    industry: Optional[str] = None
    timezone: Optional[str] = None
    status: ContactStatus = ContactStatus.PENDING
    consent_status: ConsentStatus = ConsentStatus.UNKNOWN
    consent_date: Optional[datetime] = None
    source: Optional[str] = None
    tags: List[str] = None
    custom_fields: Dict[str, Any] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.custom_fields is None:
            self.custom_fields = {}
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc)

class ContactValidator:
    """Validates and normalizes contact data"""
    
    def __init__(self, twilio_client: TwilioClient):
        self.twilio = twilio_client
        self.dnc_cache = set()  # Cache for DNC lookups
        
    async def validate_phone(self, phone: str) -> tuple[bool, str]:
        """Validate phone number using Twilio Lookup API"""
        try:
            # Normalize phone number
            normalized = self._normalize_phone(phone)
            
            # Use Twilio Lookup API
            lookup = self.twilio.lookups.phone_numbers(normalized).fetch(
                type=['carrier', 'caller-name']
            )
            
            return True, lookup.phone_number
            
        except TwilioException as e:
            logger.warning(f"Phone validation failed for {phone}: {e}")
            return False, phone
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number format"""
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        
        # Add country code if missing (assume US)
        if len(digits) == 10:
            digits = '1' + digits
        elif len(digits) == 11 and digits[0] == '1':
            pass  # Already has country code
        else:
            raise ValueError(f"Invalid phone number format: {phone}")
            
        return f"+{digits}"
    
    async def check_dnc_list(self, phone: str) -> bool:
        """Check if phone is on Do Not Call list"""
        # In production, integrate with official DNC registries
        # For now, use a simple cache-based approach
        normalized = self._normalize_phone(phone)
        return normalized in self.dnc_cache
    
    async def validate_consent(self, contact: Contact) -> ConsentStatus:
        """Validate consent status for contact"""
        # Check if consent is explicitly recorded
        if contact.consent_status == ConsentStatus.EXPLICIT:
            # Check if consent is still valid (not expired)
            if contact.consent_date:
                days_since_consent = (datetime.now(timezone.utc) - contact.consent_date).days
                if days_since_consent > 365:  # 1 year expiry
                    return ConsentStatus.EXPIRED
            return ConsentStatus.EXPLICIT
        
        # Check for business relationship (implied consent)
        if contact.source in ['customer', 'lead', 'inquiry']:
            return ConsentStatus.IMPLIED
        
        return ConsentStatus.UNKNOWN

class ContactIngestionWorker:
    """Main worker for contact ingestion and processing"""
    
    def __init__(self):
        self.redis = None
        self.db_pool = None
        self.twilio = TwilioClient(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        self.validator = ContactValidator(self.twilio)
        self.running = False
        
    async def initialize(self):
        """Initialize connections"""
        # Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis = await aioredis.from_url(redis_url)
        
        # PostgreSQL connection pool
        db_url = os.getenv('DATABASE_URL')
        self.db_pool = await asyncpg.create_pool(db_url, min_size=5, max_size=20)
        
        logger.info("Contact ingestion worker initialized")
    
    async def process_contact_list(self, file_path: str, campaign_id: str) -> Dict[str, int]:
        """Process a contact list file"""
        stats = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'dnc': 0,
            'no_consent': 0
        }
        
        try:
            # Read contact file (supports CSV, Excel)
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            
            stats['total'] = len(df)
            logger.info(f"Processing {stats['total']} contacts from {file_path}")
            
            # Process contacts in batches
            batch_size = 100
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                batch_stats = await self._process_contact_batch(batch, campaign_id)
                
                # Update stats
                for key in stats:
                    if key != 'total':
                        stats[key] += batch_stats.get(key, 0)
                
                # Log progress
                processed = min(i + batch_size, len(df))
                logger.info(f"Processed {processed}/{stats['total']} contacts")
            
            logger.info(f"Contact processing complete: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error processing contact list: {e}")
            raise
    
    async def _process_contact_batch(self, batch_df: pd.DataFrame, campaign_id: str) -> Dict[str, int]:
        """Process a batch of contacts"""
        stats = {'valid': 0, 'invalid': 0, 'dnc': 0, 'no_consent': 0}
        
        contacts = []
        for _, row in batch_df.iterrows():
            try:
                # Create contact from row data
                contact = Contact(
                    id=str(uuid.uuid4()),
                    phone=str(row.get('phone', '')),
                    email=row.get('email'),
                    first_name=row.get('first_name'),
                    last_name=row.get('last_name'),
                    company=row.get('company'),
                    title=row.get('title'),
                    industry=row.get('industry'),
                    timezone=row.get('timezone', 'America/New_York'),
                    source=row.get('source', 'import')
                )
                
                # Validate phone number
                is_valid, normalized_phone = await self.validator.validate_phone(contact.phone)
                if not is_valid:
                    contact.status = ContactStatus.INVALID
                    stats['invalid'] += 1
                    continue
                
                contact.phone = normalized_phone
                
                # Check DNC list
                if await self.validator.check_dnc_list(contact.phone):
                    contact.status = ContactStatus.DNC_LIST
                    stats['dnc'] += 1
                    continue
                
                # Validate consent
                consent_status = await self.validator.validate_consent(contact)
                contact.consent_status = consent_status
                
                if consent_status in [ConsentStatus.REVOKED, ConsentStatus.UNKNOWN]:
                    contact.status = ContactStatus.INVALID
                    stats['no_consent'] += 1
                    continue
                
                # Mark as ready for calling
                contact.status = ContactStatus.READY
                stats['valid'] += 1
                contacts.append(contact)
                
            except Exception as e:
                logger.error(f"Error processing contact row: {e}")
                stats['invalid'] += 1
        
        # Save valid contacts to database
        if contacts:
            await self._save_contacts(contacts, campaign_id)
        
        return stats
    
    async def _save_contacts(self, contacts: List[Contact], campaign_id: str):
        """Save contacts to database"""
        async with self.db_pool.acquire() as conn:
            # Prepare batch insert
            contact_data = []
            for contact in contacts:
                contact_data.append((
                    contact.id,
                    campaign_id,
                    contact.phone,
                    contact.email,
                    contact.first_name,
                    contact.last_name,
                    contact.company,
                    contact.title,
                    contact.industry,
                    contact.timezone,
                    contact.status.value,
                    contact.consent_status.value,
                    contact.consent_date,
                    contact.source,
                    json.dumps(contact.tags),
                    json.dumps(contact.custom_fields),
                    contact.created_at,
                    contact.updated_at
                ))
            
            # Batch insert
            await conn.executemany("""
                INSERT INTO contacts (
                    id, campaign_id, phone, email, first_name, last_name,
                    company, title, industry, timezone, status, consent_status,
                    consent_date, source, tags, custom_fields, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
            """, contact_data)
            
            # Queue contacts for calling
            for contact in contacts:
                await self.redis.lpush(
                    f"calling_queue:{campaign_id}",
                    json.dumps(asdict(contact))
                )
    
    async def run(self):
        """Main worker loop"""
        self.running = True
        logger.info("Contact ingestion worker started")
        
        while self.running:
            try:
                # Listen for ingestion jobs
                job_data = await self.redis.brpop('contact_ingestion_queue', timeout=5)
                
                if job_data:
                    _, job_json = job_data
                    job = json.loads(job_json)
                    
                    logger.info(f"Processing ingestion job: {job['id']}")
                    
                    # Process the contact list
                    stats = await self.process_contact_list(
                        job['file_path'],
                        job['campaign_id']
                    )
                    
                    # Update job status
                    await self.redis.hset(
                        f"job:{job['id']}",
                        mapping={
                            'status': 'completed',
                            'stats': json.dumps(stats),
                            'completed_at': datetime.now(timezone.utc).isoformat()
                        }
                    )
                    
                    logger.info(f"Ingestion job {job['id']} completed: {stats}")
                    
            except Exception as e:
                logger.error(f"Error in ingestion worker: {e}")
                await asyncio.sleep(5)
    
    async def stop(self):
        """Stop the worker"""
        self.running = False
        if self.redis:
            await self.redis.close()
        if self.db_pool:
            await self.db_pool.close()
        logger.info("Contact ingestion worker stopped")

async def main():
    """Main entry point"""
    worker = ContactIngestionWorker()
    
    try:
        await worker.initialize()
        await worker.run()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        await worker.stop()

if __name__ == "__main__":
    asyncio.run(main())