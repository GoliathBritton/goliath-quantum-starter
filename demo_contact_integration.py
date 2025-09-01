#!/usr/bin/env python3
"""
Quantum Digital Agent Contact Integration & Building Demo
=======================================================

This demo shows how to:
1. Integrate real business contacts into the system
2. Build and configure the Quantum Digital Agent
3. Set up the troubleshooting system
4. Handle client questions about the technology

Perfect for client demonstrations and technical explanations.
"""

import json
import csv
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ContactSource(Enum):
    """Contact source enumeration"""

    CRM_EXPORT = "crm_export"
    LINKEDIN_SCRAPING = "linkedin_scraping"
    TRADE_SHOWS = "trade_shows"
    REFERRALS = "referrals"
    WEBSITE_LEADS = "website_leads"
    MANUAL_ENTRY = "manual_entry"


class ContactPriority(Enum):
    """Contact priority levels"""

    HOT = "hot"  # Immediate follow-up needed
    WARM = "warm"  # Follow-up within 1 week
    COLD = "cold"  # Follow-up within 1 month
    NURTURE = "nurture"  # Long-term nurturing


@dataclass
class BusinessContact:
    """Enhanced business contact structure"""

    contact_id: str
    company_name: str
    contact_name: str
    title: str
    phone: str
    email: str
    industry: str
    company_size: str
    annual_revenue: str
    source: ContactSource
    priority: ContactPriority
    last_contact_date: Optional[datetime]
    notes: str
    priority_score: float
    timezone: str
    best_contact_time: str
    linkedin_url: Optional[str]
    website: Optional[str]
    pain_points: List[str]
    interests: List[str]
    budget_range: str
    decision_maker: bool
    technical_contact: bool


class ContactIntegrationDemo:
    """Demo class for contact integration and agent building"""

    def __init__(self):
        self.contacts = []
        self.agent_config = {}
        self.troubleshooting_agents = []

    def import_contacts_from_csv(self, file_path: str) -> List[BusinessContact]:
        """Import contacts from CSV file"""
        print(f"📥 Importing contacts from: {file_path}")
        print("-" * 50)

        contacts = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row_num, row in enumerate(reader, 1):
                    try:
                        contact = BusinessContact(
                            contact_id=f"import_{row_num:06d}",
                            company_name=row.get("company_name", f"Company {row_num}"),
                            contact_name=row.get("contact_name", f"Contact {row_num}"),
                            title=row.get("title", "Unknown"),
                            phone=row.get("phone", ""),
                            email=row.get("email", ""),
                            industry=row.get("industry", "Unknown"),
                            company_size=row.get("company_size", "Unknown"),
                            annual_revenue=row.get("annual_revenue", "Unknown"),
                            source=ContactSource.MANUAL_ENTRY,
                            priority=ContactPriority.WARM,
                            last_contact_date=None,
                            notes=row.get("notes", ""),
                            priority_score=0.5,
                            timezone=row.get("timezone", "EST"),
                            best_contact_time=row.get("best_contact_time", "9-11 AM"),
                            linkedin_url=row.get("linkedin_url"),
                            website=row.get("website"),
                            pain_points=(
                                row.get("pain_points", "").split(";")
                                if row.get("pain_points")
                                else []
                            ),
                            interests=(
                                row.get("interests", "").split(";")
                                if row.get("interests")
                                else []
                            ),
                            budget_range=row.get("budget_range", "Unknown"),
                            decision_maker=row.get("decision_maker", "false").lower()
                            == "true",
                            technical_contact=row.get(
                                "technical_contact", "false"
                            ).lower()
                            == "true",
                        )
                        contacts.append(contact)
                        print(
                            f"✅ Imported: {contact.company_name} - {contact.contact_name}"
                        )

                    except Exception as e:
                        print(f"❌ Error importing row {row_num}: {e}")

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            # Create sample contacts for demo
            contacts = self.create_sample_contacts(100)

        print(f"\n📊 Total contacts imported: {len(contacts)}")
        self.contacts = contacts
        return contacts

    def create_sample_contacts(self, count: int) -> List[BusinessContact]:
        """Create sample contacts for demo purposes"""
        print(f"🔧 Creating {count} sample contacts for demo")

        industries = ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail"]
        company_sizes = ["1-10", "11-50", "51-200", "201-1000", "1000+"]
        revenue_ranges = ["<$1M", "$1M-$10M", "$10M-$50M", "$50M-$100M", "$100M+"]
        timezones = ["EST", "CST", "MST", "PST"]

        contacts = []
        for i in range(count):
            contact = BusinessContact(
                contact_id=f"sample_{i:06d}",
                company_name=f"Sample Company {i+1}",
                contact_name=f"Sample Contact {i+1}",
                title="CEO",
                phone=f"+1-555-{100+i:03d}-{1000+i:04d}",
                email=f"contact{i+1}@samplecompany{i+1}.com",
                industry=industries[i % len(industries)],
                company_size=company_sizes[i % len(company_sizes)],
                annual_revenue=revenue_ranges[i % len(revenue_ranges)],
                source=ContactSource.MANUAL_ENTRY,
                priority=ContactPriority.WARM,
                last_contact_date=None,
                notes="Sample contact for demonstration",
                priority_score=0.5 + (i * 0.01),
                timezone=timezones[i % len(timezones)],
                best_contact_time="9-11 AM",
                linkedin_url=f"https://linkedin.com/in/samplecontact{i+1}",
                website=f"https://samplecompany{i+1}.com",
                pain_points=["Efficiency", "Cost reduction", "Growth"],
                interests=["AI", "Automation", "Innovation"],
                budget_range="$10K-$50K",
                decision_maker=True,
                technical_contact=False,
            )
            contacts.append(contact)

        return contacts

    def build_quantum_agent(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build and configure the Quantum Digital Agent"""
        print("\n🤖 BUILDING QUANTUM DIGITAL AGENT")
        print("=" * 60)

        # Agent configuration
        self.agent_config = {
            "agent_id": agent_config.get("agent_id", "quantum_agent_001"),
            "name": agent_config.get("name", "Quantum Business Development Agent"),
            "specialization": agent_config.get(
                "specialization", "General business development"
            ),
            "quantum_enhancement": agent_config.get(
                "quantum_enhancement", "Advanced lead qualification"
            ),
            "gpu_acceleration": agent_config.get("gpu_acceleration", "NVIDIA RTX 4090"),
            "contact_list_size": len(self.contacts),
            "campaign_strategy": agent_config.get(
                "campaign_strategy", "Multi-touch nurturing"
            ),
            "call_scripts": self._generate_call_scripts(),
            "follow_up_sequences": self._generate_follow_up_sequences(),
            "performance_metrics": {
                "target_conversion_rate": 0.15,
                "target_calls_per_day": 100,
                "target_qualified_leads_per_month": 50,
            },
        }

        print("✅ Agent Configuration Complete:")
        for key, value in self.agent_config.items():
            if key != "call_scripts" and key != "follow_up_sequences":
                print(f"  {key}: {value}")

        print("\n📝 Call Scripts Generated:")
        for script_type in self.agent_config["call_scripts"].keys():
            print(f"  - {script_type.replace('_', ' ').title()}")

        print("\n🔄 Follow-up Sequences Generated:")
        for sequence_type in self.agent_config["follow_up_sequences"].keys():
            print(f"  - {sequence_type.replace('_', ' ').title()}")

        return self.agent_config

    def _generate_call_scripts(self) -> Dict[str, str]:
        """Generate personalized call scripts based on contact data"""
        return {
            "opening": """Hi {contact_name}, this is {agent_name} calling from {company_name}. 
            I hope I'm catching you at a good time. I noticed {company_name} is in the {industry} space, 
            and I wanted to reach out because we've been helping companies like yours with {value_proposition}. 
            Would you be open to a brief conversation about how we might be able to help {company_name}?""",
            "value_proposition": """Based on what I know about {industry} companies, 
            we've helped businesses like yours increase their {metric} by an average of {percentage}% 
            while reducing {cost} by {cost_reduction}%. Our quantum-enhanced solutions provide insights 
            that traditional approaches simply can't match.""",
            "qualification": """To make sure this conversation is valuable for both of us, 
            could you help me understand: What are your biggest challenges right now in terms of {challenge_area}? 
            And what would success look like for {company_name} in the next 6-12 months?""",
            "objection_handling": """I completely understand your concern about {objection}. 
            Many of our clients in the {industry} space had similar thoughts initially. 
            What I've found is that {counter_argument}. Would it be helpful if I shared a specific 
            example of how we've addressed this for other {industry} companies?""",
            "closing": """Based on what you've shared about {company_name}'s challenges, 
            I think there could be a great opportunity for us to help. Would you be open to a more 
            detailed conversation next week? I could prepare some specific insights based on what 
            we've discussed today.""",
        }

    def _generate_follow_up_sequences(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate follow-up sequences based on contact priority and responses"""
        return {
            "hot_leads": [
                {
                    "day": 1,
                    "method": "email",
                    "content": "Thank you call + detailed proposal",
                },
                {
                    "day": 3,
                    "method": "call",
                    "content": "Follow-up call to address questions",
                },
                {
                    "day": 7,
                    "method": "email",
                    "content": "Case study + scheduling request",
                },
            ],
            "warm_leads": [
                {
                    "day": 3,
                    "method": "email",
                    "content": "Thank you + value-add content",
                },
                {
                    "day": 7,
                    "method": "email",
                    "content": "Industry insights + gentle follow-up",
                },
                {"day": 14, "method": "call", "content": "Check-in call"},
            ],
            "cold_leads": [
                {"day": 7, "method": "email", "content": "Educational content"},
                {
                    "day": 21,
                    "method": "email",
                    "content": "Industry trends + soft offer",
                },
                {"day": 45, "method": "email", "content": "Re-engagement campaign"},
            ],
        }

    def export_contacts_to_csv(self, file_path: str):
        """Export contacts to CSV for external use"""
        print(f"\n📤 Exporting contacts to: {file_path}")

        if not self.contacts:
            print("❌ No contacts to export")
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                # Get all fields from the first contact
                fieldnames = list(asdict(self.contacts[0]).keys())

                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for contact in self.contacts:
                    # Convert dataclass to dict and handle datetime
                    contact_dict = asdict(contact)
                    if contact_dict["last_contact_date"]:
                        contact_dict["last_contact_date"] = contact_dict[
                            "last_contact_date"
                        ].isoformat()
                    if contact_dict["pain_points"]:
                        contact_dict["pain_points"] = ";".join(
                            contact_dict["pain_points"]
                        )
                    if contact_dict["interests"]:
                        contact_dict["interests"] = ";".join(contact_dict["interests"])

                    writer.writerow(contact_dict)

                print(f"✅ Successfully exported {len(self.contacts)} contacts")

        except Exception as e:
            print(f"❌ Error exporting contacts: {e}")

    def display_contact_summary(self):
        """Display summary of imported contacts"""
        if not self.contacts:
            print("❌ No contacts available")
            return

        print("\n📊 CONTACT SUMMARY")
        print("=" * 50)

        # Industry breakdown
        industries = {}
        for contact in self.contacts:
            industry = contact.industry
            industries[industry] = industries.get(industry, 0) + 1

        print("🏭 Industry Breakdown:")
        for industry, count in sorted(
            industries.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {industry}: {count} contacts")

        # Company size breakdown
        company_sizes = {}
        for contact in self.contacts:
            size = contact.company_size
            company_sizes[size] = company_sizes.get(size, 0) + 1

        print("\n🏢 Company Size Breakdown:")
        for size, count in sorted(
            company_sizes.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {size}: {count} contacts")

        # Priority breakdown
        priorities = {}
        for contact in self.contacts:
            priority = contact.priority.value
            priorities[priority] = priorities.get(priority, 0) + 1

        print("\n🎯 Priority Breakdown:")
        for priority, count in sorted(
            priorities.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {priority.title()}: {count} contacts")

        # Decision makers
        decision_makers = sum(1 for contact in self.contacts if contact.decision_maker)
        technical_contacts = sum(
            1 for contact in self.contacts if contact.technical_contact
        )

        print(f"\n👑 Decision Makers: {decision_makers}")
        print(f"🔧 Technical Contacts: {technical_contacts}")
        print(f"📧 Total Contacts: {len(self.contacts)}")


def main():
    """Main demo function"""
    demo = ContactIntegrationDemo()

    print("🚀 QUANTUM DIGITAL AGENT CONTACT INTEGRATION DEMO")
    print("=" * 70)
    print("This demo shows how to integrate real contacts and build the agent")
    print()

    # Step 1: Import contacts
    print("📥 STEP 1: CONTACT IMPORT")
    print("-" * 40)
    contacts = demo.import_contacts_from_csv(
        "contacts.csv"
    )  # Will create samples if file doesn't exist

    # Step 2: Display contact summary
    demo.display_contact_summary()

    # Step 3: Build quantum agent
    print("\n🤖 STEP 2: AGENT BUILDING")
    print("-" * 40)
    agent_config = {
        "agent_id": "quantum_agent_001",
        "name": "Quantum Business Development Agent Alpha",
        "specialization": "Multi-industry business development",
        "quantum_enhancement": "Advanced lead qualification and scoring",
        "gpu_acceleration": "NVIDIA RTX 4090",
        "campaign_strategy": "Intelligent multi-touch nurturing",
    }

    agent = demo.build_quantum_agent(agent_config)

    # Step 4: Export contacts (optional)
    print("\n📤 STEP 3: CONTACT EXPORT (Optional)")
    print("-" * 40)
    demo.export_contacts_to_csv("exported_contacts.csv")

    print("\n🎉 CONTACT INTEGRATION DEMO COMPLETE!")
    print("=" * 70)
    print("Next Steps:")
    print("1. Replace sample contacts with your real contact list")
    print("2. Customize call scripts for your industry and value proposition")
    print("3. Configure follow-up sequences based on your sales process")
    print("4. Set up the troubleshooting system")
    print("5. Launch your first campaign!")


if __name__ == "__main__":
    main()
