"""
nano_batch - Rust-based PagedAttention Scheduling Engine

A minimalist, high-performance scheduling engine for LLM inference with PagedAttention.

Core Components:
- Rust block allocator and continuous batching scheduler
- Pure PyTorch PagedAttention kernel
- KV cache management

For model implementations (Mistral, etc.), see the nano_batch_models package.
"""

from .engine import Engine, SchedulerOutput
from .paged_attention import paged_attention_fwd, KVCache

__version__ = "0.1.0"

__all__ = [
    "Engine",
    "SchedulerOutput",
    "paged_attention_fwd",
    "KVCache",
]
