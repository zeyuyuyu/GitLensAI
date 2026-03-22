import difflib
import git
import openai
import os
from typing import List, Dict

class GitLensAI:
    def __init__(self, repo_path: str, api_key: str = None):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def get_smart_diff(self, commit_sha: str) -> Dict:
        """Generate an AI-enhanced diff summary with commit suggestions."""
        commit = self.repo.commit(commit_sha)
        parent = commit.parents[0] if commit.parents else None
        
        if not parent:
            return {'error': 'No parent commit found'}

        diffs = []
        for diff in commit.diff(parent):
            if diff.a_path and diff.b_path:
                old_content = diff.a_blob.data_stream.read().decode('utf-8')
                new_content = diff.b_blob.data_stream.read().decode('utf-8')
                diff_text = '\n'.join(difflib.unified_diff(
                    old_content.splitlines(),
                    new_content.splitlines(),
                    fromfile=diff.a_path,
                    tofile=diff.b_path
                ))
                diffs.append({
                    'file': diff.b_path,
                    'diff': diff_text
                })

        # Generate AI analysis
        analysis = self._analyze_changes(diffs)
        suggestions = self._generate_suggestions(analysis)

        return {
            'commit_sha': commit_sha,
            'commit_message': commit.message,
            'changes': diffs,
            'analysis': analysis,
            'suggestions': suggestions
        }

    def _analyze_changes(self, diffs: List[Dict]) -> str:
        """Analyze code changes using OpenAI."""
        prompt = f"Analyze these code changes and provide a concise summary:\n\n"
        for diff in diffs:
            prompt += f"File: {diff['file']}\n{diff['diff']}\n\n"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code review assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def _generate_suggestions(self, analysis: str) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        prompt = f"Based on this analysis, suggest specific improvements:\n\n{analysis}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code improvement advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        
        suggestions = response.choices[0].message.content.split('\n')
        return [s.strip() for s in suggestions if s.strip()]

    def analyze_latest_commit(self) -> Dict:
        """Analyze the most recent commit."""
        latest_commit = self.repo.head.commit
        return self.get_smart_diff(latest_commit.hexsha)

if __name__ == '__main__':
    lens = GitLensAI('.')
    analysis = lens.analyze_latest_commit()
    print(f"Analysis for commit {analysis['commit_sha']}:\n")
    print(f"Commit Message: {analysis['commit_message']}\n")
    print(f"AI Analysis:\n{analysis['analysis']}\n")
    print("Suggestions:")
    for suggestion in analysis['suggestions']:
        print(f"- {suggestion}")