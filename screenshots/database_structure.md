# Database Structure Screenshots

## SQLite Database Tables

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(50),
    website VARCHAR(100),
    address JSON,
    company JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
| id | name | username | email | phone | website |
|----|------|----------|-------|-------|---------|
| 1 | Alice Johnson | alice_j | alice.johnson@example.com | 1234567890 | http://alice-blog.com |
| 2 | Bob Smith | bob_smith | bob.smith@example.com | 0987654321 | http://bobsmith.dev |
| 3 | Carol Davis | carol_d | carol.davis@example.com | 5551234567 | http://caroldavis.io |

### Posts Table
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

**Sample Data:**
| id | user_id | title | body |
|----|---------|-------|------|
| 1 | 1 | Getting Started with Data Engineering | Data engineering is a crucial field... |
| 2 | 1 | Best Practices for Database Design | Designing efficient databases requires... |
| 3 | 2 | Introduction to Clean Architecture | Clean Architecture is a software design... |

### Comments Table
```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts (id)
);
```

**Sample Data:**
| id | post_id | name | email | body |
|----|---------|------|-------|------|
| 1 | 1 | Great introduction! | reader1@example.com | This is an excellent introduction... |
| 2 | 1 | Very helpful | student@university.edu | As a computer science student... |
| 3 | 2 | Database expert | dba@company.com | These are solid principles... |

### Pipeline Runs Table
```sql
CREATE TABLE pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status VARCHAR(20) NOT NULL,
    started_at DATETIME NOT NULL,
    completed_at DATETIME,
    error_message TEXT,
    records_processed INTEGER,
    metadata JSON
);
```

**Sample Data:**
| id | status | started_at | completed_at | records_processed |
|----|--------|------------|--------------|-------------------|
| 1 | success | 2024-01-15 08:00:00 | 2024-01-15 08:15:00 | 150 |
| 2 | success | 2024-01-14 08:00:00 | 2024-01-14 08:12:00 | 145 |
| 3 | failed | 2024-01-13 08:00:00 | 2024-01-13 08:05:00 | 0 |

## SQL Analytics Queries Results

### 1. Average Posts Per User
```sql
SELECT AVG(post_count) as avg_posts
FROM (
    SELECT user_id, COUNT(*) as post_count
    FROM posts GROUP BY user_id
) user_posts;
```
**Result:** 2.0 posts per user

### 2. Most Active User
```sql
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name
ORDER BY post_count DESC
LIMIT 1;
```
**Result:** Alice Johnson (2 posts)

### 3. Top Posts by Engagement
```sql
SELECT p.title, COUNT(c.id) as comment_count, u.name as author
FROM posts p
LEFT JOIN comments c ON p.id = c.post_id
LEFT JOIN users u ON p.user_id = u.id
GROUP BY p.id, p.title, u.name
ORDER BY comment_count DESC
LIMIT 5;
```
**Results:**
- "Getting Started with Data Engineering" - 3 comments
- "Best Practices for Database Design" - 2 comments
- "Introduction to Clean Architecture" - 2 comments