# File Structure Screenshots

## Project Directory Structure

```
data-engineering-pipeline/
├── data/
│   ├── raw/
│   │   └── 2024-01-15/
│   │       ├── users.json          # Raw user data from API
│   │       ├── posts.json          # Raw posts data from API
│   │       └── comments.json       # Raw comments data from API
│   └── processed/
│       └── 2024-01-15/
│           ├── users.parquet       # Cleaned user data
│           ├── posts.parquet       # Cleaned posts data
│           └── comments.parquet    # Cleaned comments data
├── reports/
│   ├── analytics_2024-01-15_10-30-00.json    # JSON analytics report
│   ├── analytics_2024-01-15_10-30-00.csv     # CSV analytics report
│   └── analytics_2024-01-15_sample.json      # Sample report
├── src/
│   ├── domain/
│   │   ├── entities.py             # Business entities
│   │   └── interfaces.py           # Abstract interfaces
│   ├── infrastructure/
│   │   ├── api/
│   │   │   └── client.py           # HTTP API client
│   │   ├── database/
│   │   │   ├── connection.py       # Database connection
│   │   │   ├── models.py           # SQLAlchemy models
│   │   │   ├── repository.py       # Database repository
│   │   │   ├── repositories.py     # Specific repositories
│   │   │   ├── unit_of_work.py     # Unit of Work pattern
│   │   │   └── mock_data.py        # Mock data seeder
│   │   ├── storage/
│   │   │   └── file_storage.py     # File storage operations
│   │   ├── reporting/
│   │   │   └── report_generator.py # Report generation
│   │   └── orchestration/
│   │       └── prefect_flow.py     # Prefect DAG
│   ├── application/
│   │   ├── services/
│   │   │   ├── data_processor.py   # Data processing logic
│   │   │   └── dependency_injection.py # DI container
│   │   └── use_cases/
│   │       └── pipeline_orchestrator.py # Main orchestrator
│   ├── presentation/
│   │   ├── api/
│   │   │   ├── app.py              # FastAPI application
│   │   │   └── routes/             # API endpoints
│   │   └── cli/
│   │       └── commands.py         # CLI commands
│   └── config/
│       └── settings.py             # Configuration management
├── tests/
│   ├── unit/                       # Unit tests
│   ├── e2e/                        # End-to-end tests
│   └── conftest.py                 # Test fixtures
├── config/
│   ├── development.yaml            # Development config
│   └── production.yaml             # Production config
├── docker-compose.yml              # Docker services
├── Dockerfile                      # Application container
├── Makefile                        # Automation commands
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## Raw Data Files Structure

### `/data/raw/2024-01-15/users.json`
```json
[
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  }
]
```

### `/data/raw/2024-01-15/posts.json`
```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  }
]
```

## Processed Data Files Structure

### `/data/processed/2024-01-15/users.parquet`
- **Format**: Apache Parquet (columnar storage)
- **Columns**: id, name, username, email, phone, website, address, company, created_at
- **Transformations Applied**:
  - Phone numbers cleaned (removed formatting)
  - Websites normalized (added http://)
  - Email addresses lowercased
  - Added created_at timestamps
  - Geographic coordinates converted to float

### `/data/processed/2024-01-15/posts.parquet`
- **Format**: Apache Parquet
- **Columns**: id, user_id, title, body, created_at
- **Transformations Applied**:
  - userId renamed to user_id
  - Text content cleaned (whitespace normalized)
  - Added created_at timestamps

## Generated Reports

### `/reports/analytics_2024-01-15_10-30-00.json`
```json
{
  "generated_at": "2024-01-15T10:30:00.000Z",
  "total_users": 5,
  "total_posts": 10,
  "total_comments": 12,
  "average_posts_per_user": 2.0,
  "most_active_user": "Alice Johnson",
  "engagement_metrics": [...]
}
```

### `/reports/analytics_2024-01-15_10-30-00.csv`
```csv
generated_at,total_users,total_posts,total_comments,average_posts_per_user,most_active_user
2024-01-15T10:30:00.000Z,5,10,12,2.0,Alice Johnson
```

## File Sizes and Statistics

- **Raw Data**: ~15KB total (JSON format)
- **Processed Data**: ~8KB total (Parquet format, ~47% compression)
- **Reports**: ~2KB each (JSON/CSV formats)
- **Database**: ~50KB (SQLite with indexes)

## Data Flow Verification

✅ **Extract**: API → `/data/raw/yyyy-mm-dd/*.json`
✅ **Transform**: Raw JSON → `/data/processed/yyyy-mm-dd/*.parquet`
✅ **Load**: Parquet → SQLite/PostgreSQL database
✅ **Analyze**: SQL queries → Analytics results
✅ **Report**: Analytics → `/reports/*.json` and `/reports/*.csv`