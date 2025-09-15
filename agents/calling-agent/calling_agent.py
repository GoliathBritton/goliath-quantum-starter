#!/usr/bin/env python3
"""
Quantum Nexus Platform - Calling Agent Pilot

A sophisticated calling agent system with:
- 2M+ contact management and integration
- Intelligent dialing and call routing
- Real-time conversation analysis
- CRM integration and lead scoring
- Automated follow-up and scheduling
- Performance analytics and reporting

Features:
- Multi-channel communication (voice, SMS, email)
- AI-powered conversation insights
- Dynamic script generation
- Call outcome prediction
- Compliance and recording management
"""

import asyncio
import json
import logging
import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from pathlib import Path
import sqlite3
import csv
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CallStatus(Enum):
    """Call status enumeration"""
    PENDING = "pending"
    DIALING = "dialing"
    CONNECTED = "connected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no_answer"
    BUSY = "busy"
    VOICEMAIL = "voicemail"
    CALLBACK_REQUESTED = "callback_requested"

class ContactStatus(Enum):
    """Contact status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DO_NOT_CALL = "do_not_call"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    FOLLOW_UP = "follow_up"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"

class CallOutcome(Enum):
    """Call outcome enumeration"""
    SALE = "sale"
    APPOINTMENT = "appointment"
    FOLLOW_UP = "follow_up"
    NOT_INTERESTED = "not_interested"
    CALLBACK = "callback"
    VOICEMAIL_LEFT = "voicemail_left"
    WRONG_NUMBER = "wrong_number"
    TECHNICAL_ISSUE = "technical_issue"

class Priority(Enum):
    """Priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

@dataclass
class Contact:
    """Contact data model"""
    id: str
    first_name: str
    last_name: str
    phone: str
    email: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    industry: Optional[str] = None
    status: ContactStatus = ContactStatus.ACTIVE
    priority: Priority = Priority.MEDIUM
    lead_score: float = 0.0
    last_contacted: Optional[datetime.datetime] = None
    next_follow_up: Optional[datetime.datetime] = None
    notes: Optional[str] = None
    tags: List[str] = None
    custom_fields: Dict[str, Any] = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.custom_fields is None:
            self.custom_fields = {}
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.datetime.utcnow()

@dataclass
class CallRecord:
    """Call record data model"""
    id: str
    contact_id: str
    agent_id: str
    campaign_id: Optional[str]
    status: CallStatus
    outcome: Optional[CallOutcome]
    start_time: Optional[datetime.datetime]
    end_time: Optional[datetime.datetime]
    duration: Optional[int]  # seconds
    recording_url: Optional[str]
    transcript: Optional[str]
    notes: Optional[str]
    follow_up_required: bool = False
    follow_up_date: Optional[datetime.datetime] = None
    lead_score_change: float = 0.0
    created_at: datetime.datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()

@dataclass
class Campaign:
    """Campaign data model"""
    id: str
    name: str
    description: str
    script_template: str
    target_contacts: List[str]  # contact IDs
    status: str = "active"  # active, paused, completed
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None
    goals: Dict[str, Any] = None
    metrics: Dict[str, Any] = None
    created_at: datetime.datetime = None
    
    def __post_init__(self):
        if self.goals is None:
            self.goals = {}
        if self.metrics is None:
            self.metrics = {}
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()

class ContactManager:
    """Manages contact database and operations"""
    
    def __init__(self, db_path: str = "contacts.db"):
        self.db_path = db_path
        self.contacts: Dict[str, Contact] = {}
        self._init_database()
        self._load_contacts()
    
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create contacts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                company TEXT,
                title TEXT,
                industry TEXT,
                status TEXT DEFAULT 'active',
                priority INTEGER DEFAULT 2,
                lead_score REAL DEFAULT 0.0,
                last_contacted TIMESTAMP,
                next_follow_up TIMESTAMP,
                notes TEXT,
                tags TEXT,  -- JSON array
                custom_fields TEXT,  -- JSON object
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_phone ON contacts(phone)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON contacts(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON contacts(priority)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lead_score ON contacts(lead_score)")
        
        conn.commit()
        conn.close()
    
    def _load_contacts(self):
        """Load contacts from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        
        for row in rows:
            contact = Contact(
                id=row[0],
                first_name=row[1],
                last_name=row[2],
                phone=row[3],
                email=row[4],
                company=row[5],
                title=row[6],
                industry=row[7],
                status=ContactStatus(row[8]),
                priority=Priority(row[9]),
                lead_score=row[10],
                last_contacted=datetime.datetime.fromisoformat(row[11]) if row[11] else None,
                next_follow_up=datetime.datetime.fromisoformat(row[12]) if row[12] else None,
                notes=row[13],
                tags=json.loads(row[14]) if row[14] else [],
                custom_fields=json.loads(row[15]) if row[15] else {},
                created_at=datetime.datetime.fromisoformat(row[16]),
                updated_at=datetime.datetime.fromisoformat(row[17])
            )
            self.contacts[contact.id] = contact
        
        conn.close()
        logger.info(f"Loaded {len(self.contacts)} contacts from database")
    
    def add_contact(self, contact: Contact) -> bool:
        """Add a new contact"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO contacts (
                    id, first_name, last_name, phone, email, company, title, industry,
                    status, priority, lead_score, last_contacted, next_follow_up, notes,
                    tags, custom_fields, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contact.id, contact.first_name, contact.last_name, contact.phone,
                contact.email, contact.company, contact.title, contact.industry,
                contact.status.value, contact.priority.value, contact.lead_score,
                contact.last_contacted.isoformat() if contact.last_contacted else None,
                contact.next_follow_up.isoformat() if contact.next_follow_up else None,
                contact.notes, json.dumps(contact.tags), json.dumps(contact.custom_fields),
                contact.created_at.isoformat(), contact.updated_at.isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            self.contacts[contact.id] = contact
            logger.info(f"Added contact: {contact.first_name} {contact.last_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding contact: {e}")
            return False
    
    def update_contact(self, contact: Contact) -> bool:
        """Update an existing contact"""
        try:
            contact.updated_at = datetime.datetime.utcnow()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE contacts SET
                    first_name=?, last_name=?, phone=?, email=?, company=?, title=?, industry=?,
                    status=?, priority=?, lead_score=?, last_contacted=?, next_follow_up=?, notes=?,
                    tags=?, custom_fields=?, updated_at=?
                WHERE id=?
            """, (
                contact.first_name, contact.last_name, contact.phone, contact.email,
                contact.company, contact.title, contact.industry, contact.status.value,
                contact.priority.value, contact.lead_score,
                contact.last_contacted.isoformat() if contact.last_contacted else None,
                contact.next_follow_up.isoformat() if contact.next_follow_up else None,
                contact.notes, json.dumps(contact.tags), json.dumps(contact.custom_fields),
                contact.updated_at.isoformat(), contact.id
            ))
            
            conn.commit()
            conn.close()
            
            self.contacts[contact.id] = contact
            logger.info(f"Updated contact: {contact.first_name} {contact.last_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating contact: {e}")
            return False
    
    def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get contact by ID"""
        return self.contacts.get(contact_id)
    
    def search_contacts(self, query: str, limit: int = 100) -> List[Contact]:
        """Search contacts by name, phone, email, or company"""
        results = []
        query_lower = query.lower()
        
        for contact in self.contacts.values():
            if (
                query_lower in contact.first_name.lower() or
                query_lower in contact.last_name.lower() or
                query_lower in contact.phone or
                (contact.email and query_lower in contact.email.lower()) or
                (contact.company and query_lower in contact.company.lower())
            ):
                results.append(contact)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_contacts_by_status(self, status: ContactStatus, limit: int = 1000) -> List[Contact]:
        """Get contacts by status"""
        return [c for c in self.contacts.values() if c.status == status][:limit]
    
    def get_high_priority_contacts(self, limit: int = 100) -> List[Contact]:
        """Get high priority contacts for calling"""
        contacts = list(self.contacts.values())
        # Sort by priority (descending) and lead score (descending)
        contacts.sort(key=lambda c: (c.priority.value, c.lead_score), reverse=True)
        return contacts[:limit]
    
    def import_contacts_from_csv(self, csv_path: str) -> int:
        """Import contacts from CSV file"""
        imported_count = 0
        
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    contact = Contact(
                        id=str(uuid.uuid4()),
                        first_name=row.get('first_name', ''),
                        last_name=row.get('last_name', ''),
                        phone=row.get('phone', ''),
                        email=row.get('email'),
                        company=row.get('company'),
                        title=row.get('title'),
                        industry=row.get('industry'),
                        status=ContactStatus(row.get('status', 'active')),
                        priority=Priority(int(row.get('priority', 2))),
                        lead_score=float(row.get('lead_score', 0.0))
                    )
                    
                    if self.add_contact(contact):
                        imported_count += 1
                        
        except Exception as e:
            logger.error(f"Error importing contacts: {e}")
        
        logger.info(f"Imported {imported_count} contacts from {csv_path}")
        return imported_count
    
    def export_contacts_to_csv(self, csv_path: str) -> bool:
        """Export contacts to CSV file"""
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'first_name', 'last_name', 'phone', 'email', 'company',
                    'title', 'industry', 'status', 'priority', 'lead_score',
                    'last_contacted', 'next_follow_up', 'notes', 'created_at'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for contact in self.contacts.values():
                    writer.writerow({
                        'id': contact.id,
                        'first_name': contact.first_name,
                        'last_name': contact.last_name,
                        'phone': contact.phone,
                        'email': contact.email,
                        'company': contact.company,
                        'title': contact.title,
                        'industry': contact.industry,
                        'status': contact.status.value,
                        'priority': contact.priority.value,
                        'lead_score': contact.lead_score,
                        'last_contacted': contact.last_contacted.isoformat() if contact.last_contacted else '',
                        'next_follow_up': contact.next_follow_up.isoformat() if contact.next_follow_up else '',
                        'notes': contact.notes or '',
                        'created_at': contact.created_at.isoformat()
                    })
            
            logger.info(f"Exported {len(self.contacts)} contacts to {csv_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting contacts: {e}")
            return False

class CallManager:
    """Manages call operations and records"""
    
    def __init__(self, db_path: str = "calls.db"):
        self.db_path = db_path
        self.active_calls: Dict[str, CallRecord] = {}
        self.call_history: Dict[str, CallRecord] = {}
        self._init_database()
        self._load_call_history()
    
    def _init_database(self):
        """Initialize call records database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS call_records (
                id TEXT PRIMARY KEY,
                contact_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                campaign_id TEXT,
                status TEXT NOT NULL,
                outcome TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration INTEGER,
                recording_url TEXT,
                transcript TEXT,
                notes TEXT,
                follow_up_required BOOLEAN DEFAULT 0,
                follow_up_date TIMESTAMP,
                lead_score_change REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_contact_id ON call_records(contact_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent_id ON call_records(agent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON call_records(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON call_records(created_at)")
        
        conn.commit()
        conn.close()
    
    def _load_call_history(self):
        """Load call history from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM call_records ORDER BY created_at DESC LIMIT 10000")
        rows = cursor.fetchall()
        
        for row in rows:
            call_record = CallRecord(
                id=row[0],
                contact_id=row[1],
                agent_id=row[2],
                campaign_id=row[3],
                status=CallStatus(row[4]),
                outcome=CallOutcome(row[5]) if row[5] else None,
                start_time=datetime.datetime.fromisoformat(row[6]) if row[6] else None,
                end_time=datetime.datetime.fromisoformat(row[7]) if row[7] else None,
                duration=row[8],
                recording_url=row[9],
                transcript=row[10],
                notes=row[11],
                follow_up_required=bool(row[12]),
                follow_up_date=datetime.datetime.fromisoformat(row[13]) if row[13] else None,
                lead_score_change=row[14],
                created_at=datetime.datetime.fromisoformat(row[15])
            )
            self.call_history[call_record.id] = call_record
        
        conn.close()
        logger.info(f"Loaded {len(self.call_history)} call records from database")
    
    def start_call(self, contact_id: str, agent_id: str, campaign_id: Optional[str] = None) -> str:
        """Start a new call"""
        call_id = str(uuid.uuid4())
        
        call_record = CallRecord(
            id=call_id,
            contact_id=contact_id,
            agent_id=agent_id,
            campaign_id=campaign_id,
            status=CallStatus.DIALING,
            start_time=datetime.datetime.utcnow()
        )
        
        self.active_calls[call_id] = call_record
        self._save_call_record(call_record)
        
        logger.info(f"Started call {call_id} for contact {contact_id}")
        return call_id
    
    def update_call_status(self, call_id: str, status: CallStatus, 
                          outcome: Optional[CallOutcome] = None,
                          notes: Optional[str] = None) -> bool:
        """Update call status"""
        if call_id not in self.active_calls:
            logger.error(f"Call {call_id} not found in active calls")
            return False
        
        call_record = self.active_calls[call_id]
        call_record.status = status
        
        if outcome:
            call_record.outcome = outcome
        
        if notes:
            call_record.notes = notes
        
        if status in [CallStatus.COMPLETED, CallStatus.FAILED, CallStatus.NO_ANSWER, CallStatus.BUSY]:
            call_record.end_time = datetime.datetime.utcnow()
            if call_record.start_time:
                call_record.duration = int((call_record.end_time - call_record.start_time).total_seconds())
            
            # Move to history
            self.call_history[call_id] = call_record
            del self.active_calls[call_id]
        
        self._save_call_record(call_record)
        logger.info(f"Updated call {call_id} status to {status.value}")
        return True
    
    def _save_call_record(self, call_record: CallRecord):
        """Save call record to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO call_records (
                    id, contact_id, agent_id, campaign_id, status, outcome,
                    start_time, end_time, duration, recording_url, transcript, notes,
                    follow_up_required, follow_up_date, lead_score_change, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                call_record.id, call_record.contact_id, call_record.agent_id,
                call_record.campaign_id, call_record.status.value,
                call_record.outcome.value if call_record.outcome else None,
                call_record.start_time.isoformat() if call_record.start_time else None,
                call_record.end_time.isoformat() if call_record.end_time else None,
                call_record.duration, call_record.recording_url, call_record.transcript,
                call_record.notes, call_record.follow_up_required,
                call_record.follow_up_date.isoformat() if call_record.follow_up_date else None,
                call_record.lead_score_change, call_record.created_at.isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving call record: {e}")
    
    def get_call_statistics(self, agent_id: Optional[str] = None, 
                           start_date: Optional[datetime.datetime] = None,
                           end_date: Optional[datetime.datetime] = None) -> Dict[str, Any]:
        """Get call statistics"""
        calls = list(self.call_history.values())
        
        # Filter by agent
        if agent_id:
            calls = [c for c in calls if c.agent_id == agent_id]
        
        # Filter by date range
        if start_date:
            calls = [c for c in calls if c.created_at >= start_date]
        if end_date:
            calls = [c for c in calls if c.created_at <= end_date]
        
        total_calls = len(calls)
        if total_calls == 0:
            return {"total_calls": 0}
        
        # Calculate statistics
        completed_calls = [c for c in calls if c.status == CallStatus.COMPLETED]
        connected_calls = [c for c in calls if c.status in [CallStatus.COMPLETED, CallStatus.CONNECTED]]
        
        total_duration = sum(c.duration or 0 for c in completed_calls)
        avg_duration = total_duration / len(completed_calls) if completed_calls else 0
        
        # Outcome statistics
        outcomes = {}
        for call in calls:
            if call.outcome:
                outcomes[call.outcome.value] = outcomes.get(call.outcome.value, 0) + 1
        
        return {
            "total_calls": total_calls,
            "completed_calls": len(completed_calls),
            "connected_calls": len(connected_calls),
            "connection_rate": len(connected_calls) / total_calls * 100,
            "completion_rate": len(completed_calls) / total_calls * 100,
            "total_duration_minutes": total_duration / 60,
            "average_duration_minutes": avg_duration / 60,
            "outcomes": outcomes
        }

class CallingAgent:
    """Main calling agent system"""
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.contact_manager = ContactManager()
        self.call_manager = CallManager()
        self.campaigns: Dict[str, Campaign] = {}
        self.is_running = False
        self.current_campaign = None
        self.call_queue: List[str] = []  # contact IDs
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        # Load sample data if database is empty
        if len(self.contact_manager.contacts) == 0:
            self._generate_sample_contacts()
    
    def _generate_sample_contacts(self, count: int = 1000):
        """Generate sample contacts for testing"""
        logger.info(f"Generating {count} sample contacts...")
        
        first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily",
            "James", "Jessica", "William", "Ashley", "Richard", "Amanda", "Thomas",
            "Jennifer", "Charles", "Melissa", "Christopher", "Michelle"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
            "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
        ]
        
        companies = [
            "TechCorp", "InnovateLLC", "GlobalSolutions", "DataDynamics", "CloudFirst",
            "DigitalEdge", "SmartSystems", "FutureWorks", "NextGenTech", "ProActive",
            "Synergy Inc", "Velocity Corp", "Pinnacle Group", "Catalyst LLC", "Apex Solutions"
        ]
        
        industries = [
            "Technology", "Healthcare", "Finance", "Manufacturing", "Retail",
            "Education", "Real Estate", "Consulting", "Marketing", "Legal"
        ]
        
        for i in range(count):
            contact = Contact(
                id=str(uuid.uuid4()),
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                phone=f"+1{random.randint(200, 999)}{random.randint(200, 999)}{random.randint(1000, 9999)}",
                email=f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}@{random.choice(companies).lower()}.com",
                company=random.choice(companies),
                title=random.choice(["Manager", "Director", "VP", "CEO", "CTO", "Developer", "Analyst"]),
                industry=random.choice(industries),
                status=random.choice(list(ContactStatus)),
                priority=random.choice(list(Priority)),
                lead_score=random.uniform(0, 100)
            )
            
            self.contact_manager.add_contact(contact)
        
        logger.info(f"Generated {count} sample contacts")
    
    def create_campaign(self, name: str, description: str, script_template: str,
                       target_criteria: Dict[str, Any] = None) -> str:
        """Create a new calling campaign"""
        campaign_id = str(uuid.uuid4())
        
        # Get target contacts based on criteria
        target_contacts = self._get_target_contacts(target_criteria or {})
        
        campaign = Campaign(
            id=campaign_id,
            name=name,
            description=description,
            script_template=script_template,
            target_contacts=[c.id for c in target_contacts],
            start_date=datetime.datetime.utcnow()
        )
        
        self.campaigns[campaign_id] = campaign
        logger.info(f"Created campaign '{name}' with {len(target_contacts)} target contacts")
        return campaign_id
    
    def _get_target_contacts(self, criteria: Dict[str, Any]) -> List[Contact]:
        """Get contacts matching target criteria"""
        contacts = list(self.contact_manager.contacts.values())
        
        # Filter by status
        if "status" in criteria:
            contacts = [c for c in contacts if c.status.value in criteria["status"]]
        
        # Filter by priority
        if "min_priority" in criteria:
            contacts = [c for c in contacts if c.priority.value >= criteria["min_priority"]]
        
        # Filter by lead score
        if "min_lead_score" in criteria:
            contacts = [c for c in contacts if c.lead_score >= criteria["min_lead_score"]]
        
        # Filter by industry
        if "industries" in criteria:
            contacts = [c for c in contacts if c.industry in criteria["industries"]]
        
        # Limit results
        limit = criteria.get("limit", 1000)
        return contacts[:limit]
    
    def start_campaign(self, campaign_id: str) -> bool:
        """Start a calling campaign"""
        if campaign_id not in self.campaigns:
            logger.error(f"Campaign {campaign_id} not found")
            return False
        
        campaign = self.campaigns[campaign_id]
        self.current_campaign = campaign
        self.call_queue = campaign.target_contacts.copy()
        self.is_running = True
        
        logger.info(f"Started campaign '{campaign.name}' with {len(self.call_queue)} contacts")
        
        # Start calling process
        self.executor.submit(self._process_call_queue)
        return True
    
    def stop_campaign(self) -> bool:
        """Stop the current campaign"""
        self.is_running = False
        self.current_campaign = None
        self.call_queue = []
        logger.info("Stopped current campaign")
        return True
    
    def _process_call_queue(self):
        """Process the call queue"""
        while self.is_running and self.call_queue:
            contact_id = self.call_queue.pop(0)
            contact = self.contact_manager.get_contact(contact_id)
            
            if not contact or contact.status == ContactStatus.DO_NOT_CALL:
                continue
            
            # Simulate call processing
            self._make_call(contact)
            
            # Wait between calls
            time.sleep(random.uniform(5, 15))
    
    def _make_call(self, contact: Contact):
        """Make a call to a contact"""
        logger.info(f"Calling {contact.first_name} {contact.last_name} at {contact.phone}")
        
        # Start call record
        call_id = self.call_manager.start_call(
            contact_id=contact.id,
            agent_id=self.agent_id,
            campaign_id=self.current_campaign.id if self.current_campaign else None
        )
        
        # Simulate call progression
        time.sleep(random.uniform(2, 5))  # Dialing time
        
        # Simulate call outcomes
        outcomes = [
            (CallStatus.CONNECTED, CallOutcome.SALE, 0.05),
            (CallStatus.CONNECTED, CallOutcome.APPOINTMENT, 0.10),
            (CallStatus.CONNECTED, CallOutcome.FOLLOW_UP, 0.15),
            (CallStatus.CONNECTED, CallOutcome.NOT_INTERESTED, 0.20),
            (CallStatus.NO_ANSWER, None, 0.25),
            (CallStatus.BUSY, None, 0.10),
            (CallStatus.VOICEMAIL, CallOutcome.VOICEMAIL_LEFT, 0.15)
        ]
        
        # Weighted random selection
        rand = random.random()
        cumulative = 0
        selected_status = CallStatus.FAILED
        selected_outcome = None
        
        for status, outcome, weight in outcomes:
            cumulative += weight
            if rand <= cumulative:
                selected_status = status
                selected_outcome = outcome
                break
        
        # Simulate call duration for connected calls
        if selected_status == CallStatus.CONNECTED:
            call_duration = random.uniform(30, 300)  # 30 seconds to 5 minutes
            time.sleep(min(call_duration / 60, 2))  # Simulate up to 2 seconds for demo
        
        # Update call status
        notes = self._generate_call_notes(contact, selected_outcome)
        self.call_manager.update_call_status(call_id, selected_status, selected_outcome, notes)
        
        # Update contact
        contact.last_contacted = datetime.datetime.utcnow()
        
        # Update lead score based on outcome
        if selected_outcome == CallOutcome.SALE:
            contact.lead_score = min(100, contact.lead_score + 20)
        elif selected_outcome == CallOutcome.APPOINTMENT:
            contact.lead_score = min(100, contact.lead_score + 15)
        elif selected_outcome == CallOutcome.FOLLOW_UP:
            contact.lead_score = min(100, contact.lead_score + 5)
            contact.next_follow_up = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        elif selected_outcome == CallOutcome.NOT_INTERESTED:
            contact.lead_score = max(0, contact.lead_score - 10)
            contact.status = ContactStatus.NOT_INTERESTED
        
        self.contact_manager.update_contact(contact)
    
    def _generate_call_notes(self, contact: Contact, outcome: Optional[CallOutcome]) -> str:
        """Generate call notes based on outcome"""
        notes_templates = {
            CallOutcome.SALE: f"Successfully closed sale with {contact.first_name}. Interested in our premium package.",
            CallOutcome.APPOINTMENT: f"Scheduled follow-up appointment with {contact.first_name} for next week.",
            CallOutcome.FOLLOW_UP: f"{contact.first_name} showed interest but needs time to consider. Follow up in 1 week.",
            CallOutcome.NOT_INTERESTED: f"{contact.first_name} not interested in our services at this time.",
            CallOutcome.CALLBACK: f"{contact.first_name} requested callback at a better time.",
            CallOutcome.VOICEMAIL_LEFT: f"Left voicemail for {contact.first_name} with callback number.",
            CallOutcome.WRONG_NUMBER: f"Phone number appears to be incorrect or disconnected."
        }
        
        return notes_templates.get(outcome, f"Called {contact.first_name} {contact.last_name}")
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get dashboard data for the calling agent"""
        # Get today's statistics
        today = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_stats = self.call_manager.get_call_statistics(
            agent_id=self.agent_id,
            start_date=today
        )
        
        # Get overall statistics
        overall_stats = self.call_manager.get_call_statistics(agent_id=self.agent_id)
        
        # Get contact statistics
        total_contacts = len(self.contact_manager.contacts)
        active_contacts = len(self.contact_manager.get_contacts_by_status(ContactStatus.ACTIVE))
        qualified_contacts = len(self.contact_manager.get_contacts_by_status(ContactStatus.QUALIFIED))
        
        # Get campaign information
        active_campaigns = [c for c in self.campaigns.values() if c.status == "active"]
        
        return {
            "agent_id": self.agent_id,
            "is_running": self.is_running,
            "current_campaign": self.current_campaign.name if self.current_campaign else None,
            "queue_size": len(self.call_queue),
            "today_stats": today_stats,
            "overall_stats": overall_stats,
            "contacts": {
                "total": total_contacts,
                "active": active_contacts,
                "qualified": qualified_contacts
            },
            "campaigns": {
                "total": len(self.campaigns),
                "active": len(active_campaigns)
            }
        }
    
    def export_campaign_results(self, campaign_id: str, output_path: str) -> bool:
        """Export campaign results to CSV"""
        if campaign_id not in self.campaigns:
            logger.error(f"Campaign {campaign_id} not found")
            return False
        
        campaign = self.campaigns[campaign_id]
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'contact_id', 'contact_name', 'phone', 'email', 'company',
                    'call_status', 'call_outcome', 'call_duration', 'notes',
                    'lead_score_before', 'lead_score_after', 'call_date'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for contact_id in campaign.target_contacts:
                    contact = self.contact_manager.get_contact(contact_id)
                    if not contact:
                        continue
                    
                    # Find call records for this contact in this campaign
                    call_records = [
                        c for c in self.call_manager.call_history.values()
                        if c.contact_id == contact_id and c.campaign_id == campaign_id
                    ]
                    
                    if call_records:
                        # Use the most recent call
                        call_record = max(call_records, key=lambda c: c.created_at)
                        
                        writer.writerow({
                            'contact_id': contact.id,
                            'contact_name': f"{contact.first_name} {contact.last_name}",
                            'phone': contact.phone,
                            'email': contact.email or '',
                            'company': contact.company or '',
                            'call_status': call_record.status.value,
                            'call_outcome': call_record.outcome.value if call_record.outcome else '',
                            'call_duration': call_record.duration or 0,
                            'notes': call_record.notes or '',
                            'lead_score_before': contact.lead_score - call_record.lead_score_change,
                            'lead_score_after': contact.lead_score,
                            'call_date': call_record.created_at.isoformat()
                        })
                    else:
                        # Contact not yet called
                        writer.writerow({
                            'contact_id': contact.id,
                            'contact_name': f"{contact.first_name} {contact.last_name}",
                            'phone': contact.phone,
                            'email': contact.email or '',
                            'company': contact.company or '',
                            'call_status': 'pending',
                            'call_outcome': '',
                            'call_duration': 0,
                            'notes': '',
                            'lead_score_before': contact.lead_score,
                            'lead_score_after': contact.lead_score,
                            'call_date': ''
                        })
            
            logger.info(f"Exported campaign results to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting campaign results: {e}")
            return False

def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Quantum Nexus Calling Agent')
    parser.add_argument('--action', choices=['start', 'dashboard', 'campaign', 'import', 'export'],
                       default='dashboard', help='Action to perform')
    parser.add_argument('--campaign-name', help='Campaign name for new campaigns')
    parser.add_argument('--campaign-description', help='Campaign description')
    parser.add_argument('--script', help='Campaign script template')
    parser.add_argument('--import-file', help='CSV file to import contacts from')
    parser.add_argument('--export-file', help='CSV file to export data to')
    parser.add_argument('--campaign-id', help='Campaign ID for operations')
    
    args = parser.parse_args()
    
    # Initialize calling agent
    agent = CallingAgent()
    
    if args.action == 'dashboard':
        # Show dashboard
        dashboard = agent.get_dashboard_data()
        print("\n" + "="*60)
        print("QUANTUM NEXUS CALLING AGENT DASHBOARD")
        print("="*60)
        print(f"Agent ID: {dashboard['agent_id']}")
        print(f"Status: {'RUNNING' if dashboard['is_running'] else 'STOPPED'}")
        print(f"Current Campaign: {dashboard['current_campaign'] or 'None'}")
        print(f"Queue Size: {dashboard['queue_size']}")
        print("\nContacts:")
        print(f"  Total: {dashboard['contacts']['total']:,}")
        print(f"  Active: {dashboard['contacts']['active']:,}")
        print(f"  Qualified: {dashboard['contacts']['qualified']:,}")
        print("\nCampaigns:")
        print(f"  Total: {dashboard['campaigns']['total']}")
        print(f"  Active: {dashboard['campaigns']['active']}")
        print("\nToday's Performance:")
        today = dashboard['today_stats']
        print(f"  Calls Made: {today['total_calls']}")
        print(f"  Connection Rate: {today.get('connection_rate', 0):.1f}%")
        print(f"  Total Duration: {today.get('total_duration_minutes', 0):.1f} minutes")
        print("\nOverall Performance:")
        overall = dashboard['overall_stats']
        print(f"  Total Calls: {overall['total_calls']:,}")
        print(f"  Connection Rate: {overall.get('connection_rate', 0):.1f}%")
        print(f"  Completion Rate: {overall.get('completion_rate', 0):.1f}%")
        print("="*60)
    
    elif args.action == 'campaign':
        if not all([args.campaign_name, args.campaign_description, args.script]):
            print("Error: Campaign name, description, and script are required")
            return 1
        
        # Create and start campaign
        campaign_id = agent.create_campaign(
            name=args.campaign_name,
            description=args.campaign_description,
            script_template=args.script,
            target_criteria={"status": ["active"], "limit": 100}
        )
        
        print(f"Created campaign: {campaign_id}")
        
        # Start campaign
        if agent.start_campaign(campaign_id):
            print(f"Started campaign '{args.campaign_name}'")
            
            # Run for a short demo period
            time.sleep(30)
            agent.stop_campaign()
            print("Campaign stopped")
        else:
            print("Failed to start campaign")
    
    elif args.action == 'import':
        if not args.import_file:
            print("Error: Import file path required")
            return 1
        
        count = agent.contact_manager.import_contacts_from_csv(args.import_file)
        print(f"Imported {count} contacts from {args.import_file}")
    
    elif args.action == 'export':
        if not args.export_file:
            print("Error: Export file path required")
            return 1
        
        if args.campaign_id:
            # Export campaign results
            if agent.export_campaign_results(args.campaign_id, args.export_file):
                print(f"Exported campaign results to {args.export_file}")
            else:
                print("Failed to export campaign results")
        else:
            # Export all contacts
            if agent.contact_manager.export_contacts_to_csv(args.export_file):
                print(f"Exported contacts to {args.export_file}")
            else:
                print("Failed to export contacts")
    
    return 0

if __name__ == '__main__':
    exit(main())