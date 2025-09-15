#!/usr/bin/env python3
"""
Quantum Nexus Platform - Calling Agent Web Interface

A Flask-based web interface for the calling agent system providing:
- Real-time dashboard with call statistics
- Contact management interface
- Campaign creation and management
- Live call monitoring
- Performance analytics and reporting
- Contact import/export functionality
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime, timedelta
import threading
import time
from calling_agent import CallingAgent, Contact, Campaign, ContactStatus, Priority, CallStatus, CallOutcome
import uuid
import tempfile
import csv
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quantum-nexus-calling-agent-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global calling agent instance
calling_agent = CallingAgent()

# Background thread for real-time updates
update_thread = None
update_thread_stop = threading.Event()

def background_updates():
    """Background thread to send real-time updates to connected clients"""
    while not update_thread_stop.is_set():
        try:
            # Get current dashboard data
            dashboard_data = calling_agent.get_dashboard_data()
            
            # Emit to all connected clients
            socketio.emit('dashboard_update', dashboard_data)
            
            # Wait 5 seconds before next update
            time.sleep(5)
            
        except Exception as e:
            print(f"Error in background updates: {e}")
            time.sleep(10)

@app.route('/')
def index():
    """Main dashboard page"""
    dashboard_data = calling_agent.get_dashboard_data()
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data"""
    return jsonify(calling_agent.get_dashboard_data())

@app.route('/contacts')
def contacts():
    """Contacts management page"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    # Get contacts
    all_contacts = list(calling_agent.contact_manager.contacts.values())
    
    # Apply search filter
    if search:
        filtered_contacts = calling_agent.contact_manager.search_contacts(search, limit=1000)
    else:
        filtered_contacts = all_contacts
    
    # Apply status filter
    if status_filter:
        filtered_contacts = [c for c in filtered_contacts if c.status.value == status_filter]
    
    # Pagination
    total = len(filtered_contacts)
    start = (page - 1) * per_page
    end = start + per_page
    contacts_page = filtered_contacts[start:end]
    
    # Calculate pagination info
    has_prev = page > 1
    has_next = end < total
    prev_num = page - 1 if has_prev else None
    next_num = page + 1 if has_next else None
    
    return render_template('contacts.html', 
                         contacts=contacts_page,
                         pagination={
                             'page': page,
                             'per_page': per_page,
                             'total': total,
                             'has_prev': has_prev,
                             'has_next': has_next,
                             'prev_num': prev_num,
                             'next_num': next_num
                         },
                         search=search,
                         status_filter=status_filter,
                         contact_statuses=ContactStatus,
                         priorities=Priority)

@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    """Add new contact"""
    if request.method == 'POST':
        try:
            contact = Contact(
                id=str(uuid.uuid4()),
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                phone=request.form['phone'],
                email=request.form.get('email') or None,
                company=request.form.get('company') or None,
                title=request.form.get('title') or None,
                industry=request.form.get('industry') or None,
                status=ContactStatus(request.form.get('status', 'active')),
                priority=Priority(int(request.form.get('priority', 2))),
                lead_score=float(request.form.get('lead_score', 0.0)),
                notes=request.form.get('notes') or None
            )
            
            if calling_agent.contact_manager.add_contact(contact):
                flash('Contact added successfully!', 'success')
                return redirect(url_for('contacts'))
            else:
                flash('Error adding contact!', 'error')
                
        except Exception as e:
            flash(f'Error adding contact: {str(e)}', 'error')
    
    return render_template('add_contact.html', 
                         contact_statuses=ContactStatus,
                         priorities=Priority)

@app.route('/contacts/<contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
    """Edit existing contact"""
    contact = calling_agent.contact_manager.get_contact(contact_id)
    if not contact:
        flash('Contact not found!', 'error')
        return redirect(url_for('contacts'))
    
    if request.method == 'POST':
        try:
            contact.first_name = request.form['first_name']
            contact.last_name = request.form['last_name']
            contact.phone = request.form['phone']
            contact.email = request.form.get('email') or None
            contact.company = request.form.get('company') or None
            contact.title = request.form.get('title') or None
            contact.industry = request.form.get('industry') or None
            contact.status = ContactStatus(request.form.get('status', 'active'))
            contact.priority = Priority(int(request.form.get('priority', 2)))
            contact.lead_score = float(request.form.get('lead_score', 0.0))
            contact.notes = request.form.get('notes') or None
            
            if calling_agent.contact_manager.update_contact(contact):
                flash('Contact updated successfully!', 'success')
                return redirect(url_for('contacts'))
            else:
                flash('Error updating contact!', 'error')
                
        except Exception as e:
            flash(f'Error updating contact: {str(e)}', 'error')
    
    return render_template('edit_contact.html', 
                         contact=contact,
                         contact_statuses=ContactStatus,
                         priorities=Priority)

@app.route('/campaigns')
def campaigns():
    """Campaigns management page"""
    campaigns_list = list(calling_agent.campaigns.values())
    campaigns_list.sort(key=lambda c: c.created_at, reverse=True)
    
    return render_template('campaigns.html', campaigns=campaigns_list)

@app.route('/campaigns/add', methods=['GET', 'POST'])
def add_campaign():
    """Add new campaign"""
    if request.method == 'POST':
        try:
            # Get target criteria
            target_criteria = {
                'limit': int(request.form.get('target_limit', 100))
            }
            
            if request.form.get('target_status'):
                target_criteria['status'] = [request.form['target_status']]
            
            if request.form.get('min_priority'):
                target_criteria['min_priority'] = int(request.form['min_priority'])
            
            if request.form.get('min_lead_score'):
                target_criteria['min_lead_score'] = float(request.form['min_lead_score'])
            
            if request.form.get('target_industries'):
                industries = [i.strip() for i in request.form['target_industries'].split(',')]
                target_criteria['industries'] = industries
            
            campaign_id = calling_agent.create_campaign(
                name=request.form['name'],
                description=request.form['description'],
                script_template=request.form['script_template'],
                target_criteria=target_criteria
            )
            
            flash(f'Campaign created successfully! ID: {campaign_id}', 'success')
            return redirect(url_for('campaigns'))
            
        except Exception as e:
            flash(f'Error creating campaign: {str(e)}', 'error')
    
    return render_template('add_campaign.html', 
                         contact_statuses=ContactStatus,
                         priorities=Priority)

@app.route('/campaigns/<campaign_id>/start', methods=['POST'])
def start_campaign(campaign_id):
    """Start a campaign"""
    if calling_agent.start_campaign(campaign_id):
        flash('Campaign started successfully!', 'success')
    else:
        flash('Error starting campaign!', 'error')
    
    return redirect(url_for('campaigns'))

@app.route('/campaigns/<campaign_id>/stop', methods=['POST'])
def stop_campaign(campaign_id):
    """Stop a campaign"""
    if calling_agent.stop_campaign():
        flash('Campaign stopped successfully!', 'success')
    else:
        flash('Error stopping campaign!', 'error')
    
    return redirect(url_for('campaigns'))

@app.route('/campaigns/<campaign_id>/export')
def export_campaign(campaign_id):
    """Export campaign results"""
    try:
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        temp_file.close()
        
        if calling_agent.export_campaign_results(campaign_id, temp_file.name):
            return send_file(temp_file.name, 
                           as_attachment=True, 
                           download_name=f'campaign_{campaign_id}_results.csv',
                           mimetype='text/csv')
        else:
            flash('Error exporting campaign results!', 'error')
            return redirect(url_for('campaigns'))
            
    except Exception as e:
        flash(f'Error exporting campaign: {str(e)}', 'error')
        return redirect(url_for('campaigns'))

@app.route('/calls')
def calls():
    """Call history page"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    # Get call history
    all_calls = list(calling_agent.call_manager.call_history.values())
    all_calls.sort(key=lambda c: c.created_at, reverse=True)
    
    # Pagination
    total = len(all_calls)
    start = (page - 1) * per_page
    end = start + per_page
    calls_page = all_calls[start:end]
    
    # Get contact names for calls
    for call in calls_page:
        contact = calling_agent.contact_manager.get_contact(call.contact_id)
        call.contact_name = f"{contact.first_name} {contact.last_name}" if contact else "Unknown"
    
    # Calculate pagination info
    has_prev = page > 1
    has_next = end < total
    prev_num = page - 1 if has_prev else None
    next_num = page + 1 if has_next else None
    
    return render_template('calls.html', 
                         calls=calls_page,
                         pagination={
                             'page': page,
                             'per_page': per_page,
                             'total': total,
                             'has_prev': has_prev,
                             'has_next': has_next,
                             'prev_num': prev_num,
                             'next_num': next_num
                         })

@app.route('/analytics')
def analytics():
    """Analytics and reporting page"""
    # Get date range from query params
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)  # Default to last 30 days
    
    if request.args.get('start_date'):
        start_date = datetime.fromisoformat(request.args['start_date'])
    if request.args.get('end_date'):
        end_date = datetime.fromisoformat(request.args['end_date'])
    
    # Get statistics
    stats = calling_agent.call_manager.get_call_statistics(
        agent_id=calling_agent.agent_id,
        start_date=start_date,
        end_date=end_date
    )
    
    # Get daily statistics for chart
    daily_stats = []
    current_date = start_date
    while current_date <= end_date:
        day_start = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_stats = calling_agent.call_manager.get_call_statistics(
            agent_id=calling_agent.agent_id,
            start_date=day_start,
            end_date=day_end
        )
        
        daily_stats.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'calls': day_stats['total_calls'],
            'connected': day_stats['connected_calls'],
            'duration': day_stats.get('total_duration_minutes', 0)
        })
        
        current_date += timedelta(days=1)
    
    return render_template('analytics.html', 
                         stats=stats,
                         daily_stats=daily_stats,
                         start_date=start_date.strftime('%Y-%m-%d'),
                         end_date=end_date.strftime('%Y-%m-%d'))

@app.route('/import', methods=['GET', 'POST'])
def import_contacts():
    """Import contacts from CSV"""
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('No file selected!', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('No file selected!', 'error')
                return redirect(request.url)
            
            if file and file.filename.endswith('.csv'):
                # Save uploaded file temporarily
                temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
                file.save(temp_file.name)
                temp_file.close()
                
                # Import contacts
                count = calling_agent.contact_manager.import_contacts_from_csv(temp_file.name)
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
                flash(f'Successfully imported {count} contacts!', 'success')
                return redirect(url_for('contacts'))
            else:
                flash('Please upload a CSV file!', 'error')
                
        except Exception as e:
            flash(f'Error importing contacts: {str(e)}', 'error')
    
    return render_template('import.html')

@app.route('/export')
def export_contacts():
    """Export all contacts to CSV"""
    try:
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        temp_file.close()
        
        if calling_agent.contact_manager.export_contacts_to_csv(temp_file.name):
            return send_file(temp_file.name, 
                           as_attachment=True, 
                           download_name='contacts_export.csv',
                           mimetype='text/csv')
        else:
            flash('Error exporting contacts!', 'error')
            return redirect(url_for('contacts'))
            
    except Exception as e:
        flash(f'Error exporting contacts: {str(e)}', 'error')
        return redirect(url_for('contacts'))

@app.route('/api/contacts/search')
def api_search_contacts():
    """API endpoint for contact search"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify([])
    
    contacts = calling_agent.contact_manager.search_contacts(query, limit)
    
    return jsonify([{
        'id': c.id,
        'name': f"{c.first_name} {c.last_name}",
        'phone': c.phone,
        'email': c.email,
        'company': c.company
    } for c in contacts])

@app.route('/api/stats/realtime')
def api_realtime_stats():
    """API endpoint for real-time statistics"""
    return jsonify({
        'active_calls': len(calling_agent.call_manager.active_calls),
        'queue_size': len(calling_agent.call_queue),
        'is_running': calling_agent.is_running,
        'timestamp': datetime.utcnow().isoformat()
    })

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    # Send initial dashboard data
    emit('dashboard_update', calling_agent.get_dashboard_data())

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('request_update')
def handle_request_update():
    """Handle manual update request"""
    emit('dashboard_update', calling_agent.get_dashboard_data())

# Template filters
@app.template_filter('datetime')
def datetime_filter(value):
    """Format datetime for display"""
    if value is None:
        return 'Never'
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('duration')
def duration_filter(seconds):
    """Format duration in seconds to human readable"""
    if not seconds:
        return '0s'
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

@app.template_filter('percentage')
def percentage_filter(value, decimals=1):
    """Format number as percentage"""
    if value is None:
        return '0.0%'
    return f"{value:.{decimals}f}%"

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

def create_app():
    """Application factory"""
    return app

if __name__ == '__main__':
    # Start background update thread
    update_thread = threading.Thread(target=background_updates)
    update_thread.daemon = True
    update_thread.start()
    
    # Run the application
    print("Starting Quantum Nexus Calling Agent Web Interface...")
    print("Dashboard will be available at: http://localhost:5000")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
        update_thread_stop.set()
        if update_thread:
            update_thread.join()