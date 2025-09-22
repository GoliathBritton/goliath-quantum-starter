# Quantum Omniscient™ Domain Setup Script
# Configures custom domain for production deployment

param(
    [Parameter(Mandatory=$true)]
    [string]$DomainName,
    
    [Parameter(Mandatory=$false)]
    [string]$Environment = "production",
    
    [Parameter(Mandatory=$false)]
    [string]$ServerIP = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$SetupSSL = $true
)

Write-Host "🌐 Quantum Omniscient™ Domain Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Validate domain name
if (-not ($DomainName -match "^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$")) {
    Write-Host "❌ Invalid domain name format: $DomainName" -ForegroundColor Red
    exit 1
}

Write-Host "🔧 Setting up domain: $DomainName" -ForegroundColor Green
Write-Host "📍 Environment: $Environment" -ForegroundColor Yellow

# Create environment-specific .env file
$envFile = ".env.$Environment"
$envContent = @"
# Quantum Omniscient™ Domain Configuration
DOMAIN_NAME=$DomainName
APP_URL=https://$DomainName
NEXT_PUBLIC_APP_URL=https://$DomainName
NEXT_PUBLIC_API_URL=https://api.$DomainName
NEXT_PUBLIC_WS_URL=wss://ws.$DomainName

# Environment
NODE_ENV=$Environment
ENVIRONMENT=$Environment

# Security
FORCE_HTTPS=true
HSTS_ENABLED=true

# API Configuration
API_BASE_URL=https://api.$DomainName
WEBSOCKET_URL=wss://ws.$DomainName

# Quantum Omniscient™ Branding
NEXT_PUBLIC_BRAND_NAME=Quantum Omniscient™
NEXT_PUBLIC_BRAND_TAGLINE=The Future of Quantum Intelligence

# JWT Configuration (generate new secret for production)
JWT_SECRET=quantum-omniscient-$(Get-Random -Minimum 100000 -Maximum 999999)
JWT_EXPIRES_IN=24h

# Database (update with your production database)
DATABASE_URL=postgresql://user:password@localhost:5432/quantum_omniscient
REDIS_URL=redis://localhost:6379

# Payment Configuration
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Email Configuration
SMTP_HOST=smtp.your-provider.com
SMTP_PORT=587
SMTP_USER=noreply@$DomainName
SMTP_PASS=your_smtp_password

# Analytics
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
MIXPANEL_TOKEN=your_mixpanel_token
"@

Write-Host "📝 Creating environment file: $envFile" -ForegroundColor Blue
$envContent | Out-File -FilePath $envFile -Encoding UTF8

# Update domain configuration
Write-Host "🔄 Updating domain configuration..." -ForegroundColor Blue
$domainConfig = Get-Content "domain-config.json" | ConvertFrom-Json

if ($Environment -eq "production") {
    $domainConfig.domains.production.primary = $DomainName
    $domainConfig.domains.production.api = "api.$DomainName"
    $domainConfig.domains.production.websocket = "wss://ws.$DomainName"
    $domainConfig.domains.production.cdn = "cdn.$DomainName"
} elseif ($Environment -eq "staging") {
    $domainConfig.domains.staging.primary = $DomainName
    $domainConfig.domains.staging.api = "api.$DomainName"
    $domainConfig.domains.staging.websocket = "wss://ws.$DomainName"
}

# Update DNS records if server IP provided
if ($ServerIP) {
    Write-Host "🌍 Updating DNS configuration for IP: $ServerIP" -ForegroundColor Green
    $domainConfig.dns.records[0].content = $ServerIP
}

$domainConfig | ConvertTo-Json -Depth 10 | Out-File "domain-config.json" -Encoding UTF8

# Create Nginx configuration for domain
$nginxConfig = @"
# Quantum Omniscient™ Nginx Configuration
server {
    listen 80;
    server_name $DomainName www.$DomainName;
    
    # Redirect HTTP to HTTPS
    return 301 https://`$server_name`$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DomainName www.$DomainName;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/$DomainName/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DomainName/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header Referrer-Policy "origin-when-cross-origin";
    add_header X-Powered-By "Quantum Omniscient™";
    
    # Main application
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade `$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
        proxy_cache_bypass `$http_upgrade;
    }
    
    # API routes
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
    }
    
    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade `$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
    }
}

# API subdomain
server {
    listen 443 ssl http2;
    server_name api.$DomainName;
    
    ssl_certificate /etc/letsencrypt/live/$DomainName/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DomainName/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
    }
}
"@

Write-Host "🔧 Creating Nginx configuration..." -ForegroundColor Blue
$nginxConfig | Out-File -FilePath "nginx-$DomainName.conf" -Encoding UTF8

# Create SSL setup script
if ($SetupSSL) {
    $sslScript = @"
#!/bin/bash
# SSL Certificate Setup for $DomainName

echo "🔒 Setting up SSL certificate for $DomainName"

# Install Certbot if not already installed
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    sudo apt-get update
    sudo apt-get install -y certbot python3-certbot-nginx
fi

# Obtain SSL certificate
sudo certbot --nginx -d $DomainName -d www.$DomainName -d api.$DomainName -d ws.$DomainName

# Set up auto-renewal
sudo crontab -l | grep -q certbot || (sudo crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | sudo crontab -

echo "✅ SSL certificate setup complete for $DomainName"
"@

    $sslScript | Out-File -FilePath "setup-ssl-$DomainName.sh" -Encoding UTF8
    Write-Host "🔒 Created SSL setup script: setup-ssl-$DomainName.sh" -ForegroundColor Green
}

# Display next steps
Write-Host "`n✅ Domain setup complete!" -ForegroundColor Green
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update your DNS records to point to your server IP" -ForegroundColor White
Write-Host "2. Copy nginx-$DomainName.conf to your server's Nginx sites-available" -ForegroundColor White
Write-Host "3. Run setup-ssl-$DomainName.sh on your server to configure SSL" -ForegroundColor White
Write-Host "4. Update your environment variables in $envFile" -ForegroundColor White
Write-Host "5. Deploy your application with: npm run build && npm start" -ForegroundColor White

Write-Host "`n🌐 Your Quantum Omniscient™ platform will be available at:" -ForegroundColor Cyan
Write-Host "   Main site: https://$DomainName" -ForegroundColor Green
Write-Host "   API: https://api.$DomainName" -ForegroundColor Green
Write-Host "   WebSocket: wss://ws.$DomainName" -ForegroundColor Green

Write-Host "`n🔧 Configuration files created:" -ForegroundColor Yellow
Write-Host "   - $envFile (environment variables)" -ForegroundColor White
Write-Host "   - nginx-$DomainName.conf (web server config)" -ForegroundColor White
Write-Host "   - setup-ssl-$DomainName.sh (SSL setup script)" -ForegroundColor White
Write-Host "   - domain-config.json (updated)" -ForegroundColor White