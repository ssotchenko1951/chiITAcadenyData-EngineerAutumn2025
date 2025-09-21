# Data Pipeline API Documentation

## Overview

This document provides comprehensive API documentation for the Data Engineering Pipeline. The API follows OpenAPI 3.0 specification and provides endpoints for pipeline management, analytics, and reporting.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication

Currently, the API does not require authentication. In production, consider implementing:
- JWT tokens
- API keys
- OAuth2

## OpenAPI Specification

### Swagger UI

Access the interactive API documentation at:
- Development: `http://localhost:8000/docs`
- ReDoc format: `http://localhost:8000/redoc`

## Endpoints

### Health Check

#### GET /health/

Check the health status of the API service.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "data-pipeline-api"
}
```

**Status Codes:**
- `200`: Service is healthy

---

### Pipeline Management

#### POST /pipeline/run

Trigger a new pipeline execution. The pipeline will run asynchronously in the background.

**Response:**
```json
{
  "message": "Pipeline execution started",
  "task_id": "pipeline_1705315200"
}
```

**Status Codes:**
- `200`: Pipeline started successfully
- `500`: Internal server error

#### GET /pipeline/status/{task_id}

Get the status of a specific pipeline execution.

**Parameters:**
- `task_id` (path): Task identifier returned from the run endpoint

**Response:**
```json
{
  "status": "completed",
  "result": {
    "pipeline_run": {
      "id": 1,
      "status": "success",
      "started_at": "2024-01-15T10:00:00.000Z",
      "completed_at": "2024-01-15T10:30:00.000Z",
      "records_processed": 150
    }
  }
}
```

**Status Codes:**
- `200`: Status retrieved successfully
- `404`: Task not found

#### GET /pipeline/runs

Get a list of recent pipeline runs.

**Parameters:**
- `limit` (query): Maximum number of runs to return (default: 10)

**Response:**
```json
{
  "runs": [
    {
      "id": 1,
      "status": "success",
      "started_at": "2024-01-15T10:00:00.000Z",
      "completed_at": "2024-01-15T10:30:00.000Z",
      "records_processed": 150,
      "error_message": null
    }
  ]
}
```

**Status Codes:**
- `200`: Runs retrieved successfully

---

### Analytics

#### GET /analytics/summary

Get comprehensive analytics summary including all metrics.

**Response:**
```json
{
  "total_users": 10,
  "total_posts": 100,
  "total_comments": 500,
  "average_posts_per_user": 10.0,
  "most_active_user": "John Doe",
  "top_posts_by_engagement": [
    {
      "title": "Popular Post Title",
      "comment_count": 25,
      "author": "Jane Smith"
    }
  ]
}
```

**Status Codes:**
- `200`: Analytics retrieved successfully
- `500`: Database error

#### GET /analytics/users/stats

Get user-specific statistics.

**Response:**
```json
{
  "total_users": 10,
  "average_posts_per_user": 10.0,
  "most_active_user": "John Doe"
}
```

**Status Codes:**
- `200`: User statistics retrieved successfully

#### GET /analytics/engagement

Get engagement metrics for posts and comments.

**Response:**
```json
{
  "total_posts": 100,
  "total_comments": 500,
  "top_posts": [
    {
      "title": "Most Engaging Post",
      "comment_count": 25,
      "author": "Author Name"
    }
  ]
}
```

**Status Codes:**
- `200`: Engagement metrics retrieved successfully

---

### Reports

#### GET /reports/

List all available reports with metadata.

**Response:**
```json
{
  "reports": [
    {
      "filename": "analytics_2024-01-15_10-30-00.json",
      "size": 2048,
      "created": 1705315800.0,
      "format": "json"
    },
    {
      "filename": "analytics_2024-01-15_10-30-00.csv",
      "size": 1024,
      "created": 1705315800.0,
      "format": "csv"
    }
  ]
}
```

**Status Codes:**
- `200`: Reports listed successfully

#### GET /reports/{filename}

Download a specific report file.

**Parameters:**
- `filename` (path): Name of the report file to download

**Response:**
- Binary file content with appropriate content-type headers

**Status Codes:**
- `200`: File downloaded successfully
- `404`: File not found

#### DELETE /reports/{filename}

Delete a specific report file.

**Parameters:**
- `filename` (path): Name of the report file to delete

**Response:**
```json
{
  "message": "Report analytics_2024-01-15.json deleted successfully"
}
```

**Status Codes:**
- `200`: File deleted successfully
- `404`: File not found
- `500`: File deletion failed

---

## Data Models

### Pipeline Run

```json
{
  "id": 1,
  "status": "success|running|failed|pending",
  "started_at": "2024-01-15T10:00:00.000Z",
  "completed_at": "2024-01-15T10:30:00.000Z",
  "error_message": "Error description if failed",
  "records_processed": 150,
  "metadata": {
    "users_processed": 10,
    "posts_processed": 100,
    "comments_processed": 500
  }
}
```

### Analytics Summary

```json
{
  "total_users": 10,
  "total_posts": 100,
  "total_comments": 500,
  "average_posts_per_user": 10.0,
  "most_active_user": "Username",
  "top_posts_by_engagement": [
    {
      "title": "Post title",
      "comment_count": 25,
      "author": "Author name"
    }
  ]
}
```

### Report Metadata

```json
{
  "filename": "report_name.json",
  "size": 2048,
  "created": 1705315800.0,
  "format": "json|csv"
}
```

---

## Error Handling

The API uses standard HTTP status codes and returns error responses in JSON format:

```json
{
  "detail": "Error description",
  "type": "error_type",
  "code": "ERROR_CODE"
}
```

### Common Error Codes

- `400`: Bad Request - Invalid input parameters
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Server-side error
- `503`: Service Unavailable - Service temporarily unavailable

---

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting in production:

- Per-IP limits
- Per-user limits (if authentication is added)
- Different limits for different endpoints

---

## Webhooks (Future Enhancement)

Consider implementing webhooks for:
- Pipeline completion notifications
- Error notifications
- Report generation notifications

---

## SDK Examples

### Python

```python
import httpx

class PipelineClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url)
    
    def run_pipeline(self):
        response = self.client.post("/pipeline/run")
        return response.json()
    
    def get_analytics(self):
        response = self.client.get("/analytics/summary")
        return response.json()
    
    def list_reports(self):
        response = self.client.get("/reports/")
        return response.json()

# Usage
client = PipelineClient()
result = client.run_pipeline()
print(f"Pipeline started with task_id: {result['task_id']}")
```

### JavaScript

```javascript
class PipelineClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async runPipeline() {
        const response = await fetch(`${this.baseUrl}/pipeline/run`, {
            method: 'POST',
        });
        return await response.json();
    }
    
    async getAnalytics() {
        const response = await fetch(`${this.baseUrl}/analytics/summary`);
        return await response.json();
    }
    
    async listReports() {
        const response = await fetch(`${this.baseUrl}/reports/`);
        return await response.json();
    }
}

// Usage
const client = new PipelineClient();
const result = await client.runPipeline();
console.log(`Pipeline started with task_id: ${result.task_id}`);
```

---

## OpenAPI 3.0 Specification

The complete OpenAPI specification is available at `/openapi.json` when the server is running.

## Testing the API

### Using cURL

```bash
# Health check
curl -X GET "http://localhost:8000/health/"

# Run pipeline
curl -X POST "http://localhost:8000/pipeline/run"

# Get analytics
curl -X GET "http://localhost:8000/analytics/summary"

# List reports
curl -X GET "http://localhost:8000/reports/"
```

### Using HTTPie

```bash
# Health check
http GET localhost:8000/health/

# Run pipeline
http POST localhost:8000/pipeline/run

# Get analytics
http GET localhost:8000/analytics/summary

# List reports
http GET localhost:8000/reports/
```

This API documentation provides a comprehensive guide for integrating with the Data Engineering Pipeline API.