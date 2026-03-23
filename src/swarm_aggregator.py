import asyncio
from typing import List, Dict, Any
import aiohttp
import backoff
from datetime import datetime

class SwarmAggregator:
    def __init__(self, nodes: List[str], timeout: int = 30):
        self.nodes = nodes
        self.timeout = timeout
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @backoff.on_exception(backoff.expo,
                         (aiohttp.ClientError, asyncio.TimeoutError),
                         max_tries=5)
    async def _fetch_node_data(self, node: str) -> Dict[str, Any]:
        async with self.session.get(
            f'{node}/data',
            timeout=self.timeout
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def aggregate_data(self) -> Dict[str, Any]:
        tasks = [self._fetch_node_data(node) for node in self.nodes]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        aggregated_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'node_count': len(self.nodes),
            'successful_nodes': 0,
            'failed_nodes': 0,
            'data': []
        }

        for result in results:
            if isinstance(result, Exception):
                aggregated_data['failed_nodes'] += 1
                continue
            aggregated_data['successful_nodes'] += 1
            aggregated_data['data'].append(result)

        return aggregated_data

    @staticmethod
    def merge_results(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        merged = {}
        for entry in data:
            for key, value in entry.items():
                if key not in merged:
                    merged[key] = []
                if isinstance(value, (int, float)):
                    merged[key].append(value)

        # Calculate statistics for numeric values
        stats = {}
        for key, values in merged.items():
            if values:
                stats[key] = {
                    'mean': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }

        return stats

    async def get_aggregated_stats(self) -> Dict[str, Any]:
        raw_data = await self.aggregate_data()
        if raw_data['data']:
            raw_data['statistics'] = self.merge_results(raw_data['data'])
        return raw_data
