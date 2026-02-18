"""
Governance panel for document approval and management
"""
from typing import List, Dict, Any
from datetime import datetime
import json
from pathlib import Path
from backend.config import DATA_DIR


class GovernancePanel:
    """Manages document governance and approval workflow"""
    
    def __init__(self):
        self.governance_file = DATA_DIR / "governance.json"
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load governance data from file"""
        if self.governance_file.exists():
            try:
                with open(self.governance_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default structure
        return {
            "documents": {},
            "queries": [],
            "users": {},
            "stats": {
                "total_queries": 0,
                "total_uploads": 0
            }
        }
    
    def _save_data(self):
        """Save governance data to file"""
        try:
            with open(self.governance_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Failed to save governance data: {str(e)}")
    
    def register_document(
        self,
        document_id: str,
        filename: str,
        file_type: str,
        uploader: str = "anonymous"
    ):
        """Register a new document for governance"""
        self.data["documents"][document_id] = {
            "filename": filename,
            "file_type": file_type,
            "uploader": uploader,
            "upload_date": datetime.now().isoformat(),
            "status": "pending",  # pending, approved, rejected
            "approval_date": None,
            "approver": None,
            "rejection_reason": None
        }
        self.data["stats"]["total_uploads"] += 1
        self._save_data()
    
    def approve_document(self, document_id: str, approver: str = "admin"):
        """Approve a document"""
        if document_id in self.data["documents"]:
            self.data["documents"][document_id]["status"] = "approved"
            self.data["documents"][document_id]["approval_date"] = datetime.now().isoformat()
            self.data["documents"][document_id]["approver"] = approver
            self._save_data()
            return True
        return False
    
    def reject_document(
        self,
        document_id: str,
        reason: str = "Not suitable",
        approver: str = "admin"
    ):
        """Reject a document"""
        if document_id in self.data["documents"]:
            self.data["documents"][document_id]["status"] = "rejected"
            self.data["documents"][document_id]["approval_date"] = datetime.now().isoformat()
            self.data["documents"][document_id]["approver"] = approver
            self.data["documents"][document_id]["rejection_reason"] = reason
            self._save_data()
            return True
        return False
    
    def log_query(self, query: str, user: str = "anonymous"):
        """Log a user query"""
        self.data["queries"].append({
            "query": query[:200],
            "user": user,
            "timestamp": datetime.now().isoformat()
        })
        self.data["stats"]["total_queries"] += 1
        
        # Keep only last 1000 queries
        if len(self.data["queries"]) > 1000:
            self.data["queries"] = self.data["queries"][-1000:]
        
        self._save_data()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get governance statistics"""
        docs = self.data["documents"]
        
        pending = sum(1 for d in docs.values() if d["status"] == "pending")
        approved = sum(1 for d in docs.values() if d["status"] == "approved")
        rejected = sum(1 for d in docs.values() if d["status"] == "rejected")
        
        # Calculate storage (simplified)
        storage_mb = len(docs) * 0.5  # Estimate 0.5 MB per document
        
        return {
            "total_documents": len(docs),
            "pending_approval": pending,
            "approved_documents": approved,
            "rejected_documents": rejected,
            "total_queries": self.data["stats"]["total_queries"],
            "active_users": len(self.data["users"]),
            "storage_used_mb": round(storage_mb, 2)
        }
    
    def get_pending_documents(self) -> List[Dict[str, Any]]:
        """Get all pending documents"""
        pending = []
        for doc_id, doc_data in self.data["documents"].items():
            if doc_data.get("status") == "pending":
                pending.append({
                    "document_id": doc_id,
                    **doc_data
                })
        return pending
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents"""
        all_docs = []
        for doc_id, doc_data in self.data["documents"].items():
            all_docs.append({
                "document_id": doc_id,
                **doc_data
            })
        return all_docs


# Global instance
_governance_panel: GovernancePanel = None


def get_governance_panel() -> GovernancePanel:
    """Get GovernancePanel instance"""
    global _governance_panel
    if _governance_panel is None:
        _governance_panel = GovernancePanel()
    return _governance_panel
