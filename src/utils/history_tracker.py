"""Application History Tracker with JSON storage."""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class HistoryTracker:
    """Track all job applications."""
    
    HISTORY_FILE = Path("data/application_history.json")
    
    @classmethod
    def initialize(cls):
        """Create data directory and file if not exists."""
        cls.HISTORY_FILE.parent.mkdir(exist_ok=True)
        if not cls.HISTORY_FILE.exists():
            cls.HISTORY_FILE.write_text("[]")
    
    @classmethod
    def add_application(cls, data: Dict):
        """Add new application record."""
        cls.initialize()
        
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        data['id'] = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Load existing
        history = cls.get_all()
        history.append(data)
        
        # Save
        cls.HISTORY_FILE.write_text(json.dumps(history, indent=2))
    
    @classmethod
    def get_all(cls) -> List[Dict]:
        """Get all applications."""
        cls.initialize()
        try:
            return json.loads(cls.HISTORY_FILE.read_text())
        except:
            return []
    
    @classmethod
    def get_stats(cls) -> Dict:
        """Get application statistics."""
        history = cls.get_all()
        
        if not history:
            return {
                'total_applications': 0,
                'avg_ats_score': 0,
                'companies': [],
                'roles': []
            }
        
        return {
            'total_applications': len(history),
            'avg_ats_score': sum(h.get('ats_score', 0) for h in history) / len(history),
            'companies': list(set(h.get('company', '') for h in history)),
            'roles': list(set(h.get('role', '') for h in history))
        }
