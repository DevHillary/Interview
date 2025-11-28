"""
Script to create sample data for testing the CRM system with Kenyan-based data.
Run this inside the Docker container:
    docker-compose exec backend python create_sample_data.py
"""

import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from crm.models import Lead, Contact, Note, Reminder, Correspondence

User = get_user_model()


def create_sample_data():
    print("Creating Kenyan-based sample data...")
    
    # Create users if they don't exist
    manager, created = User.objects.get_or_create(
        username='manager',
        defaults={
            'email': 'manager@crm.co.ke',
            'first_name': 'Amina',
            'last_name': 'Odhiambo',
            'role': 'manager'
        }
    )
    if created:
        manager.set_password('password123')
        manager.save()
        print("✓ Created manager user (username: manager, password: password123)")
    else:
        print("✓ Manager user already exists")
    
    agent, created = User.objects.get_or_create(
        username='agent',
        defaults={
            'email': 'agent@crm.co.ke',
            'first_name': 'James',
            'last_name': 'Kamau',
            'role': 'agent'
        }
    )
    if created:
        agent.set_password('password123')
        agent.save()
        print("✓ Created agent user (username: agent, password: password123)")
    else:
        print("✓ Agent user already exists")
    
    # Create sample leads with Kenyan businesses
    leads_data = [
        {
            'name': 'Peter Mwangi',
            'company': 'Safaricom Business Solutions',
            'email': 'p.mwangi@safaricom.co.ke',
            'phone': '+254-722-123-456',
            'status': 'new',
            'priority': 'high',
            'source': 'Website',
            'estimated_value': 2500000.00,
            'description': 'Interested in enterprise CRM solution for telecommunications',
            'owner': manager
        },
        {
            'name': 'Grace Njeri',
            'company': 'Equity Bank Kenya',
            'email': 'g.njeri@equitybank.co.ke',
            'phone': '+254-733-234-567',
            'status': 'contacted',
            'priority': 'high',
            'source': 'Referral',
            'estimated_value': 3500000.00,
            'description': 'Looking for customer relationship management for banking sector',
            'owner': manager
        },
        {
            'name': 'David Kipchoge',
            'company': 'Kenya Airways',
            'email': 'd.kipchoge@kenya-airways.com',
            'phone': '+254-711-345-678',
            'status': 'qualified',
            'priority': 'high',
            'source': 'Trade Show',
            'estimated_value': 4200000.00,
            'description': 'Ready to purchase, needs demo for aviation management',
            'owner': manager
        },
        {
            'name': 'Lucy Wanjiku',
            'company': 'Nairobi Hospital',
            'email': 'l.wanjiku@nairobihospital.org',
            'phone': '+254-722-456-789',
            'status': 'contacted',
            'priority': 'medium',
            'source': 'LinkedIn',
            'estimated_value': 1800000.00,
            'description': 'Healthcare facility interested in patient management system',
            'owner': agent
        },
        {
            'name': 'John Otieno',
            'company': 'Twiga Foods',
            'email': 'j.otieno@twigafoods.com',
            'phone': '+254-733-567-890',
            'status': 'new',
            'priority': 'medium',
            'source': 'Cold Call',
            'estimated_value': 1200000.00,
            'description': 'Food distribution company needs supply chain CRM',
            'owner': agent
        },
        {
            'name': 'Sarah Achieng',
            'company': 'NCBA Bank',
            'email': 's.achieng@ncbabank.com',
            'phone': '+254-711-678-901',
            'status': 'qualified',
            'priority': 'high',
            'source': 'Website',
            'estimated_value': 3000000.00,
            'description': 'Financial services CRM for retail banking division',
            'owner': manager
        },
        {
            'name': 'Michael Omondi',
            'company': 'Bidco Africa',
            'email': 'm.omondi@bidco-africa.com',
            'phone': '+254-722-789-012',
            'status': 'contacted',
            'priority': 'medium',
            'source': 'Email Campaign',
            'estimated_value': 2100000.00,
            'description': 'Manufacturing company seeking distributor management system',
            'owner': agent
        },
        {
            'name': 'Faith Mutua',
            'company': 'Standard Chartered Kenya',
            'email': 'f.mutua@sc.com',
            'phone': '+254-733-890-123',
            'status': 'new',
            'priority': 'high',
            'source': 'Referral',
            'estimated_value': 3800000.00,
            'description': 'Corporate banking division needs comprehensive CRM',
            'owner': manager
        },
        {
            'name': 'Daniel Kariuki',
            'company': 'Jambojet Airlines',
            'email': 'd.kariuki@jambojet.com',
            'phone': '+254-711-901-234',
            'status': 'lost',
            'priority': 'low',
            'source': 'Trade Show',
            'estimated_value': 800000.00,
            'description': 'Budget airline - decided to postpone CRM implementation',
            'owner': agent
        },
        {
            'name': 'Rose Chebet',
            'company': 'M-KOPA Solar',
            'email': 'r.chebet@m-kopa.com',
            'phone': '+254-722-012-345',
            'status': 'converted',
            'priority': 'medium',
            'source': 'Website',
            'estimated_value': 1500000.00,
            'description': 'Renewable energy company - successfully onboarded',
            'owner': manager
        },
    ]
    
    kenyan_notes = [
        "Initial contact made during Nairobi Tech Week. Very interested in cloud-based solutions.",
        "Follow-up call scheduled. Discussed M-Pesa integration requirements.",
        "Sent proposal including pricing in KES. Awaiting feedback from procurement team.",
        "Demo completed successfully. Impressed with mobile-first approach.",
        "Contract negotiations ongoing. Legal team reviewing terms.",
        "Discussed GDPR and Kenya Data Protection Act compliance.",
        "Meeting with IT department scheduled at their Westlands office.",
        "Requested customization for Swahili language support.",
    ]
    
    correspondence_subjects = [
        "Initial CRM Solution Inquiry",
        "Follow-up: Product Demo Request",
        "Proposal for Enterprise CRM Implementation",
        "Meeting Minutes: Requirements Discussion",
        "Quote Request - CRM System",
        "Technical Specifications Review",
    ]
    
    for lead_data in leads_data:
        lead, created = Lead.objects.get_or_create(
            email=lead_data['email'],
            defaults=lead_data
        )
        if created:
            print(f"✓ Created lead: {lead.name} - {lead.company}")
            
            # Create primary contact
            contact = Contact.objects.create(
                lead=lead,
                name=lead.name,
                email=lead.email,
                phone=lead.phone,
                position='Chief Technology Officer' if 'tech' in lead.company.lower() else 'Business Development Manager',
                is_primary=True,
                notes=f'Primary decision maker at {lead.company}'
            )
            print(f"  ✓ Created contact: {contact.name}")
            
            # Create 1-2 additional contacts for some leads
            if random.choice([True, False]):
                additional_names = ['Joseph Mutinda', 'Mary Wambui', 'Patrick Njoroge', 'Anne Akinyi']
                Contact.objects.create(
                    lead=lead,
                    name=random.choice(additional_names),
                    email=f"{random.choice(additional_names).lower().replace(' ', '.')}@{lead.email.split('@')[1]}",
                    phone=f"+254-{random.randint(700,799)}-{random.randint(100,999)}-{random.randint(100,999)}",
                    position='IT Manager',
                    is_primary=False,
                    notes='Technical contact for implementation'
                )
            
            # Create 2-3 notes per lead
            for i in range(random.randint(2, 3)):
                Note.objects.create(
                    lead=lead,
                    author=lead.owner,
                    content=random.choice(kenyan_notes)
                )
            print(f"  ✓ Created notes for lead")
            
            # Create reminders based on status
            if lead.status in ['new', 'contacted', 'qualified']:
                days_ahead = {'new': 2, 'contacted': 5, 'qualified': 1}
                reminder_date = datetime.now() + timedelta(days=days_ahead.get(lead.status, 3))
                Reminder.objects.create(
                    lead=lead,
                    user=lead.owner,
                    title=f"Follow up with {lead.name} from {lead.company}",
                    description=f"Schedule {'demo' if lead.status == 'new' else 'follow-up'} call to discuss CRM implementation",
                    reminder_date=reminder_date,
                    status='pending'
                )
                print(f"  ✓ Created reminder for lead")
            
            # Create 1-3 correspondence logs
            for i in range(random.randint(1, 3)):
                corr_type = random.choice(['email', 'phone', 'meeting'])
                Correspondence.objects.create(
                    contact=contact,
                    type=corr_type,
                    subject=random.choice(correspondence_subjects),
                    description=f"{'Discussed' if corr_type == 'phone' else 'Sent information about'} CRM features and pricing. {'Client expressed interest in' if i == 0 else 'Followed up on'} implementation timeline.",
                    date=datetime.now() - timedelta(days=random.randint(1, 14)),
                    logged_by=lead.owner
                )
            print(f"  ✓ Created correspondence logs")
        else:
            print(f"✓ Lead already exists: {lead.name} - {lead.company}")
    
    print("\n" + "="*50)
    print("Sample data creation complete!")
    print("="*50)
    print("\nYou can now login with:")
    print("  Manager: username=manager, password=password123")
    print("  Agent:   username=agent, password=password123")
    print("\nAccess the application at:")
    print("  Frontend: http://localhost:8080")
    print("  Backend:  http://localhost:8000")
    print("  API Docs: http://localhost:8000/swagger/")
    print("="*50)


if __name__ == '__main__':
    create_sample_data()


