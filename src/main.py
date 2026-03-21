import os
import git
from transformers import AutoModelForSequenceClassification
from .analyzers import ImpactAnalyzer, QualityGate
from .visualization import DependencyGraph

class GitLensAI:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
        self.impact_analyzer = ImpactAnalyzer()
        self.quality_gate = QualityGate()
        
    def analyze_commit(self, commit_hash: str) -> dict:
        diff = self.repo.git.diff(commit_hash)
        impact_score = self.impact_analyzer.predict_impact(diff)
        quality_metrics = self.quality_gate.evaluate(diff)
        
        return {
            'impact_score': impact_score,
            'quality_metrics': quality_metrics,
            'visualization': DependencyGraph.generate(diff)
        }
    
    def watch(self, enforce: bool = False):
        # Set up Git hooks for real-time analysis
        pass