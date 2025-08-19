# Installation Guide

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.11 or higher
- **Memory**: 4 GB RAM minimum, 8 GB recommended
- **Storage**: 1 GB free disk space
- **Network**: Internet connection for initial setup (optional for operation)

### Recommended Requirements

- **Operating System**: Linux (Ubuntu 22.04 LTS) or Windows Server 2019+
- **Python**: Version 3.11+
- **Memory**: 8 GB RAM or higher
- **Storage**: 10 GB free disk space (for logs and database growth)
- **Network**: Dedicated network segment for security tools

## Installation Methods

### Method 1: Standard Installation

#### Step 1: Download and Extract

1. Download the project archive from GitHub
2. Extract to your desired directory:
   ```bash
   unzip ot-cybersecurity-maturity-tool.zip
   cd ot-cybersecurity-maturity-tool
   ```

#### Step 2: Python Environment Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   
   On Linux/macOS:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```cmd
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

#### Step 3: Database Initialization

The application will automatically create the SQLite database on first run. No manual database setup is required.

#### Step 4: Start the Application

```bash
python src/main.py
```

The application will be available at `http://localhost:5000`

### Method 2: Docker Installation

#### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+ (optional)

#### Step 1: Build Docker Image

```bash
docker build -t ot-security-tool .
```

#### Step 2: Run Container

```bash
docker run -d \
  --name ot-security-tool \
  -p 5000:5000 \
  -v $(pwd)/data:/app/src/database \
  ot-security-tool
```

#### Step 3: Access Application

Navigate to `http://localhost:5000` in your web browser.

### Method 3: Production Deployment

#### Using Gunicorn (Recommended)

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn configuration** (`gunicorn.conf.py`):
   ```python
   bind = "0.0.0.0:5000"
   workers = 4
   worker_class = "sync"
   timeout = 120
   keepalive = 5
   max_requests = 1000
   max_requests_jitter = 100
   preload_app = True
   ```

3. **Start with Gunicorn**:
   ```bash
   gunicorn -c gunicorn.conf.py src.main:app
   ```

#### Using Nginx Reverse Proxy

1. **Install Nginx**:
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Create Nginx configuration** (`/etc/nginx/sites-available/ot-security-tool`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable the site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/ot-security-tool /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///src/database/app.db

# Security Configuration
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Database Configuration

#### SQLite (Default)

No additional configuration required. The database file will be created at `src/database/app.db`.

#### PostgreSQL (Optional)

1. **Install PostgreSQL adapter**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Update configuration**:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/ot_security
   ```

3. **Create database**:
   ```sql
   CREATE DATABASE ot_security;
   CREATE USER ot_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE ot_security TO ot_user;
   ```

### Security Configuration

#### SSL/TLS Setup

1. **Generate SSL certificates**:
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```

2. **Update Flask configuration**:
   ```python
   app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
   ```

#### Firewall Configuration

1. **Allow application port**:
   ```bash
   sudo ufw allow 5000/tcp
   sudo ufw enable
   ```

2. **Restrict access to specific networks**:
   ```bash
   sudo ufw allow from 192.168.1.0/24 to any port 5000
   ```

## Verification

### Health Check

1. **Application Status**:
   ```bash
   curl http://localhost:5000/api/assets/stats
   ```

2. **Database Connectivity**:
   ```bash
   python -c "from src.models.user import db; print('Database OK')"
   ```

### Performance Testing

1. **Load Testing with Apache Bench**:
   ```bash
   ab -n 1000 -c 10 http://localhost:5000/
   ```

2. **Memory Usage Monitoring**:
   ```bash
   ps aux | grep python
   ```

## Troubleshooting

### Common Installation Issues

#### Python Version Conflicts

**Problem**: Multiple Python versions causing conflicts

**Solution**:
```bash
python3.11 -m venv venv
source venv/bin/activate
which python  # Should point to venv/bin/python
```

#### Permission Errors

**Problem**: Database file permission denied

**Solution**:
```bash
sudo chown -R $USER:$USER src/database/
chmod 755 src/database/
chmod 644 src/database/app.db
```

#### Port Already in Use

**Problem**: Port 5000 already occupied

**Solution**:
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>

# Or use different port
python src/main.py --port 5001
```

#### Missing Dependencies

**Problem**: Import errors for required packages

**Solution**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Performance Issues

#### Slow Database Queries

**Problem**: Application responds slowly

**Solution**:
1. Check database size and optimize:
   ```bash
   sqlite3 src/database/app.db "VACUUM;"
   sqlite3 src/database/app.db "ANALYZE;"
   ```

2. Add database indexes if needed

#### High Memory Usage

**Problem**: Application consuming too much memory

**Solution**:
1. Reduce worker processes in Gunicorn
2. Implement database connection pooling
3. Add memory limits to Docker container

### Network Issues

#### CORS Errors

**Problem**: Frontend cannot connect to backend

**Solution**:
Verify CORS configuration in `src/main.py`:
```python
from flask_cors import CORS
CORS(app, origins=['http://localhost:3000', 'http://your-domain.com'])
```

#### SSL Certificate Issues

**Problem**: SSL/TLS connection errors

**Solution**:
1. Verify certificate validity:
   ```bash
   openssl x509 -in cert.pem -text -noout
   ```

2. Check certificate chain:
   ```bash
   openssl verify -CAfile ca-bundle.crt cert.pem
   ```

## Maintenance

### Regular Maintenance Tasks

#### Database Backup

```bash
# Create backup
cp src/database/app.db backups/app_$(date +%Y%m%d_%H%M%S).db

# Automated backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp src/database/app.db "$BACKUP_DIR/app_$DATE.db"
find "$BACKUP_DIR" -name "app_*.db" -mtime +30 -delete
```

#### Log Rotation

```bash
# Configure logrotate
sudo tee /etc/logrotate.d/ot-security-tool << EOF
/path/to/ot-cybersecurity-maturity-tool/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
EOF
```

#### Security Updates

```bash
# Update Python packages
pip list --outdated
pip install --upgrade package-name

# Update system packages
sudo apt update && sudo apt upgrade
```

### Monitoring

#### Application Monitoring

1. **Process Monitoring**:
   ```bash
   # Create systemd service
   sudo tee /etc/systemd/system/ot-security-tool.service << EOF
   [Unit]
   Description=OT Security Tool
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/path/to/ot-cybersecurity-maturity-tool
   ExecStart=/path/to/ot-cybersecurity-maturity-tool/venv/bin/gunicorn -c gunicorn.conf.py src.main:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   EOF
   
   sudo systemctl enable ot-security-tool
   sudo systemctl start ot-security-tool
   ```

2. **Health Check Script**:
   ```bash
   #!/bin/bash
   HEALTH_URL="http://localhost:5000/api/assets/stats"
   
   if curl -f -s "$HEALTH_URL" > /dev/null; then
       echo "$(date): Application is healthy"
   else
       echo "$(date): Application health check failed"
       # Add notification logic here
   fi
   ```

#### Log Monitoring

```bash
# Monitor application logs
tail -f logs/app.log

# Monitor system logs
sudo journalctl -u ot-security-tool -f
```

## Uninstallation

### Complete Removal

1. **Stop the application**:
   ```bash
   sudo systemctl stop ot-security-tool
   sudo systemctl disable ot-security-tool
   ```

2. **Remove application files**:
   ```bash
   rm -rf /path/to/ot-cybersecurity-maturity-tool
   ```

3. **Remove system service**:
   ```bash
   sudo rm /etc/systemd/system/ot-security-tool.service
   sudo systemctl daemon-reload
   ```

4. **Remove Nginx configuration** (if used):
   ```bash
   sudo rm /etc/nginx/sites-enabled/ot-security-tool
   sudo rm /etc/nginx/sites-available/ot-security-tool
   sudo systemctl reload nginx
   ```

5. **Remove database backups** (optional):
   ```bash
   rm -rf /path/to/backups/app_*.db
   ```

## Support

For installation support, please refer to:

- GitHub Issues: [Repository Issues Page]
- Documentation: README.md
- Contact: Moazzam Jafri (Author)

## Next Steps

After successful installation:

1. Review the User Guide in README.md
2. Configure your first assets
3. Set up security baselines
4. Conduct your first assessment
5. Implement monitoring and backup procedures

