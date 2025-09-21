import json
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime
import logging

from src.domain.interfaces import FileStorageInterface
from src.config import get_settings

logger = logging.getLogger(__name__)


class FileStorage(FileStorageInterface):
    def __init__(self):
        self.settings = get_settings()
        self.data_dir = Path(self.settings.data_dir)
        self.reports_dir = Path(self.settings.reports_dir)
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.data_dir / "raw",
            self.data_dir / "processed", 
            self.reports_dir
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _get_date_partition_path(self, base_path: Path, date_partition: datetime) -> Path:
        """Get path with date partition (YYYY-MM-DD format)"""
        date_str = date_partition.strftime("%Y-%m-%d")
        partition_path = base_path / date_str
        partition_path.mkdir(parents=True, exist_ok=True)
        return partition_path

    def save_raw_data(self, data: Any, filename: str, date_partition: datetime) -> str:
        """Save raw data in JSON format"""
        partition_path = self._get_date_partition_path(
            self.data_dir / "raw", date_partition
        )
        filepath = partition_path / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Raw data saved to {filepath}")
        return str(filepath)

    def save_processed_data(self, data: Any, filename: str, date_partition: datetime) -> str:
        """Save processed data in Parquet format"""
        partition_path = self._get_date_partition_path(
            self.data_dir / "processed", date_partition
        )
        filepath = partition_path / f"{filename}.parquet"
        
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError("Data must be a list or DataFrame for Parquet storage")
        
        df.to_parquet(filepath, index=False)
        logger.info(f"Processed data saved to {filepath}")
        return str(filepath)

    def load_raw_data(self, filename: str, date_partition: datetime) -> Any:
        """Load raw data from JSON file"""
        partition_path = self._get_date_partition_path(
            self.data_dir / "raw", date_partition
        )
        filepath = partition_path / f"{filename}.json"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Raw data file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Raw data loaded from {filepath}")
        return data

    def load_processed_data(self, filename: str, date_partition: datetime) -> pd.DataFrame:
        """Load processed data from Parquet file"""
        partition_path = self._get_date_partition_path(
            self.data_dir / "processed", date_partition
        )
        filepath = partition_path / f"{filename}.parquet"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Processed data file not found: {filepath}")
        
        df = pd.read_parquet(filepath)
        logger.info(f"Processed data loaded from {filepath}")
        return df

    def save_report(self, data: Any, filename: str, format: str = "json") -> str:
        """Save report in specified format"""
        if format.lower() == "json":
            filepath = self.reports_dir / f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        elif format.lower() == "csv":
            filepath = self.reports_dir / f"{filename}.csv"
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data
            df.to_csv(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Report saved to {filepath}")
        return str(filepath)

    def list_files(self, directory: str, date_partition: Optional[datetime] = None) -> List[str]:
        """List files in a directory, optionally filtered by date partition"""
        if directory == "raw":
            base_path = self.data_dir / "raw"
        elif directory == "processed":
            base_path = self.data_dir / "processed"
        elif directory == "reports":
            base_path = self.reports_dir
        else:
            raise ValueError(f"Unknown directory: {directory}")
        
        if date_partition and directory != "reports":
            search_path = self._get_date_partition_path(base_path, date_partition)
        else:
            search_path = base_path
        
        if not search_path.exists():
            return []
        
        return [str(f.relative_to(search_path)) for f in search_path.iterdir() if f.is_file()]