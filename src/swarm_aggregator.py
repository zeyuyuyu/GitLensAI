import os
import sys
import time
import random
import multiprocessing as mp
from typing import List, Tuple, Dict

class SwarmAggregator:
    def __init__(self, num_nodes: int, node_data_fn: callable, aggregation_fn: callable):
        self.num_nodes = num_nodes
        self.node_data_fn = node_data_fn
        self.aggregation_fn = aggregation_fn
        self.nodes = [SwarmNode(i, self.node_data_fn) for i in range(num_nodes)]
        self.manager = mp.Manager()
        self.result_queue = self.manager.Queue()

    def run(self):
        processes = []
        for node in self.nodes:
            p = mp.Process(target=node.run, args=(self.result_queue,))
            p.start()
            processes.append(p)

        while True:
            try:
                node_data = self.result_queue.get(timeout=1)
                self.aggregation_fn(node_data)
            except queue.Empty:
                if not any(p.is_alive() for p in processes):
                    break

        for p in processes:
            p.join()

        return self.aggregation_fn.get_result()

class SwarmNode:
    def __init__(self, node_id: int, node_data_fn: callable):
        self.node_id = node_id
        self.node_data_fn = node_data_fn

    def run(self, result_queue: mp.Queue):
        data = self.node_data_fn()
        result_queue.put(data)

class AverageAggregator:
    def __init__(self):
        self.total = 0
        self.count = 0

    def __call__(self, data: Any):
        self.total += data
        self.count += 1

    def get_result(self):
        return self.total / self.count

if __name__ == '__main__':
    def generate_node_data() -> float:
        return random.uniform(0, 100)

    aggregator = SwarmAggregator(10, generate_node_data, AverageAggregator())
    result = aggregator.run()
    print(f'Final result: {result}')