# Overview

This is a Streamlit-based web application with a view counter feature. The application uses PostgreSQL to track and persist view counts for assessments or similar content. The project appears to be in early development stages, with the core functionality focused on displaying content while tracking engagement metrics through a database-backed counter system.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture

**Framework:** Streamlit  
**Rationale:** Streamlit provides a rapid development framework for creating data-driven web applications with minimal boilerplate code. It's ideal for quick prototyping and deploying interactive dashboards or content displays.

**Key Components:**
- Main application logic in `app.py` handles UI rendering and user interactions
- Built-in session state management through Streamlit for maintaining application state

## Backend Architecture

**Pattern:** Monolithic application structure  
**Rationale:** The application combines frontend and backend logic in a single codebase, which is appropriate for small to medium-sized applications where Streamlit's architecture provides sufficient separation of concerns.

**Data Layer:**
- Direct database connections using psycopg2
- Simple function-based data access patterns
- Counter initialization and increment operations handled through SQL queries

**Design Decisions:**
- Error handling uses try-except blocks that silently fail (returns default values)
- Connection pooling is not implemented; each operation creates a new connection
- Database schema is auto-initialized on application startup

## Data Storage

**Database:** PostgreSQL  
**Rationale:** PostgreSQL provides ACID compliance and reliability for persisting counter data, ensuring accurate view counts even under concurrent access.

**Schema Design:**
- `view_counter` table with serial primary key
- Unique constraint on `counter_name` to prevent duplicates
- Simple integer counter with default value of 0
- Uses `ON CONFLICT DO NOTHING` for idempotent initialization

**Alternatives Considered:**
- In-memory storage: Would lose data on application restart
- File-based storage: Less reliable for concurrent access

**Pros:**
- Reliable data persistence
- Support for concurrent updates
- Scalable for future feature additions

**Cons:**
- Requires external database service
- Additional infrastructure complexity for simple counter functionality

# External Dependencies

## Database Services
- **PostgreSQL**: Primary data store accessed via `DATABASE_URL` environment variable
- Connection string expected to be provided through environment configuration

## Python Libraries
- **streamlit**: Web application framework for UI and server functionality
- **psycopg2**: PostgreSQL adapter for Python, handles all database operations
- **os**: Standard library for environment variable access

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string (required for database operations)