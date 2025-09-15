# Quantum Nexus Calling Agent System

A sophisticated, enterprise-grade calling agent system designed to handle 2M+ contacts with real-time monitoring, advanced campaign management, and comprehensive analytics.

## 🚀 Features

### Core Capabilities
- **Massive Scale**: Handle 2M+ contacts with optimized database performance
- **Real-time Monitoring**: Live dashboard with WebSocket updates
- **Campaign Management**: Advanced scheduling, targeting, and automation
- **Multi-channel Communication**: Voice calls, SMS, and email integration
- **Comprehensive Analytics**: Detailed reporting and performance metrics
- **SOC2-Lite Compliance**: Built-in security and compliance framework

### Advanced Features
- **AI-Powered Insights**: Intelligent call outcome prediction
- **Dynamic Scheduling**: Timezone-aware, business hours optimization
- **Contact Deduplication**: Automatic duplicate detection and merging
- **Bulk Operations**: Efficient mass contact and campaign management
- **API Integration**: RESTful API for external system integration
- **Webhook Support**: Real-time event notifications

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   Calling Agent │    │   Contact Mgmt  │
│   (Flask + WS)  │◄──►│   (Core Logic)  │◄──►│   (2M+ Records) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dashboard     │    │   Campaign Mgr  │    │   Analytics     │
│   (Real-time)   │    │   (Scheduler)   │    │   (Reporting)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.8+
- Redis (for caching and background tasks)
- PostgreSQL (recommended for production)
- Twilio Account (for voice/SMS)

### Quick Start

1. **Clone and Setup**
   ```bash
   cd agents/calling-agent
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database Setup**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Access Dashboard**
   Open http://localhost:5000 in your browser

## ⚙️ Configuration

### Environment Variables

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost/calling_agent

# Redis
REDIS_URL=redis://localhost:6379/0

# Twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Calling Configuration
MAX_CONCURRENT_CALLS=10
CALL_TIMEOUT_SECONDS=30
RETRY_ATTEMPTS=3

# Security
API_KEY=your-api-key
WEBHOOK_SECRET=your-webhook-secret
```

### Advanced Configuration

See `config.py` for comprehensive configuration options including:
- Campaign scheduling settings
- Contact import/export options
- Security and compliance settings
- Analytics and reporting configuration

## 📊 Usage

### Dashboard Overview
The main dashboard provides:
- Real-time agent status
- Active campaign monitoring
- Contact queue management
- Performance metrics
- Quick action buttons

### Contact Management
- **Import**: Bulk import from CSV/Excel files
- **Export**: Export contact lists and call results
- **Deduplication**: Automatic duplicate detection
- **Segmentation**: Advanced filtering and grouping
- **Bulk Operations**: Mass updates and campaign assignments

### Campaign Management
- **Creation**: Wizard-based campaign setup
- **Scheduling**: Timezone-aware scheduling
- **Targeting**: Advanced contact filtering
- **Monitoring**: Real-time progress tracking
- **Analytics**: Comprehensive performance reports

### API Usage

```python
import requests

# Add contact via API
response = requests.post('http://localhost:5000/api/contacts', 
    headers={'Authorization': 'Bearer YOUR_API_KEY'},
    json={
        'name': 'John Doe',
        'phone': '+1234567890',
        'email': 'john@example.com'
    }
)

# Start campaign
response = requests.post('http://localhost:5000/api/campaigns/123/start',
    headers={'Authorization': 'Bearer YOUR_API_KEY'}
)
```

## 🔧 Development

### Project Structure
```
calling-agent/
├── app.py                 # Main application entry
├── config.py             # Configuration management
├── calling_agent.py      # Core calling logic
├── web_interface.py      # Flask web application
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── contacts.html
│   └── campaigns.html
├── static/              # CSS, JS, images
├── migrations/          # Database migrations
└── tests/              # Test suite
```

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Linting
flake8 .

# Type checking
mypy .

# Security scan
bandit -r .
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t quantum-calling-agent .

# Run container
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  quantum-calling-agent
```

### Production Deployment
1. Use PostgreSQL for database
2. Configure Redis for caching
3. Set up SSL/TLS certificates
4. Configure monitoring and logging
5. Set up backup procedures

## 📈 Performance

### Optimization Features
- **Database Indexing**: Optimized for 2M+ contact queries
- **Connection Pooling**: Efficient database connections
- **Caching**: Redis-based caching for frequent queries
- **Background Tasks**: Celery for async processing
- **Rate Limiting**: API and calling rate limits

### Scaling Recommendations
- **Horizontal Scaling**: Multiple application instances
- **Database Sharding**: For 10M+ contacts
- **CDN**: For static assets
- **Load Balancing**: Distribute traffic across instances

## 🔒 Security

### Built-in Security Features
- SOC2-Lite compliance framework
- API key authentication
- Rate limiting and DDoS protection
- Input validation and sanitization
- Secure session management
- CSRF protection

### Compliance Features
- Do Not Call (DNC) list management
- Call recording compliance
- Data retention policies
- Audit logging
- GDPR compliance tools

## 📞 Integrations

### Supported Platforms
- **Twilio**: Voice calls and SMS
- **SendGrid**: Email campaigns
- **Salesforce**: CRM integration
- **HubSpot**: Marketing automation
- **Zapier**: Workflow automation

### Webhook Events
- Call started/completed
- Campaign status changes
- Contact updates
- System alerts

## 🆘 Support

### Troubleshooting
- Check logs in `logs/calling_agent.log`
- Verify Twilio credentials
- Ensure Redis is running
- Check database connectivity

### Common Issues
1. **Calls not connecting**: Verify Twilio configuration
2. **Slow performance**: Check database indexes
3. **Memory issues**: Increase Redis memory limit
4. **Import failures**: Validate CSV format

## 📄 License

This project is part of the Quantum Nexus ecosystem and follows the project's licensing terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

---

**Quantum Nexus Calling Agent** - Empowering businesses with intelligent, scalable communication solutions.