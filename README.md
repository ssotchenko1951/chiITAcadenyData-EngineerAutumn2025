# Data Engineering Pipeline

## Project Overview

This project implements a comprehensive data engineering pipeline that extracts data from a public REST API, processes it, stores it in a database, and generates analytics reports. The implementation follows clean architecture principles, SOLID design patterns, and includes comprehensive testing and documentation.

## Architecture

The project follows Clean Architecture principles with clear separation of concerns:

```
src/
├── domain/           # Business logic and entities
├── infrastructure/   # External concerns (DB, API, File I/O)
├── application/      # Use cases and orchestration
├── presentation/     # API endpoints and CLI
└── config/          # Configuration management
```

## Unit of Work Pattern Implementation

### Overview

The Unit of Work pattern is implemented to manage database transactions and ensure data consistency across multiple repository operations. This pattern provides several key benefits when working with SQLite and other databases.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Unit of Work Pattern                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │   Application   │    │           Unit of Work              │ │
│  │     Layer       │───▶│                                     │ │
│  │                 │    │  ┌─────────────────────────────────┐ │ │
│  └─────────────────┘    │  │        Transaction              │ │ │
│                         │  │                                 │ │ │
│                         │  │  ┌─────────┐  ┌─────────────┐   │ │ │
│                         │  │  │  User   │  │    Post     │   │ │ │
│                         │  │  │Repository│  │ Repository  │   │ │ │
│                         │  │  └─────────┘  └─────────────┘   │ │ │
│                         │  │                                 │ │ │
│                         │  │  ┌─────────┐  ┌─────────────┐   │ │ │
│                         │  │  │Comment  │  │ PipelineRun │   │ │ │
│                         │  │  │Repository│  │ Repository  │   │ │ │
│                         │  │  └─────────┘  └─────────────┘   │ │ │
│                         │  └─────────────────────────────────┘ │ │
│                         └─────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                      Database Session                          │
│                    (SQLite/PostgreSQL)                         │
└─────────────────────────────────────────────────────────────────┘
```

### Benefits for SQLite Database Operations

#### 1. **Transaction Management**
- **Atomic Operations**: All repository operations within a Unit of Work are committed or rolled back together
- **ACID Compliance**: Ensures Atomicity, Consistency, Isolation, and Durability
- **Automatic Rollback**: If any operation fails, all changes are automatically rolled back

#### 2. **Performance Optimization**
- **Single Connection**: Reuses the same database connection across multiple operations
- **Reduced Overhead**: Minimizes connection establishment and teardown costs
- **Batch Operations**: Groups multiple database operations into a single transaction

#### 3. **Data Consistency**
- **Cross-Table Integrity**: Ensures related data across multiple tables remains consistent
- **Foreign Key Constraints**: Properly handles relationships between entities
- **Concurrent Access**: Manages concurrent access to SQLite database safely

#### 4. **Error Handling**
- **Graceful Degradation**: Handles database errors gracefully with automatic rollback
- **Exception Safety**: Ensures database remains in a consistent state even when exceptions occur
- **Resource Cleanup**: Automatically closes database connections and cleans up resources

### Usage Examples

#### Basic Usage
```python
from src.infrastructure.database.unit_of_work import UnitOfWork
from src.application.services.dependency_injection import get_database_connection

# Using context manager (recommended)
with UnitOfWork(get_database_connection()) as uow:
    # Add a user
    user = uow.users.add(new_user)
    
    # Add posts for the user
    for post_data in posts:
        post = Post(user_id=user.id, **post_data)
        uow.posts.add(post)
    
    # All operations are committed together
    # If any operation fails, all are rolled back
```

#### Complex Transaction Example
```python
def create_user_with_content(user_data, posts_data, comments_data):
    """Create user with posts and comments in a single transaction"""
    with UnitOfWork(get_database_connection()) as uow:
        # Create user
        user = User(**user_data)
        created_user = uow.users.add(user)
        
        # Create posts
        created_posts = []
        for post_data in posts_data:
            post = Post(user_id=created_user.id, **post_data)
            created_post = uow.posts.add(post)
            created_posts.append(created_post)
        
        # Create comments
        for comment_data in comments_data:
            comment = Comment(
                post_id=created_posts[0].id,
                **comment_data
            )
            uow.comments.add(comment)
        
        # All operations succeed or fail together
        return created_user
```

#### Error Handling
```python
try:
    with UnitOfWork(get_database_connection()) as uow:
        # Perform multiple operations
        uow.users.add(user)
        uow.posts.add(post)
        
        # If this fails, all previous operations are rolled back
        uow.comments.add(invalid_comment)
        
except Exception as e:
    # Database is in consistent state
    # All operations have been rolled back
    logger.error(f"Transaction failed: {e}")
```

### Repository Pattern Integration

The Unit of Work pattern works seamlessly with the Repository pattern:

- **UserRepository**: Manages user-related database operations
- **PostRepository**: Handles blog post operations
- **CommentRepository**: Manages comment operations
- **PipelineRunRepository**: Tracks pipeline execution history

Each repository provides:
- **CRUD Operations**: Create, Read, Update, Delete
- **Specialized Queries**: Domain-specific query methods
- **Entity Mapping**: Automatic conversion between domain entities and database models

### Mock Data Integration

The system automatically seeds mock data for frontend development:

```python
# Mock data is automatically loaded on application startup
# Includes:
# - 5 sample users with realistic profiles
# - 10 blog posts with engaging content
# - 12 comments with meaningful interactions
# - 3 pipeline run records with different statuses
```

### Frontend API Endpoints

New endpoints provide mock data for frontend development:

- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get specific user
- `GET /api/posts` - Get all posts
- `GET /api/posts/{id}` - Get specific post
- `GET /api/posts/{id}/comments` - Get post comments
- `GET /api/users/{id}/posts` - Get user's posts
- `GET /api/dashboard/stats` - Get dashboard statistics

### Testing Strategy

The Unit of Work pattern is thoroughly tested:

- **Unit Tests**: Test individual repository operations
- **Integration Tests**: Test cross-repository transactions
- **Error Handling Tests**: Verify rollback behavior
- **Performance Tests**: Measure transaction overhead

This implementation provides a robust foundation for database operations while maintaining clean architecture principles and ensuring data consistency across all operations.

## Features

- ✅ **Data Extraction**: Fetch data from JSONPlaceholder API
- ✅ **Data Storage**: Raw data saved in S3-like structure
- ✅ **Data Processing**: Clean, transform, and enrich data
- ✅ **Multi-Database Support**: SQLite and PostgreSQL
- ✅ **Analytics**: SQL-based data analysis
- ✅ **Report Generation**: CSV and JSON reports
- ✅ **Docker Support**: Complete containerization
- ✅ **API Documentation**: Swagger/OpenAPI
- ✅ **Automation**: Makefile and scripts
- ✅ **Testing**: Unit and E2E tests
- ✅ **Workflow Orchestration**: Prefect DAG

## Tech Stack

- **Python 3.11+**
- **FastAPI** for REST API
- **SQLAlchemy** for database ORM
- **Pandas** for data processing
- **PyArrow** for Parquet files
- **Prefect** for workflow orchestration
- **Docker & Docker Compose**
- **PostgreSQL & SQLite**
- **Pytest** for testing

## Quick Start

### Using Docker (Recommended)

```bash
# Start the entire stack
make docker-up

# Run the pipeline
make run-pipeline

# View API documentation
# Visit http://localhost:8000/docs
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run database migrations
make migrate

# Start the pipeline
make run-pipeline

# Start API server
make start-api
```

## API Endpoints

- `GET /health` - Health check
- `POST /pipeline/run` - Trigger pipeline execution
- `GET /pipeline/status` - Get pipeline status
- `GET /analytics/summary` - Get analytics summary
- `GET /reports/` - List available reports
- `GET /reports/{report_id}` - Download specific report

## Configuration

The application supports multiple environments through configuration files:

```yaml
# config/development.yaml
database:
  type: "sqlite"
  url: "sqlite:///data/pipeline.db"

# config/production.yaml
database:
  type: "postgresql"
  host: "localhost"
  port: 5432
  database: "pipeline_db"
```

## Pipeline Workflow

1. **Extract**: Fetch data from JSONPlaceholder API
2. **Transform**: Clean and enrich the data
3. **Load**: Store in database (SQLite/PostgreSQL)
4. **Analyze**: Run SQL analytics queries
5. **Report**: Generate CSV/JSON reports

## Data Flow

```
API → Raw Data (JSON) → Processed Data (Parquet) → Database → Analytics → Reports
```

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run E2E tests
make test-e2e
```

## Database Schema

The pipeline creates tables for:
- `users` - User information
- `posts` - User posts
- `comments` - Post comments
- `pipeline_runs` - Execution logs

## Implementation Details

### 1. Data Source
- **API**: JSONPlaceholder (https://jsonplaceholder.typicode.com)
- **Endpoints**: /users, /posts, /comments
- **Data Format**: JSON

### 2. Data Processing
- **Cleaning**: Remove null values, validate data types
- **Enrichment**: Add calculated fields (post_count, comment_density)
- **Transformation**: Normalize nested JSON structures

### 3. Database Support
- **SQLite**: For development and testing
- **PostgreSQL**: For production deployment
- **Migrations**: Automated schema management

### 4. Analytics Queries
- Average posts per user
- Most active users by comment count
- Post engagement metrics
- User activity distribution

## Screenshots

### Database Tables
![Database Screenshot](screenshots/database.png)

### Local File Structure
![Files Screenshot](screenshots/files.png)

### API Documentation
![API Screenshot](screenshots/api.png)

## Reports

Sample analytics reports are generated in:
- `reports/analytics_YYYY-MM-DD.json`
- `reports/analytics_YYYY-MM-DD.csv`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the coding standards
4. Add tests for new features
5. Submit a pull request

## License

MIT License