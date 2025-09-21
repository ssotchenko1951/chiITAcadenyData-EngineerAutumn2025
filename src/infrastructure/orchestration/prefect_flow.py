from prefect import flow, task
from datetime import datetime, timedelta
import asyncio
import logging

from src.application.use_cases.pipeline_orchestrator import PipelineOrchestrator
from src.application.services.dependency_injection import get_pipeline_orchestrator

logger = logging.getLogger(__name__)


@task
def extract_data_task():
    """Task to extract data from API"""
    orchestrator = get_pipeline_orchestrator()
    return asyncio.run(orchestrator.extract_data())


@task
def process_data_task(raw_data):
    """Task to process extracted data"""
    orchestrator = get_pipeline_orchestrator()
    return orchestrator.process_data(raw_data)


@task
def store_data_task(processed_data):
    """Task to store processed data"""
    orchestrator = get_pipeline_orchestrator()
    return orchestrator.store_data(processed_data)


@task
def generate_analytics_task():
    """Task to generate analytics"""
    orchestrator = get_pipeline_orchestrator()
    return orchestrator.generate_analytics()


@flow(name="data-pipeline", retries=2, retry_delay_seconds=60)
def data_pipeline_flow():
    """Main data pipeline flow"""
    logger.info("Starting data pipeline flow")
    
    # Extract data
    raw_data = extract_data_task()
    
    # Process data
    processed_data = process_data_task(raw_data)
    
    # Store in database
    store_data_task(processed_data)
    
    # Generate analytics
    analytics_report = generate_analytics_task()
    
    logger.info("Data pipeline flow completed successfully")
    return analytics_report


@flow(name="scheduled-data-pipeline")
def scheduled_data_pipeline_flow():
    """Scheduled version of the data pipeline"""
    return data_pipeline_flow()


class DataPipelineFlow:
    """Wrapper class for Prefect flow operations"""
    
    @staticmethod
    def run():
        """Run the pipeline flow manually"""
        return data_pipeline_flow()
    
    @staticmethod
    def deploy():
        """Deploy the flow for scheduling"""
        from prefect.deployments import Deployment
        
        deployment = Deployment.build_from_flow(
            flow=scheduled_data_pipeline_flow,
            name="daily-data-pipeline",
            schedule={"cron": "0 6 * * *"},  # Run daily at 6 AM
            work_queue_name="default"
        )
        
        deployment.apply()
        logger.info("Data pipeline deployment created")


if __name__ == "__main__":
    # Deploy the flow when running this script directly
    flow_manager = DataPipelineFlow()
    flow_manager.deploy()