# MISP User Manual

## Welcome to MISP Integration

This user manual provides comprehensive guidance for using MISP (Malware Information Sharing Platform) within the unified executive function dashboard. The MISP integration maintains full compatibility with original MISP functionality while providing enhanced user experience and performance.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Navigation](#dashboard-navigation)  
3. [Event Management](#event-management)
4. [Attribute Management](#attribute-management)
5. [Threat Intelligence Correlation](#threat-intelligence-correlation)
6. [Organization Management](#organization-management)
7. [Taxonomies and Tagging](#taxonomies-and-tagging)
8. [Data Import and Export](#data-import-and-export)
9. [Search and Analysis](#search-and-analysis)
10. [User Preferences](#user-preferences)
11. [Security Features](#security-features)
12. [Troubleshooting](#troubleshooting)

## Getting Started

### Accessing MISP

1. **Login to Platform:**
   - Navigate to your platform URL
   - Use your assigned credentials
   - Enable two-factor authentication if prompted

2. **Navigate to Security Domain:**
   - Click "Security" in the main navigation
   - Select "MISP" from the security tools menu
   - You'll see the MISP dashboard with your organization's data

3. **First-Time Setup:**
   - Complete your user profile
   - Set notification preferences  
   - Configure executive function accommodations
   - Review organization settings

### User Interface Overview

The MISP interface consists of:
- **Navigation Bar**: Quick access to main functions
- **Dashboard**: Overview of recent events and statistics
- **Tool Panel**: Context-sensitive actions
- **Content Area**: Main workspace for events, attributes, etc.
- **Status Bar**: Connection status and real-time updates

### Executive Function Accommodations

The platform includes accommodations for ADHD/autism users:

**Focus Support:**
- Distraction-free mode (press F11)
- Progress indicators for all operations
- Auto-save every 30 seconds
- Session preservation across browser restarts

**Navigation Consistency:**
- Same menu patterns across all tools
- Persistent breadcrumb navigation
- Context preservation when switching tools
- Clear visual indicators for current location

**Cognitive Load Reduction:**
- Progressive disclosure of complex features
- Consistent terminology and icons
- Simplified workflows with step-by-step guidance
- Optional tutorial overlays for new features

## Dashboard Navigation

### Main Dashboard

The MISP dashboard provides an overview of your threat intelligence data:

**Key Metrics:**
- Total events in your organization
- Recent attribute additions
- Correlation statistics
- Sharing activity summary

**Recent Activity:**
- Latest events created or modified
- New correlations discovered
- External feed updates
- System notifications

**Quick Actions:**
- Create new event
- Import threat data
- Search existing events
- Export reports

### Navigation Menu

**Events Section:**
- List Events: Browse all events with filtering
- Create Event: Start new threat intelligence event
- Import Events: Bulk import from various formats
- Event Templates: Use predefined event structures

**Attributes Section:**
- Browse Attributes: Search and filter IOCs
- Add Attributes: Manually add indicators
- Bulk Import: CSV/JSON attribute import
- Correlation View: See attribute relationships

**Analysis Section:**
- Correlations: Explore threat relationships
- Search: Advanced search capabilities
- Reports: Generate threat intelligence reports
- Statistics: Usage and trend analysis

**Administration Section:**
- Organizations: Manage sharing partners
- Taxonomies: Browse classification systems
- Users: User and role management (admin only)
- Settings: Configuration and preferences

## Event Management

### Creating Events

1. **Start New Event:**
   - Click "Create Event" button
   - Fill in required information:
     - **Info**: Brief description of the threat
     - **Threat Level**: Select 1-4 (1=High, 4=Undefined)
     - **Analysis**: Select 0-2 (0=Initial, 1=Ongoing, 2=Complete)
     - **Distribution**: Set sharing level (0-4)

2. **Event Information Fields:**
   ```
   Info: APT campaign targeting financial institutions
   Threat Level: High (1)
   Analysis: Ongoing (1)
   Distribution: Organization only (1)
   Tags: apt, banking-malware, targeted-attack
   ```

3. **Save and Continue:**
   - Click "Save Event"
   - Event is created and ready for attributes
   - Automatic correlation begins immediately

### Editing Events

1. **Open Event:**
   - Click event title in event list
   - Or use search to find specific event
   - Event details page opens

2. **Modify Information:**
   - Click "Edit" button in event header
   - Update any field as needed
   - Changes are auto-saved every 30 seconds
   - Click "Save Changes" to commit immediately

3. **Version Control:**
   - All changes are tracked with timestamps
   - Previous versions accessible via "History" tab
   - Rollback capability for administrators

### Event Status Management

**Analysis Levels:**
- **Initial (0)**: Newly created, basic information
- **Ongoing (1)**: Investigation in progress, being enriched  
- **Complete (2)**: Analysis finished, ready for sharing

**Publication Status:**
- **Draft**: Visible only to your organization
- **Published**: Shared according to distribution level
- **Withdrawn**: Marked as no longer relevant

### Event Collaboration

**Comments and Notes:**
- Add investigation notes to events
- Collaborate with team members
- Track analysis progress
- Document evidence and sources

**Sharing Controls:**
- Set distribution levels per event
- Configure sharing groups
- Manage external partner access
- Control data sensitivity levels

## Attribute Management

### Understanding Attributes

Attributes are indicators of compromise (IOCs) and contextual information associated with events:

**Common Attribute Types:**
- **Network**: IP addresses, domains, URLs
- **File**: Hashes (MD5, SHA1, SHA256), filenames
- **Email**: Addresses, subjects, message IDs
- **Registry**: Windows registry keys and values
- **Mutex**: Malware mutex names
- **Other**: Custom indicators and context

### Adding Attributes

1. **Within Event View:**
   - Open an event
   - Click "Add Attribute" button
   - Select attribute category and type
   - Enter the indicator value
   - Set detection flag (to_ids)
   - Add comments if needed

2. **Attribute Form Example:**
   ```
   Category: Network activity
   Type: domain
   Value: malicious-domain.example.com
   For IDS: Yes (checked)
   Distribution: Inherit from event
   Comment: C2 domain observed in network logs
   ```

3. **Bulk Import:**
   - Use "Bulk Import" for multiple attributes
   - Supports CSV, JSON, and text formats
   - Automatic validation and deduplication
   - Preview before final import

### Attribute Validation

The system automatically validates attributes:

**Format Validation:**
- IP addresses: IPv4/IPv6 format checking
- Domains: DNS name validation  
- Hashes: Length and character validation
- URLs: Well-formed URL validation

**Intelligence Enrichment:**
- Automatic reputation lookups
- Geolocation data for IPs
- WHOIS information for domains
- File signature analysis for hashes

**Duplicate Detection:**
- Checks against existing attributes
- Suggests similar existing indicators
- Prevents duplicate entries
- Offers merge options for conflicts

### Attribute Lifecycle

**Creation:**
- New attributes trigger automatic correlation
- Background enrichment begins immediately
- Validation results appear within seconds

**Updates:**
- Modifications re-trigger correlation
- Change history maintained
- Impact on related events calculated

**Expiration:**
- Optional expiration dates for temporal IOCs
- Automatic archiving of old indicators
- Retention policy enforcement

## Threat Intelligence Correlation

### Automatic Correlation

The system automatically correlates attributes across events:

**Correlation Types:**
- **Exact Match**: Identical attribute values
- **Infrastructure Overlap**: Related IP/domain relationships
- **Hash Relationships**: File variants and families
- **Temporal Proximity**: Indicators from similar timeframes
- **Campaign Attribution**: Patterns suggesting same threat actor

### Viewing Correlations

1. **Attribute Level:**
   - Click any attribute value
   - Correlation panel shows related indicators
   - Click "View Details" for full correlation report

2. **Event Level:**
   - "Correlations" tab in event view
   - Shows all related events and confidence scores
   - Interactive graph visualization available

3. **Correlation Details:**
   ```
   Attribute: malicious-domain.example.com
   Correlations Found: 12
   
   Related Events:
   - Event #123: APT Campaign Phase 2 (confidence: 0.95)
   - Event #124: Banking Trojan Infrastructure (confidence: 0.87)
   - Event #125: Phishing Campaign (confidence: 0.72)
   
   Related Attributes:
   - 192.168.1.100 (IP resolution)
   - suspicious-file.exe (same infrastructure)
   - phishing@example.com (same domain)
   ```

### Correlation Analysis

**Confidence Scoring:**
- 0.9-1.0: Very High (exact/near-exact matches)
- 0.7-0.9: High (strong indicators)
- 0.5-0.7: Medium (possible relationships)
- 0.3-0.5: Low (weak connections)
- 0.0-0.3: Very Low (statistical noise)

**Attribution Intelligence:**
- Threat actor mapping
- Campaign clustering
- Technique classification (MITRE ATT&CK)
- Geographic attribution
- Temporal analysis

### Manual Correlation

1. **Create Relationships:**
   - Select multiple attributes
   - Click "Create Correlation"
   - Specify relationship type
   - Add confidence assessment

2. **Correlation Types:**
   - Infrastructure: Shared hosting, DNS relationships
   - Campaign: Same threat actor or operation
   - Variant: Malware family relationships
   - Victimology: Common target patterns

## Organization Management

### Your Organization

**Organization Profile:**
- Name and description
- Contact information
- Sector and nationality
- Trust relationships
- Sharing agreements

**Members and Roles:**
- User management (admin only)
- Role assignments
- Permission levels
- Activity monitoring

### Sharing Partners

**Partner Organizations:**
- View trusted partners
- Sharing statistics
- Collaboration history
- Trust level indicators

**Sharing Groups:**
- Create custom sharing groups
- Define member organizations
- Set sharing rules
- Manage group permissions

### Data Distribution

**Distribution Levels:**
- **0 - Your organization only**: No external sharing
- **1 - This community only**: Community partners
- **2 - Connected communities**: Extended network
- **3 - All communities**: Broad sharing
- **4 - Sharing group**: Custom group only

**Sharing Controls:**
- Per-event distribution settings
- Attribute-level sharing controls
- Automatic sharing rules
- Manual approval workflows

## Taxonomies and Tagging

### Understanding Taxonomies

Taxonomies provide standardized classification for threat intelligence:

**Common Taxonomies:**
- **TLP (Traffic Light Protocol)**: Sharing guidelines
- **PAP (Permissible Actions Protocol)**: Usage permissions  
- **MISP Threat Actor**: Attribution classifications
- **Diamond Model**: Threat modeling framework
- **Kill Chain**: Attack progression stages

### Applying Tags

1. **Event Tagging:**
   - Open event for editing
   - Click "Add Tag" button
   - Browse taxonomy or search for tags
   - Select appropriate classifications
   - Save changes

2. **Attribute Tagging:**
   - Select attribute in event view
   - Click "Tag" button
   - Choose relevant tags
   - Apply to single attribute or batch

3. **Tag Examples:**
   ```
   TLP Tags:
   - tlp:white (unrestricted sharing)
   - tlp:green (community sharing)
   - tlp:amber (limited sharing)
   - tlp:red (restricted sharing)
   
   Threat Actor Tags:
   - misp-threat-actor="APT29"
   - misp-threat-actor="Lazarus Group"
   
   Technique Tags:
   - misp-technique="T1071.001" (Web Protocols)
   - misp-technique="T1055" (Process Injection)
   ```

### Custom Taxonomies

**Creating Custom Tags:**
- Define organization-specific classifications
- Create internal threat categorizations
- Build custom workflow states
- Implement business-specific labels

**Tag Management:**
- Browse all available taxonomies
- Search for specific tags
- View tag usage statistics
- Manage custom tag libraries

## Data Import and Export

### Importing Data

**Supported Formats:**
- **MISP JSON**: Native MISP format
- **STIX 1.x/2.x**: Industry standard format
- **IOC**: Mandiant IOC format
- **CSV**: Custom attribute lists
- **OpenYOC**: Yet another IOC format

**Import Process:**
1. **Select Import Method:**
   - File upload: Browse and select files
   - Direct input: Paste data directly
   - URL import: Import from external feeds
   - API import: Programmatic data ingestion

2. **Import Configuration:**
   ```
   File: threat_intelligence.json
   Format: MISP JSON
   Target Organization: ACME Corp
   Distribution: Organization only (1)
   Tag with: imported-data, external-feed
   Validate: Yes
   Preview before import: Yes
   ```

3. **Validation and Preview:**
   - System validates all data
   - Shows preview of events and attributes
   - Highlights potential issues
   - Allows corrections before import

4. **Import Execution:**
   - Process runs in background
   - Progress indicator shows status
   - Email notification on completion
   - Import summary with statistics

### Exporting Data

**Export Formats:**
- **MISP JSON**: Full fidelity export
- **STIX 2.1**: Industry standard
- **CSV**: Spreadsheet compatible
- **IOC**: Mandiant format
- **PDF**: Human-readable reports

**Export Options:**
1. **Event Export:**
   - Single event or multiple events
   - Include/exclude attributes
   - Filter by date range
   - Apply tag filters

2. **Search Export:**
   - Export search results
   - Custom field selection
   - Batch processing for large datasets
   - Scheduled exports

3. **Export Configuration:**
   ```
   Events: Selected events (5)
   Date Range: Last 30 days
   Include Attributes: Yes
   Include Correlations: No
   Format: STIX 2.1
   Encryption: PGP (optional)
   Password Protection: Yes
   ```

### Feed Management

**External Feeds:**
- Configure automatic data feeds
- Schedule regular imports
- Monitor feed health
- Manage feed credentials

**Feed Sources:**
- Commercial threat intelligence
- Open source intelligence
- Government feeds
- Industry sharing groups

## Search and Analysis

### Basic Search

**Quick Search:**
- Search box in navigation bar
- Searches events, attributes, and tags
- Auto-complete suggestions
- Recent search history

**Search Examples:**
```
malicious-domain.com        # Find specific indicator
apt29                       # Search for threat actor
"spear phishing"           # Exact phrase search
tag:banking-malware        # Search by tag
org:ACME                   # Search by organization
```

### Advanced Search

**Search Builder:**
1. Click "Advanced Search"
2. Add search criteria:
   - Field selection (event info, attribute value, etc.)
   - Operator (contains, equals, greater than, etc.)
   - Value input
   - Boolean logic (AND, OR, NOT)

3. **Example Advanced Search:**
   ```
   Event Info contains "banking"
   AND
   Threat Level equals "High"
   AND
   Tags contains "apt"
   AND
   Date created within "last 30 days"
   ```

### Search Filters

**Date Filters:**
- Created date range
- Modified date range
- Published date range
- Attribute timestamp range

**Classification Filters:**
- Threat level (1-4)
- Analysis status (0-2)
- Distribution level (0-4)
- Publication status

**Organization Filters:**
- Source organization
- Creator organization
- Sharing group membership
- Trust level

### Analysis Tools

**Correlation Analysis:**
- Find related events and attributes
- Identify campaign patterns
- Discover infrastructure overlaps
- Analyze temporal relationships

**Trend Analysis:**
- Threat volume over time
- Attribution trends
- Geographic patterns
- Technique evolution

**Statistics Dashboard:**
- Data ingestion rates
- Correlation success rates
- User activity metrics
- Sharing statistics

## User Preferences

### Account Settings

**Profile Information:**
- Name and contact details
- Organization assignment
- Role and permissions
- Language preferences

**Notification Settings:**
- Email notifications for new correlations
- Weekly summary reports
- System maintenance alerts
- Security notifications

### Executive Function Accommodations

**ADHD Support:**
- Distraction-free mode
- Enhanced focus indicators
- Reduced animation/transitions
- Simplified navigation options
- Extended session timeouts

**Autism Support:**
- Consistent interface patterns
- Detailed progress indicators
- Predictable navigation flows
- Reduced sensory overload
- Clear status messages

**Cognitive Load Reduction:**
- Progressive disclosure of features
- Context-sensitive help
- Guided workflows
- Simplified terminology
- Visual task organization

### Interface Customization

**Dashboard Layout:**
- Rearrange dashboard widgets
- Hide/show information panels
- Customize quick action buttons
- Set default views and filters

**Display Preferences:**
- Color scheme selection
- Font size adjustment
- Information density
- Icon vs. text labels
- Animation preferences

**Keyboard Shortcuts:**
- Enable/disable shortcuts
- Customize key bindings
- Quick action assignments
- Navigation shortcuts

### Workflow Preferences

**Default Settings:**
- Default distribution levels
- Standard tags to apply
- Auto-correlation preferences
- Notification thresholds

**Automation Preferences:**
- Auto-save intervals
- Background correlation
- Automatic enrichment
- Import validation levels

## Security Features

### Authentication

**Multi-Factor Authentication:**
- Time-based OTP (TOTP)
- SMS verification (if enabled)
- Hardware tokens (FIDO2/WebAuthn)
- Backup codes

**Session Management:**
- Automatic session timeout
- Concurrent session limits
- Device trust management
- Session activity monitoring

### Authorization

**Role-Based Access:**
- Read-only users
- Analysts (read/write events)
- Publishers (can publish events)
- Administrators (full access)

**Data Access Controls:**
- Organization-level isolation
- Distribution-based access
- Sharing group permissions
- Attribute-level restrictions

### Audit Logging

**Activity Tracking:**
- All user actions logged
- Data access monitoring
- Export activity tracking
- Administrative actions

**Security Monitoring:**
- Failed login attempts
- Unusual access patterns
- Data export anomalies
- Permission changes

### Data Protection

**Encryption:**
- Data encrypted at rest
- TLS encryption in transit
- API key encryption
- Backup encryption

**Privacy Controls:**
- Data anonymization options
- Personal data handling
- Retention policies
- Deletion procedures

## Troubleshooting

### Common Issues

**Login Problems:**
1. Check credentials carefully
2. Verify account is not locked
3. Check multi-factor authentication
4. Clear browser cache and cookies
5. Try incognito/private browsing mode

**Performance Issues:**
1. Check internet connection speed
2. Try refreshing the page
3. Clear browser cache
4. Disable browser extensions
5. Contact support if persistent

**Data Not Appearing:**
1. Check organization access permissions
2. Verify distribution level settings
3. Confirm event publication status
4. Check date filters in search
5. Wait for synchronization (up to 5 minutes)

**Correlation Issues:**
1. Ensure attributes are properly formatted
2. Check if correlation is still processing
3. Verify attribute types are supported
4. Consider manual correlation if needed
5. Contact support for complex cases

### Getting Help

**Built-in Help:**
- Hover tooltips on all interface elements
- Context-sensitive help panels
- Step-by-step workflow guides
- Video tutorials (if available)

**Support Channels:**
- In-app support chat
- Email support: support@your-domain.com
- Phone support: +1-XXX-XXX-XXXX
- Emergency contact for security issues

**Documentation:**
- Complete API documentation
- Administrator guides
- Integration tutorials
- Best practices guides

**Community Resources:**
- User forums
- Knowledge base
- FAQ sections
- Community-contributed content

### Keyboard Shortcuts

**Navigation:**
- `Ctrl + /`: Open search
- `Ctrl + N`: New event
- `Ctrl + E`: Edit current item
- `Ctrl + S`: Save changes
- `Esc`: Cancel operation

**Views:**
- `G → E`: Go to events list
- `G → A`: Go to attributes list
- `G → C`: Go to correlations
- `G → D`: Go to dashboard
- `F11`: Toggle distraction-free mode

**Actions:**
- `Ctrl + Enter`: Submit form
- `Ctrl + Z`: Undo last action
- `Tab`: Navigate form fields
- `Enter`: Activate buttons/links
- `?`: Show keyboard shortcuts

---

**User Manual Version**: 1.0.0  
**Last Updated**: 2025-10-31  
**For Technical Support**: support@your-domain.com  
**Emergency Security Contact**: security@your-domain.com