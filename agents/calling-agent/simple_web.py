#!/usr/bin/env python3
"""
Quantum Nexus Platform - Simple Calling Agent Web Interface

A basic Flask web interface for the calling agent system.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
from datetime import datetime, timedelta
from calling_agent import CallingAgent, Contact, Campaign, ContactStatus, Priority, CallStatus, CallOutcome
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quantum-nexus-calling-agent-2024'

# Global calling agent instance
calling_agent = CallingAgent()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        dashboard_data = calling_agent.get_dashboard_data()
        return render_template('dashboard.html', data=dashboard_data)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html', data={})

@app.route('/contacts')
def contacts():
    """Contacts management page"""
    try:
        contacts_list = calling_agent.contact_manager.get_all_contacts()
        return render_template('contacts.html', contacts=contacts_list)
    except Exception as e:
        flash(f'Error loading contacts: {str(e)}', 'error')
        return render_template('contacts.html', contacts=[])

@app.route('/campaigns')
def campaigns():
    """Campaigns management page"""
    try:
        campaigns_list = calling_agent.call_manager.get_all_campaigns()
        return render_template('campaigns.html', campaigns=campaigns_list)
    except Exception as e:
        flash(f'Error loading campaigns: {str(e)}', 'error')
        return render_template('campaigns.html', campaigns=[])

@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    """API endpoint to get contacts"""
    try:
        contacts = calling_agent.contact_manager.get_all_contacts()
        return jsonify({
            'success': True,
            'contacts': [contact.__dict__ for contact in contacts]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/contacts', methods=['POST'])
def api_add_contact():
    """API endpoint to add a new contact"""
    try:
        data = request.get_json()
        contact = Contact(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            company=data.get('company', ''),
            notes=data.get('notes', '')
        )
        calling_agent.contact_manager.add_contact(contact)
        return jsonify({
            'success': True,
            'message': 'Contact added successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/campaigns', methods=['GET'])
def api_get_campaigns():
    """API endpoint to get campaigns"""
    try:
        campaigns = calling_agent.call_manager.get_all_campaigns()
        return jsonify({
            'success': True,
            'campaigns': [campaign.__dict__ for campaign in campaigns]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/campaigns', methods=['POST'])
def api_create_campaign():
    """API endpoint to create a new campaign"""
    try:
        data = request.get_json()
        campaign = Campaign(
            name=data['name'],
            description=data.get('description', ''),
            contact_ids=data.get('contact_ids', []),
            script=data.get('script', ''),
            priority=Priority(data.get('priority', 'medium'))
        )
        calling_agent.call_manager.create_campaign(campaign)
        return jsonify({
            'success': True,
            'message': 'Campaign created successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint to get dashboard data"""
    try:
        data = calling_agent.get_dashboard_data()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )