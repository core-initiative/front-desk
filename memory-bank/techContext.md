# Technical Context: Inn Hotels

## Technology Stack

### **Core Framework**
- **Frappe Framework**: v14+ (Python-based ERP framework)
- **Python**: 3.8+ (Backend language)
- **MySQL**: 8.0+ (Primary database with InnoDB engine)
- **JavaScript**: ES6+ (Frontend scripting)
- **HTML/CSS**: Web interface rendering

### **Dependencies**
```
Primary Dependencies:
├── frappe (Core framework)
├── mysqlclient (Database connector)
├── requests (HTTP client for API calls)
├── jinja2 (Template engine)
└── werkzeug (WSGI utilities)

Development Dependencies:
├── pytest (Testing framework)
├── black (Code formatting)
├── flake8 (Linting)
└── mypy (Type checking)
```

### **External Integrations**
- **Door Lock Systems**: TESA, DOWS APIs
- **WiFi Hotspot**: Custom provider APIs
- **Payment Gateways**: Multiple payment processor integrations
- **Channel Managers**: OTA and distribution system APIs

## Development Environment

### **System Requirements**
- **Operating System**: Linux (Ubuntu 20.04+), macOS, Windows with WSL
- **Python**: 3.8+ with virtual environment support
- **Node.js**: 16+ for frontend asset compilation
- **MySQL**: 8.0+ with InnoDB support
- **Redis**: 6.0+ for caching and session management

### **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd front-desk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup Frappe bench
bench init
bench get-app inn
bench install-app inn

# Start development server
bench start
```

### **Database Configuration**
```python
# Database settings in site_config.json
{
    "db_host": "localhost",
    "db_port": 3306,
    "db_name": "inn_hotels",
    "db_user": "inn_user",
    "db_password": "secure_password"
}
```

## Architecture Components

### **Backend Services**
- **Frappe Server**: Main application server
- **Celery**: Background task processing
- **Redis**: Caching and session storage
- **MySQL**: Primary data persistence
- **File Storage**: Local or cloud-based file management

### **Frontend Components**
- **Frappe UI**: Built-in web interface framework
- **JavaScript Modules**: Custom business logic
- **CSS/SCSS**: Styling and theming
- **Print Formats**: PDF generation and printing
- **Mobile Responsiveness**: Adaptive design for various devices

### **Integration Services**
- **API Gateway**: External system communication
- **Webhook Handlers**: Real-time event processing
- **Data Synchronization**: Multi-system data consistency
- **Error Handling**: Comprehensive error management and logging

## Development Workflow

### **Code Organization**
```
inn/
├── __init__.py              # Package initialization
├── config/                  # Configuration files
├── fixtures/                # Initial data and configurations
├── helper/                  # Utility functions and helpers
├── hooks.py                 # Frappe framework hooks
├── inn_hotels/             # Main application module
│   ├── doctype/            # Document type definitions
│   ├── page/               # Custom web pages
│   ├── report/             # Reporting modules
│   ├── print_format/       # Print templates
│   └── workspace/          # Dashboard configurations
├── overrides/               # Framework overrides
├── public/                  # Static assets
└── templates/               # Email and page templates
```

### **Document Type Structure**
Each DocType follows Frappe's standard structure:
```
doctype_name/
├── __init__.py             # Python model
├── doctype_name.json       # Schema definition
├── doctype_name.js         # Client-side logic
├── doctype_name.py         # Server-side logic
├── doctype_name_list.js    # List view customization
└── doctype_name_list.html  # List view template
```

### **Development Patterns**
- **Document Lifecycle**: Create → Validate → Save → Submit → Approve
- **Field Validation**: Server-side and client-side validation
- **Permission Control**: Role-based access at document and field levels
- **Audit Trail**: Automatic logging of all changes
- **Workflow Automation**: Automated business process execution

## Testing Strategy

### **Testing Framework**
- **Unit Tests**: Python unittest framework
- **Integration Tests**: Frappe testing utilities
- **Frontend Tests**: JavaScript testing with Jest
- **Database Tests**: MySQL-specific test scenarios
- **API Tests**: External integration testing

### **Test Organization**
```
tests/
├── unit/                   # Unit tests for individual functions
├── integration/            # Integration tests for modules
├── fixtures/               # Test data and configurations
└── utils/                  # Testing utilities and helpers
```

## Deployment & Operations

### **Production Environment**
- **Web Server**: Nginx or Apache with WSGI
- **Application Server**: Gunicorn or uWSGI
- **Database**: MySQL with replication and backup
- **Caching**: Redis for performance optimization
- **Monitoring**: Application and system monitoring

### **Configuration Management**
- **Environment Variables**: Sensitive configuration management
- **Site Configuration**: Frappe-specific settings
- **Database Migrations**: Schema evolution management
- **Backup Strategy**: Automated backup and recovery procedures

### **Performance Optimization**
- **Database Indexing**: Strategic index creation for query optimization
- **Query Optimization**: Efficient database query patterns
- **Caching Strategy**: Intelligent caching for frequently accessed data
- **Asset Optimization**: Minification and compression of static assets

## Security Considerations

### **Authentication & Authorization**
- **User Management**: Frappe's built-in user system
- **Role-Based Access**: Granular permissions for different user types
- **Session Management**: Secure session handling and timeout controls
- **Password Policies**: Strong password requirements and encryption

### **Data Protection**
- **Encryption**: Data encryption at rest and in transit
- **Audit Logging**: Comprehensive logging of all system activities
- **Input Validation**: Protection against injection attacks
- **Access Control**: Restrictive access to sensitive data and functions

### **Integration Security**
- **API Security**: Secure external API communication
- **Webhook Validation**: Secure webhook endpoint handling
- **Data Sanitization**: Clean external data before processing
- **Error Handling**: Secure error messages without information leakage
