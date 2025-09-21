from typing import Dict, Any, List
from datetime import datetime
import logging

from src.domain.entities import PipelineRun, PipelineStatus, AnalyticsReport
from src.domain.interfaces import (
    DataExtractorInterface, 
    DataProcessorInterface, 
    FileStorageInterface, 
    DatabaseInterface, 
    ReportGeneratorInterface
)

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Main orchestrator for the data pipeline"""
    
    def __init__(
        self,
        api_client: DataExtractorInterface,
        data_processor: DataProcessorInterface,
        file_storage: FileStorageInterface,
        database: DatabaseInterface,
        report_generator: ReportGeneratorInterface
    ):
        self.api_client = api_client
        self.data_processor = data_processor
        self.file_storage = file_storage
        self.database = database
        self.report_generator = report_generator
    
    async def run_full_pipeline(self) -> Dict[str, Any]:
        """Run the complete data pipeline"""
        pipeline_run = PipelineRun(
            id=None,
            status=PipelineStatus.RUNNING,
            started_at=datetime.utcnow(),
            completed_at=None,
            error_message=None,
            records_processed=None
        )
        
        # Save initial pipeline run
        pipeline_run = self.database.save_pipeline_run(pipeline_run)
        
        try:
            logger.info(f"Starting pipeline run {pipeline_run.id}")
            
            # Step 1: Extract data
            raw_data = await self.extract_data()
            
            # Step 2: Process data
            processed_data = self.process_data(raw_data)
            
            # Step 3: Store data
            self.store_data(processed_data)
            
            # Step 4: Generate analytics
            analytics_report = self.generate_analytics()
            
            # Update pipeline run status
            total_records = (
                len(processed_data["users"]) + 
                len(processed_data["posts"]) + 
                len(processed_data["comments"])
            )
            
            pipeline_run.status = PipelineStatus.SUCCESS
            pipeline_run.completed_at = datetime.utcnow()
            pipeline_run.records_processed = total_records
            pipeline_run.metadata = {
                "users_processed": len(processed_data["users"]),
                "posts_processed": len(processed_data["posts"]),
                "comments_processed": len(processed_data["comments"])
            }
            
            self.database.save_pipeline_run(pipeline_run)
            
            logger.info(f"Pipeline run {pipeline_run.id} completed successfully")
            
            return {
                "pipeline_run": pipeline_run,
                "analytics_report": analytics_report
            }
            
        except Exception as e:
            logger.error(f"Pipeline run {pipeline_run.id} failed: {e}")
            
            pipeline_run.status = PipelineStatus.FAILED
            pipeline_run.completed_at = datetime.utcnow()
            pipeline_run.error_message = str(e)
            
            self.database.save_pipeline_run(pipeline_run)
            
            raise
    
    async def extract_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract data from API sources"""
        logger.info("Starting data extraction")
        
        # Extract all data concurrently
        raw_data = await self.api_client.extract_all_data()
        
        # Save raw data to files
        current_time = datetime.utcnow()
        for data_type, data_list in raw_data.items():
            self.file_storage.save_raw_data(
                data=data_list,
                filename=data_type,
                date_partition=current_time
            )
        
        logger.info(f"Extracted {sum(len(data) for data in raw_data.values())} total records")
        return raw_data
    
    def process_data(self, raw_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Process and transform raw data"""
        logger.info("Starting data processing")
        
        processed_data = {}
        current_time = datetime.utcnow()
        
        # Process users
        if "users" in raw_data:
            processed_users = self.data_processor.process_users(raw_data["users"])
            processed_data["users"] = processed_users
            
            # Save processed users
            users_dict = [
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "website": user.website,
                    "address": user.address,
                    "company": user.company,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
                for user in processed_users
            ]
            self.file_storage.save_processed_data(
                data=users_dict,
                filename="users",
                date_partition=current_time
            )
        
        # Process posts
        if "posts" in raw_data:
            processed_posts = self.data_processor.process_posts(raw_data["posts"])
            processed_data["posts"] = processed_posts
            
            posts_dict = [
                {
                    "id": post.id,
                    "user_id": post.user_id,
                    "title": post.title,
                    "body": post.body,
                    "created_at": post.created_at.isoformat() if post.created_at else None
                }
                for post in processed_posts
            ]
            self.file_storage.save_processed_data(
                data=posts_dict,
                filename="posts",
                date_partition=current_time
            )
        
        # Process comments
        if "comments" in raw_data:
            processed_comments = self.data_processor.process_comments(raw_data["comments"])
            processed_data["comments"] = processed_comments
            
            comments_dict = [
                {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "name": comment.name,
                    "email": comment.email,
                    "body": comment.body,
                    "created_at": comment.created_at.isoformat() if comment.created_at else None
                }
                for comment in processed_comments
            ]
            self.file_storage.save_processed_data(
                data=comments_dict,
                filename="comments",
                date_partition=current_time
            )
        
        logger.info("Data processing completed")
        return processed_data
    
    def store_data(self, processed_data: Dict[str, Any]) -> None:
        """Store processed data in database"""
        logger.info("Starting data storage")
        
        # Store users
        if "users" in processed_data:
            self.database.save_users(processed_data["users"])
        
        # Store posts
        if "posts" in processed_data:
            self.database.save_posts(processed_data["posts"])
        
        # Store comments
        if "comments" in processed_data:
            self.database.save_comments(processed_data["comments"])
        
        logger.info("Data storage completed")
    
    def generate_analytics(self) -> AnalyticsReport:
        """Generate analytics report"""
        logger.info("Generating analytics report")
        
        # Get analytics data from database
        analytics_data = self.database.get_analytics_data()
        
        # Generate report
        report = self.report_generator.generate_analytics_report(analytics_data)
        
        # Export reports
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        json_filename = f"analytics_{timestamp}"
        csv_filename = f"analytics_{timestamp}"
        
        json_filepath = self.file_storage.save_report(
            data=analytics_data, 
            filename=json_filename, 
            format="json"
        )
        
        csv_filepath = self.file_storage.save_report(
            data=analytics_data,
            filename=csv_filename,
            format="csv"
        )
        
        logger.info(f"Analytics report generated: {json_filepath}, {csv_filepath}")
        return report