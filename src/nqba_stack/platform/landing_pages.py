"""
FLYFOX AI Dynamic Landing Page Generator
========================================

Generates professional landing pages for all FLYFOX AI services:
- AI Agents (Standalone & Packages)
- QAIaaS Platform
- Custom Development Services
- Industry-Specific Solutions
- QAaaS Platform
"""

import json
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class LandingPageType(Enum):
    """Types of landing pages"""
    AI_AGENT = "ai_agent"
    QAIAAS = "qaias"
    CUSTOM_DEVELOPMENT = "custom_development"
    INDUSTRY_SOLUTION = "industry_solution"
    QAAS = "qaas"

@dataclass
class LandingPageConfig:
    """Configuration for landing page generation"""
    page_type: LandingPageType
    service_name: str
    service_description: str
    features: List[str]
    pricing: Dict[str, Any]
    target_audience: str
    call_to_action: str
    branding: str = "FLYFOX AI"

class LandingPageGenerator:
    """Generates dynamic landing pages for FLYFOX AI services"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load HTML templates for different page types"""
        return {
            "base": self._get_base_template(),
            "ai_agent": self._get_ai_agent_template(),
            "qaias": self._get_qaias_template(),
            "custom_development": self._get_custom_development_template(),
            "qaas": self._get_qaas_template()
        }
    
    def generate_landing_page(self, config: LandingPageConfig) -> str:
        """Generate a complete landing page based on configuration"""
        template = self.templates.get(config.page_type.value, self.templates["base"])
        
        # Replace placeholders with actual content
        html = template.replace("{{SERVICE_NAME}}", config.service_name)
        html = html.replace("{{SERVICE_DESCRIPTION}}", config.service_description)
        html = html.replace("{{BRANDING}}", config.branding)
        html = html.replace("{{TARGET_AUDIENCE}}", config.target_audience)
        html = html.replace("{{CALL_TO_ACTION}}", config.call_to_action)
        
        # Generate features HTML
        features_html = self._generate_features_html(config.features)
        html = html.replace("{{FEATURES}}", features_html)
        
        # Generate pricing HTML
        pricing_html = self._generate_pricing_html(config.pricing)
        html = html.replace("{{PRICING}}", pricing_html)
        
        return html
    
    def _generate_features_html(self, features: List[str]) -> str:
        """Generate HTML for features list"""
        features_html = ""
        for feature in features:
            features_html += f'<li class="feature-item">✅ {feature}</li>\n'
        return features_html
    
    def _generate_pricing_html(self, pricing: Dict[str, Any]) -> str:
        """Generate HTML for pricing section"""
        pricing_html = ""
        for tier, details in pricing.items():
            pricing_html += f"""
            <div class="pricing-tier">
                <h3>{tier.title()}</h3>
                <div class="price">{details.get('price', 'Contact Sales')}</div>
                <ul class="tier-features">
            """
            for feature in details.get('features', []):
                pricing_html += f'<li>{feature}</li>\n'
            pricing_html += "</ul></div>"
        return pricing_html
    
    def _get_base_template(self) -> str:
        """Base HTML template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{SERVICE_NAME}} - {{BRANDING}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }
        .hero { padding: 4rem 2rem; text-align: center; background: #f8f9fa; }
        .features { padding: 4rem 2rem; background: white; }
        .pricing { padding: 4rem 2rem; background: #f8f9fa; }
        .contact { padding: 4rem 2rem; background: white; }
        .cta { padding: 4rem 2rem; background: #667eea; color: white; text-align: center; }
        .feature-item { margin: 1rem 0; font-size: 1.1rem; }
        .pricing-tier { border: 1px solid #ddd; padding: 2rem; margin: 1rem; border-radius: 8px; display: inline-block; width: 300px; }
        .price { font-size: 2rem; font-weight: bold; color: #667eea; margin: 1rem 0; }
        .contact-form { max-width: 600px; margin: 0 auto; }
        .form-group { margin: 1rem 0; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; }
        .form-group textarea { height: 120px; resize: vertical; }
        .submit-btn { background: #667eea; color: white; padding: 1rem 2rem; border: none; border-radius: 5px; font-size: 1.2rem; cursor: pointer; width: 100%; }
        .submit-btn:hover { background: #5a6fd8; }
        .contact-info { background: #f8f9fa; padding: 2rem; border-radius: 8px; margin: 2rem 0; }
        .contact-method { display: flex; align-items: center; margin: 1rem 0; }
        .contact-method i { margin-right: 1rem; font-size: 1.5rem; color: #667eea; }
        .live-chat { position: fixed; bottom: 2rem; right: 2rem; background: #667eea; color: white; padding: 1rem; border-radius: 50px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .live-chat:hover { background: #5a6fd8; transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{BRANDING}}</h1>
        <p>Quantum-Enhanced AI Solutions</p>
        <div style="margin-top: 1rem;">
            <a href="mailto:hello@flyfox.ai" style="color: white; text-decoration: none; margin: 0 1rem;">📧 hello@flyfox.ai</a>
            <a href="tel:+1-555-FLYFOX" style="color: white; text-decoration: none; margin: 0 1rem;">📞 +1-555-FLYFOX</a>
        </div>
    </div>
    
    <div class="hero">
        <h1>{{SERVICE_NAME}}</h1>
        <p>{{SERVICE_DESCRIPTION}}</p>
        <p>Perfect for: {{TARGET_AUDIENCE}}</p>
    </div>
    
    <div class="features">
        <h2>Key Features</h2>
        <ul>{{FEATURES}}</ul>
    </div>
    
    <div class="pricing">
        <h2>Pricing Plans</h2>
        {{PRICING}}
    </div>
    
    <div class="contact">
        <h2>Get In Touch With Our Team</h2>
        <p>Ready to transform your business with quantum-enhanced AI? Our FLYFOX AI family is here to help!</p>
        
        <div class="contact-info">
            <h3>📞 Direct Contact</h3>
            <div class="contact-method">
                <span>📧</span>
                <div>
                    <strong>Email:</strong> <a href="mailto:hello@flyfox.ai">hello@flyfox.ai</a><br>
                    <small>Response within 2 hours during business hours</small>
                </div>
            </div>
            <div class="contact-method">
                <span>📱</span>
                <div>
                    <strong>Phone:</strong> <a href="tel:+1-555-FLYFOX">+1-555-FLYFOX</a><br>
                    <small>Available Mon-Fri 9AM-6PM EST</small>
                </div>
            </div>
            <div class="contact-method">
                <span>💬</span>
                <div>
                    <strong>Live Chat:</strong> Available 24/7<br>
                    <small>Click the chat bubble to start talking</small>
                </div>
            </div>
            <div class="contact-method">
                <span>🌐</span>
                <div>
                    <strong>Website:</strong> <a href="https://flyfoxai.io" target="_blank">flyfoxai.io</a><br>
                    <small>Learn more about our complete AI ecosystem</small>
                </div>
            </div>
        </div>
        
        <div class="contact-form">
            <h3>📝 Send Us a Message</h3>
            <form id="contactForm" onsubmit="submitContactForm(event)">
                <div class="form-group">
                    <label for="name">Full Name *</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email Address *</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="company">Company Name</label>
                    <input type="text" id="company" name="company">
                </div>
                <div class="form-group">
                    <label for="service">Service Interest</label>
                    <select id="service" name="service">
                        <option value="">Select a service...</option>
                        <option value="qdllm">qdLLM Platform</option>
                        <option value="ai_agents">AI Agent Suite</option>
                        <option value="qaias">QAIaaS Platform</option>
                        <option value="custom_development">Custom Development</option>
                        <option value="industrial_ai">Industrial AI & Energy</option>
                        <option value="web3_ai">Web3 AI Integration</option>
                        <option value="white_label">White Label Solutions</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="message">How can we help you? *</label>
                    <textarea id="message" name="message" placeholder="Tell us about your project, goals, or questions..." required></textarea>
                </div>
                <div class="form-group">
                    <label for="timeline">Timeline</label>
                    <select id="timeline" name="timeline">
                        <option value="">Select timeline...</option>
                        <option value="immediate">Immediate (This week)</option>
                        <option value="soon">Soon (Next 2-4 weeks)</option>
                        <option value="planning">Planning (Next 1-3 months)</option>
                        <option value="future">Future consideration</option>
                    </select>
                </div>
                <button type="submit" class="submit-btn">🚀 Send Message to FLYFOX AI Team</button>
            </form>
        </div>
    </div>
    
    <div class="cta">
        <h2>{{CALL_TO_ACTION}}</h2>
        <button style="background: white; color: #667eea; padding: 1rem 2rem; border: none; border-radius: 5px; font-size: 1.2rem; cursor: pointer;">
            Get Started Today
        </button>
    </div>
    
    <div class="live-chat" onclick="openLiveChat()">
        💬 Live Chat
    </div>
    
    <script>
        function submitContactForm(event) {
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const data = Object.fromEntries(formData);
            
            // Simulate form submission
            alert('Thank you for your message! Our FLYFOX AI team will get back to you within 2 hours.\n\nWe\'ve received your inquiry about: ' + data.service + '\n\nYou can also reach us directly at hello@flyfox.ai or call +1-555-FLYFOX');
            
            // Reset form
            event.target.reset();
        }
        
        function openLiveChat() {
            alert('Live Chat Feature\n\nThis would integrate with our live chat system.\n\nFor immediate assistance, please email hello@flyfox.ai or call +1-555-FLYFOX');
        }
    </script>
</body>
</html>
        """
    
    def _get_ai_agent_template(self) -> str:
        """AI Agent landing page template"""
        return self._get_base_template()
    
    def _get_qaias_template(self) -> str:
        """QAIaaS landing page template"""
        return self._get_base_template()
    
    def _get_custom_development_template(self) -> str:
        """Custom Development landing page template"""
        return self._get_base_template()
    
    def _get_qaas_template(self) -> str:
        """QAaaS landing page template"""
        return self._get_base_template()
