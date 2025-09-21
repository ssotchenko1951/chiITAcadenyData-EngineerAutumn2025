import json
import pandas as pd
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

from src.domain.entities import AnalyticsReport
from src.domain.interfaces import ReportGeneratorInterface
from src.config import get_settings

class ReportGenerator(ReportGeneratorInterface):
    def __init__(self):
        self.settings = get_settings()
        self.reports_dir = Path(self.settings.reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_analytics_report(self, data: Dict[str, Any]) -> AnalyticsReport:
        """Generate analytics report from raw data"""
        return AnalyticsReport(
            generated_at=datetime.utcnow(),
            total_users=data.get("total_users", 0),
            total_posts=data.get("total_posts", 0),
            total_comments=data.get("total_comments", 0),
            average_posts_per_user=data.get("average_posts_per_user", 0.0),
            most_active_user=data.get("most_active_user"),
            engagement_metrics=data.get("top_posts_by_engagement", [])
        )

    def export_to_csv(self, report: AnalyticsReport, filepath: str) -> None:
        """Export report to CSV format"""
        # Create a flattened view for CSV
        report_data = {
            "generated_at": report.generated_at,
            "total_users": report.total_users,
            "total_posts": report.total_posts,
            "total_comments": report.total_comments,
            "average_posts_per_user": report.average_posts_per_user,
            "most_active_user": report.most_active_user,
        }
        
        # Main report
        df_main = pd.DataFrame([report_data])
        
        # Engagement metrics in separate section
        df_engagement = pd.DataFrame(report.engagement_metrics)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write("# Analytics Report Summary\n")
            df_main.to_csv(f, index=False)
            f.write("\n# Top Posts by Engagement\n")
            df_engagement.to_csv(f, index=False)

    def export_to_json(self, report: AnalyticsReport, filepath: str) -> None:
        """Export report to JSON format"""
        report_dict = {
            "generated_at": report.generated_at.isoformat(),
            "total_users": report.total_users,
            "total_posts": report.total_posts,
            "total_comments": report.total_comments,
            "average_posts_per_user": report.average_posts_per_user,
            "most_active_user": report.most_active_user,
            "engagement_metrics": report.engagement_metrics,
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)

    def generate_filename(self, format: str, prefix: str = "analytics") -> str:
        """Generate timestamped filename"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{prefix}_{timestamp}.{format}"