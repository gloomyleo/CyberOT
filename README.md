# OT Cybersecurity Maturity Assessment Tool

**Author:** Moazzam Jafri  
**Experience:** 25+ Years in Cybersecurity Industry  
**Version:** 1.0.0  
**License:** MIT

## Overview

The OT Cybersecurity Maturity Assessment Tool is a comprehensive, interactive platform designed to help organizations evaluate, track, and improve their operational technology (OT) security posture. Built on industry-leading frameworks including IEC 62443 and NIST Cybersecurity Framework, this tool provides a structured approach to managing OT cybersecurity risks without causing business interruptions.

### Key Features

- **Asset Management**: Comprehensive inventory and tracking of OT assets with criticality classification
- **Vulnerability Management**: Track and manage security vulnerabilities across your OT environment
- **Maturity Assessments**: Conduct structured cybersecurity assessments based on IEC 62443 and NIST frameworks
- **Configuration Management**: Define security baselines and track configuration deviations
- **Zero Trust Implementation**: Guidance and tracking for Zero Trust principles in OT environments
- **Interactive Dashboard**: Real-time visibility into security posture with charts and metrics
- **Risk-Based Approach**: Prioritize security efforts based on asset criticality and risk levels

### Industry Standards Compliance

This tool is designed around established cybersecurity frameworks:

- **IEC 62443**: The international standard for industrial automation and control systems security
- **NIST Cybersecurity Framework**: Comprehensive framework for managing cybersecurity risks
- **Zero Trust Architecture**: Implementation guidance for Zero Trust principles in OT environments

## Architecture

The application follows a modern full-stack architecture:

- **Frontend**: React.js with Tailwind CSS and shadcn/ui components
- **Backend**: Flask (Python) with RESTful API design
- **Database**: SQLite for simplicity and portability
- **Deployment**: Docker-ready with easy deployment options

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 20.x or higher (for development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ot-cybersecurity-maturity-tool
   ```

2. **Set up the Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python src/main.py
   ```
   The application will automatically create the SQLite database and tables on first run.

4. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

### Default Login

The application currently runs without authentication for simplicity. In a production environment, implement proper authentication and authorization mechanisms.

## User Guide

### Dashboard

The dashboard provides an overview of your OT security posture including:

- Total assets and their criticality distribution
- Open vulnerabilities by severity
- Configuration deviations and their risk levels
- Overall security score and trends
- Recent security activities

### Asset Management

#### Adding Assets

1. Navigate to the "Assets" section
2. Click "Add Asset"
3. Fill in the asset details:
   - **Name**: Unique identifier for the asset
   - **Type**: PLC, HMI, SCADA, DCS, RTU, Sensor, Actuator, Network Device, or Other
   - **Manufacturer**: Asset manufacturer
   - **Model**: Asset model number
   - **Serial Number**: Unique serial number
   - **IP Address**: Network address
   - **Location**: Physical or logical location
   - **Criticality**: Critical, High, Medium, or Low
   - **Description**: Additional details

#### Asset Criticality Levels

- **Critical**: Assets whose failure would cause immediate safety risks or significant business impact
- **High**: Assets important for operations but with some redundancy
- **Medium**: Assets that support operations but have limited impact if compromised
- **Low**: Assets with minimal impact on operations or safety

### Vulnerability Management

#### Reporting Vulnerabilities

1. Navigate to "Vulnerabilities"
2. Click "Report Vulnerability"
3. Provide vulnerability details:
   - **Title**: Descriptive name for the vulnerability
   - **CVE ID**: Common Vulnerabilities and Exposures identifier (if available)
   - **Severity**: Critical, High, Medium, or Low
   - **CVSS Score**: Common Vulnerability Scoring System score (0-10)
   - **Affected Asset**: Select from your asset inventory
   - **Description**: Detailed description of the vulnerability
   - **Status**: Open, In Progress, Resolved, or Accepted Risk

#### Vulnerability Lifecycle

1. **Open**: Newly discovered vulnerability requiring attention
2. **In Progress**: Vulnerability is being actively remediated
3. **Resolved**: Vulnerability has been successfully remediated
4. **Accepted Risk**: Organization has decided to accept the risk

### Security Assessments

#### Creating Assessments

1. Navigate to "Assessments"
2. Click "New Assessment"
3. Select framework (IEC 62443 or NIST)
4. Provide assessment name and description

#### Assessment Frameworks

**IEC 62443 Assessment Categories:**
- Security Governance
- Risk Assessment
- Network Segmentation
- Access Control
- Asset Management
- Incident Response

**NIST Framework Assessment Categories:**
- Identify
- Protect
- Detect
- Respond
- Recover

#### Scoring System

Each assessment question uses a 0-5 maturity scale:
- **0**: Not Implemented
- **1**: Initial (ad-hoc processes)
- **2**: Developing (some processes defined)
- **3**: Defined (documented processes)
- **4**: Managed (measured and controlled processes)
- **5**: Optimized (continuously improving processes)

### Configuration Management

#### Configuration Baselines

1. Navigate to "Configurations" → "Configuration Baselines"
2. Click "Add Baseline"
3. Define secure configuration standards for asset types
4. Document expected configuration parameters

#### Configuration Deviations

1. Navigate to "Configurations" → "Configuration Deviations"
2. Click "Report Deviation"
3. Document deviations from established baselines:
   - **Deviation Type**: Missing, Extra, or Modified
   - **Risk Level**: Critical, High, Medium, or Low
   - **Expected vs. Actual Values**
   - **Remediation Notes**

## API Documentation

The application provides a RESTful API for integration with other systems.

### Asset Endpoints

- `GET /api/assets` - List all assets
- `POST /api/assets` - Create new asset
- `GET /api/assets/{id}` - Get specific asset
- `PUT /api/assets/{id}` - Update asset
- `DELETE /api/assets/{id}` - Delete asset
- `GET /api/assets/stats` - Get asset statistics

### Vulnerability Endpoints

- `GET /api/vulnerabilities` - List all vulnerabilities
- `POST /api/vulnerabilities` - Create new vulnerability
- `GET /api/vulnerabilities/{id}` - Get specific vulnerability
- `PUT /api/vulnerabilities/{id}` - Update vulnerability
- `DELETE /api/vulnerabilities/{id}` - Delete vulnerability
- `GET /api/vulnerabilities/stats` - Get vulnerability statistics

### Assessment Endpoints

- `GET /api/assessments` - List all assessments
- `POST /api/assessments` - Create new assessment
- `GET /api/assessments/{id}` - Get assessment with questions
- `PUT /api/assessments/{id}` - Update assessment
- `PUT /api/assessments/{id}/questions/{question_id}` - Update assessment question
- `DELETE /api/assessments/{id}` - Delete assessment

### Configuration Endpoints

- `GET /api/configuration-baselines` - List configuration baselines
- `POST /api/configuration-baselines` - Create new baseline
- `GET /api/configuration-deviations` - List configuration deviations
- `POST /api/configuration-deviations` - Create new deviation
- `GET /api/configuration-deviations/stats` - Get deviation statistics

## Security Considerations

### Data Protection

- All data is stored locally in SQLite database
- No external data transmission by default
- Implement encryption at rest for sensitive environments
- Regular database backups recommended

### Access Control

- Implement authentication and authorization for production use
- Role-based access control (RBAC) recommended
- Audit logging for all security-related activities
- Session management and timeout policies

### Network Security

- Deploy behind corporate firewall
- Use HTTPS in production environments
- Network segmentation between OT and IT networks
- VPN access for remote administration

## Deployment Options

### Local Development

```bash
python src/main.py
```

### Production Deployment

1. **Using Docker** (recommended)
   ```bash
   docker build -t ot-security-tool .
   docker run -p 5000:5000 ot-security-tool
   ```

2. **Using WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

### Environment Variables

- `FLASK_ENV`: Set to 'production' for production deployment
- `SECRET_KEY`: Change default secret key for production
- `DATABASE_URL`: Custom database connection string (optional)

## Customization

### Adding Custom Assessment Questions

1. Modify the assessment creation functions in `src/routes/assessment.py`
2. Add new question categories and questions
3. Update the frontend components to display new categories

### Custom Asset Types

1. Update the asset type options in the frontend components
2. Modify the database model if additional fields are needed
3. Update API validation rules

### Branding and Styling

1. Modify the React components in `src/components/`
2. Update CSS styles in the frontend
3. Replace logos and branding elements

## Troubleshooting

### Common Issues

**Database Connection Errors**
- Ensure SQLite database file has proper permissions
- Check if database directory exists and is writable

**Frontend Not Loading**
- Verify that the React build files are in the `src/static/` directory
- Check browser console for JavaScript errors

**API Errors**
- Check Flask application logs
- Verify CORS configuration for cross-origin requests
- Ensure all required Python packages are installed

### Logging

Enable debug logging by setting `FLASK_ENV=development` or modifying the Flask configuration.

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/React code
- Add docstrings for all functions and classes
- Include type hints where appropriate

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions, issues, or feature requests, please contact:

**Moazzam Jafri**  
Cybersecurity Professional  
25+ Years Industry Experience

## Acknowledgments

This tool was developed based on industry best practices and standards including:

- IEC 62443 series of standards
- NIST Cybersecurity Framework
- NIST SP 800-82r3 Guide to Operational Technology Security
- Zero Trust Architecture principles

Special thanks to the cybersecurity community for their continued efforts in securing operational technology environments.

