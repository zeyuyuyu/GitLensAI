import asyncio
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
from src.swarm_aggregator import SwarmAggregator

class GitLensAI:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.aggregator = SwarmAggregator()
        self.batch_size = 50

    async def process_file(self, file_path: Path) -> Dict:
        """Process a single file and return its analysis results"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return {
                'path': str(file_path),
                'analysis': await self.aggregator.analyze(content),
                'status': 'success'
            }
        except Exception as e:
            return {
                'path': str(file_path),
                'error': str(e),
                'status': 'error'
            }

    async def process_batch(self, files: List[Path]) -> List[Dict]:
        """Process a batch of files concurrently"""
        tasks = [self.process_file(f) for f in files]
        return await asyncio.gather(*tasks)

    async def analyze_repository(self) -> List[Dict]:
        """Analyze entire repository with progress tracking"""
        all_files = list(self.repo_path.rglob('*.py'))
        results = []
        
        with tqdm(total=len(all_files), desc='Analyzing repository') as pbar:
            for i in range(0, len(all_files), self.batch_size):
                batch = all_files[i:i + self.batch_size]
                batch_results = await self.process_batch(batch)
                results.extend(batch_results)
                pbar.update(len(batch))
        
        return results

def main():
    repo_path = './'
    analyzer = GitLensAI(repo_path)
    
    results = asyncio.run(analyzer.analyze_repository())
    
    # Print summary
    success = sum(1 for r in results if r['status'] == 'success')
    errors = sum(1 for r in results if r['status'] == 'error')
    print(f'\nAnalysis complete:\n{success} files processed successfully\n{errors} errors')

if __name__ == '__main__':
    main()