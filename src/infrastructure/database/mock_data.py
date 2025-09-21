from datetime import datetime, timedelta
from typing import List
import logging

from src.domain.entities import User, Post, Comment, PipelineStatus
from .unit_of_work import UnitOfWork
from .connection import DatabaseConnection

logger = logging.getLogger(__name__)


class MockDataSeeder:
    """
    Seeder class for populating the database with mock data.
    
    This provides sample data for frontend development and testing
    without requiring the full pipeline to run.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
    
    def seed_all(self) -> None:
        """Seed all mock data"""
        logger.info("Starting mock data seeding...")
        
        try:
            with UnitOfWork(self.db_connection) as uow:
                # Check if data already exists
                existing_users = uow.users.get_all()
                if existing_users:
                    logger.info("Mock data already exists, skipping seeding")
                    return
                
                # Seed users first
                users = self._create_mock_users()
                for user in users:
                    uow.users.add(user)
                
                # Seed posts
                posts = self._create_mock_posts()
                for post in posts:
                    uow.posts.add(post)
                
                # Seed comments
                comments = self._create_mock_comments()
                for comment in comments:
                    uow.comments.add(comment)
                
                # Seed pipeline runs
                pipeline_runs = self._create_mock_pipeline_runs()
                for run in pipeline_runs:
                    uow.pipeline_runs.add(run)
                
                uow.commit()
                logger.info("Mock data seeding completed successfully")
                
        except Exception as e:
            logger.error(f"Error seeding mock data: {e}")
            raise
    
    def _create_mock_users(self) -> List[User]:
        """Create mock users"""
        return [
            User(
                id=1,
                name="Alice Johnson",
                username="alice_j",
                email="alice.johnson@example.com",
                phone="1234567890",
                website="http://alice-blog.com",
                address={
                    "street": "123 Main St",
                    "suite": "Apt 4B",
                    "city": "New York",
                    "zipcode": "10001",
                    "geo": {"lat": 40.7128, "lng": -74.0060}
                },
                company={
                    "name": "Tech Innovations Inc",
                    "catchPhrase": "Innovation at its finest",
                    "bs": "cutting-edge solutions"
                },
                created_at=datetime.utcnow() - timedelta(days=30)
            ),
            User(
                id=2,
                name="Bob Smith",
                username="bob_smith",
                email="bob.smith@example.com",
                phone="0987654321",
                website="http://bobsmith.dev",
                address={
                    "street": "456 Oak Ave",
                    "suite": "Suite 200",
                    "city": "San Francisco",
                    "zipcode": "94102",
                    "geo": {"lat": 37.7749, "lng": -122.4194}
                },
                company={
                    "name": "Digital Solutions LLC",
                    "catchPhrase": "Digital transformation made easy",
                    "bs": "scalable digital platforms"
                },
                created_at=datetime.utcnow() - timedelta(days=25)
            ),
            User(
                id=3,
                name="Carol Davis",
                username="carol_d",
                email="carol.davis@example.com",
                phone="5551234567",
                website="http://caroldavis.io",
                address={
                    "street": "789 Pine St",
                    "suite": "",
                    "city": "Seattle",
                    "zipcode": "98101",
                    "geo": {"lat": 47.6062, "lng": -122.3321}
                },
                company={
                    "name": "Creative Minds Studio",
                    "catchPhrase": "Where creativity meets technology",
                    "bs": "innovative creative solutions"
                },
                created_at=datetime.utcnow() - timedelta(days=20)
            ),
            User(
                id=4,
                name="David Wilson",
                username="david_w",
                email="david.wilson@example.com",
                phone="7778889999",
                website="http://davidwilson.net",
                address={
                    "street": "321 Elm St",
                    "suite": "Floor 3",
                    "city": "Austin",
                    "zipcode": "73301",
                    "geo": {"lat": 30.2672, "lng": -97.7431}
                },
                company={
                    "name": "Data Analytics Pro",
                    "catchPhrase": "Turning data into insights",
                    "bs": "advanced analytics solutions"
                },
                created_at=datetime.utcnow() - timedelta(days=15)
            ),
            User(
                id=5,
                name="Eva Martinez",
                username="eva_m",
                email="eva.martinez@example.com",
                phone="3334445555",
                website="http://evamartinez.com",
                address={
                    "street": "654 Maple Dr",
                    "suite": "Unit 12",
                    "city": "Miami",
                    "zipcode": "33101",
                    "geo": {"lat": 25.7617, "lng": -80.1918}
                },
                company={
                    "name": "Global Consulting Group",
                    "catchPhrase": "Global solutions, local expertise",
                    "bs": "strategic business consulting"
                },
                created_at=datetime.utcnow() - timedelta(days=10)
            )
        ]
    
    def _create_mock_posts(self) -> List[Post]:
        """Create mock posts"""
        return [
            Post(
                id=1,
                user_id=1,
                title="Getting Started with Data Engineering",
                body="Data engineering is a crucial field that focuses on the design and construction of systems for collecting, storing, and analyzing data at scale. In this post, we'll explore the fundamentals of building robust data pipelines.",
                created_at=datetime.utcnow() - timedelta(days=5)
            ),
            Post(
                id=2,
                user_id=1,
                title="Best Practices for Database Design",
                body="Designing efficient databases requires careful consideration of normalization, indexing, and query optimization. Here are some key principles to follow when designing your database schema.",
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
            Post(
                id=3,
                user_id=2,
                title="Introduction to Clean Architecture",
                body="Clean Architecture is a software design philosophy that emphasizes separation of concerns and dependency inversion. This approach leads to more maintainable and testable code.",
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            Post(
                id=4,
                user_id=2,
                title="Implementing SOLID Principles in Python",
                body="The SOLID principles are fundamental guidelines for object-oriented programming. Let's explore how to apply these principles effectively in Python applications.",
                created_at=datetime.utcnow() - timedelta(days=2)
            ),
            Post(
                id=5,
                user_id=3,
                title="Modern Frontend Development with React",
                body="React has revolutionized frontend development with its component-based architecture. This post covers the latest features and best practices for React development.",
                created_at=datetime.utcnow() - timedelta(days=6)
            ),
            Post(
                id=6,
                user_id=3,
                title="State Management in Large Applications",
                body="Managing state in large applications can be challenging. We'll explore different approaches including Redux, Context API, and modern state management solutions.",
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
            Post(
                id=7,
                user_id=4,
                title="Data Visualization with Python",
                body="Effective data visualization is key to understanding complex datasets. This post demonstrates various Python libraries for creating compelling visualizations.",
                created_at=datetime.utcnow() - timedelta(days=4)
            ),
            Post(
                id=8,
                user_id=4,
                title="Machine Learning Pipeline Automation",
                body="Automating machine learning pipelines improves efficiency and reproducibility. Learn how to build robust ML pipelines using modern tools and frameworks.",
                created_at=datetime.utcnow() - timedelta(days=8)
            ),
            Post(
                id=9,
                user_id=5,
                title="Microservices Architecture Patterns",
                body="Microservices architecture offers scalability and flexibility but comes with its own challenges. This post explores common patterns and anti-patterns.",
                created_at=datetime.utcnow() - timedelta(days=9)
            ),
            Post(
                id=10,
                user_id=5,
                title="DevOps Best Practices for Modern Applications",
                body="DevOps practices are essential for delivering reliable software at scale. We'll cover CI/CD, infrastructure as code, and monitoring strategies.",
                created_at=datetime.utcnow() - timedelta(days=12)
            )
        ]
    
    def _create_mock_comments(self) -> List[Comment]:
        """Create mock comments"""
        return [
            Comment(
                id=1,
                post_id=1,
                name="Great introduction!",
                email="reader1@example.com",
                body="This is an excellent introduction to data engineering. Looking forward to more posts on this topic!",
                created_at=datetime.utcnow() - timedelta(days=4)
            ),
            Comment(
                id=2,
                post_id=1,
                name="Very helpful",
                email="student@university.edu",
                body="As a computer science student, this post really helped me understand the basics of data engineering.",
                created_at=datetime.utcnow() - timedelta(days=4)
            ),
            Comment(
                id=3,
                post_id=2,
                name="Database expert",
                email="dba@company.com",
                body="These are solid principles for database design. I'd also recommend considering partitioning for large tables.",
                created_at=datetime.utcnow() - timedelta(days=2)
            ),
            Comment(
                id=4,
                post_id=3,
                name="Architecture enthusiast",
                email="architect@tech.com",
                body="Clean Architecture has transformed how I approach software design. The dependency inversion principle is particularly powerful.",
                created_at=datetime.utcnow() - timedelta(days=6)
            ),
            Comment(
                id=5,
                post_id=3,
                name="Question about implementation",
                email="developer@startup.io",
                body="How do you handle the complexity that comes with implementing clean architecture in smaller projects?",
                created_at=datetime.utcnow() - timedelta(days=6)
            ),
            Comment(
                id=6,
                post_id=4,
                name="Python developer",
                email="pythonista@code.com",
                body="SOLID principles are game-changers for Python development. The examples you provided are very clear.",
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
            Comment(
                id=7,
                post_id=5,
                name="React fan",
                email="frontend@web.dev",
                body="React's component model is indeed revolutionary. Have you tried the new concurrent features?",
                created_at=datetime.utcnow() - timedelta(days=5)
            ),
            Comment(
                id=8,
                post_id=6,
                name="State management question",
                email="junior@company.com",
                body="Which state management solution would you recommend for a medium-sized e-commerce application?",
                created_at=datetime.utcnow() - timedelta(hours=12)
            ),
            Comment(
                id=9,
                post_id=7,
                name="Data scientist",
                email="datascientist@research.org",
                body="Excellent overview of visualization libraries. Plotly and Seaborn are my go-to choices for most projects.",
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
            Comment(
                id=10,
                post_id=8,
                name="ML engineer",
                email="mlengineer@ai.com",
                body="Pipeline automation is crucial for production ML systems. MLflow and Kubeflow are great tools for this.",
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            Comment(
                id=11,
                post_id=9,
                name="Microservices practitioner",
                email="architect@enterprise.com",
                body="The circuit breaker pattern has saved us from many cascading failures in our microservices architecture.",
                created_at=datetime.utcnow() - timedelta(days=8)
            ),
            Comment(
                id=12,
                post_id=10,
                name="DevOps engineer",
                email="devops@cloud.com",
                body="Infrastructure as code is a must-have for any serious DevOps practice. Terraform and Ansible are excellent choices.",
                created_at=datetime.utcnow() - timedelta(days=11)
            )
        ]
    
    def _create_mock_pipeline_runs(self) -> List:
        """Create mock pipeline runs"""
        from src.domain.entities import PipelineRun
        
        return [
            PipelineRun(
                id=1,
                status=PipelineStatus.SUCCESS,
                started_at=datetime.utcnow() - timedelta(hours=2),
                completed_at=datetime.utcnow() - timedelta(hours=1, minutes=45),
                error_message=None,
                records_processed=150,
                metadata={
                    "users_processed": 5,
                    "posts_processed": 10,
                    "comments_processed": 12
                }
            ),
            PipelineRun(
                id=2,
                status=PipelineStatus.SUCCESS,
                started_at=datetime.utcnow() - timedelta(days=1),
                completed_at=datetime.utcnow() - timedelta(days=1) + timedelta(minutes=30),
                error_message=None,
                records_processed=145,
                metadata={
                    "users_processed": 5,
                    "posts_processed": 10,
                    "comments_processed": 12
                }
            ),
            PipelineRun(
                id=3,
                status=PipelineStatus.FAILED,
                started_at=datetime.utcnow() - timedelta(days=2),
                completed_at=datetime.utcnow() - timedelta(days=2) + timedelta(minutes=5),
                error_message="API rate limit exceeded",
                records_processed=0,
                metadata={}
            )
        ]


def seed_mock_data(db_connection: DatabaseConnection) -> None:
    """Convenience function to seed mock data"""
    seeder = MockDataSeeder(db_connection)
    seeder.seed_all()