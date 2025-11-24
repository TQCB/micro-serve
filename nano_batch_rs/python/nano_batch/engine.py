"""Python wrapper for the Rust nano_batch engine."""

from typing import Dict, List
from dataclasses import dataclass

# Import the Rust module (built by maturin)
from ._nano_batch import PySchedulerOutput
from ._nano_batch import Engine as RustEngine

@dataclass
class SchedulerOutput:
    """Type-safe wrapper for scheduler output."""
    
    scheduled_requests: List[str]
    block_tables: Dict[str, List[int]]
    slot_mappings: List[int]
    num_tokens_per_request: Dict[str, int]
    
    @classmethod
    def from_rust(cls, rust_output: PySchedulerOutput) -> "SchedulerOutput":
        """Convert Rust PySchedulerOutput to Python dataclass."""
        return cls(
            scheduled_requests=rust_output.scheduled_requests,
            block_tables=rust_output.block_tables,
            slot_mappings=rust_output.slot_mappings,
            num_tokens_per_request=rust_output.num_tokens_per_request,
        )


class Engine:
    """
    Python wrapper for the Rust-based continuous batching engine.
    
    This engine implements PagedAttention-style memory management with
    continuous batching for efficient LLM inference.
    
    Args:
        num_blocks: Total number of memory blocks available
        block_size: Number of tokens that fit in each block
    """
    
    def __init__(self, num_blocks: int, block_size: int):
        self._engine = RustEngine(num_blocks, block_size)
    
    def add_request(
        self,
        request_id: str,
        prompt_token_ids: List[int],
        temperature: float = 1.0,
        top_p: float = 1.0,
        max_tokens: int = 100,
        stop_tokens: List[int] | None = None,
    ) -> None:
        """
        Add a new inference request to the scheduler.
        
        Args:
            request_id: Unique identifier for this request
            prompt_token_ids: Input tokens for the prompt
            temperature: Sampling temperature (default: 1.0)
            top_p: Nucleus sampling parameter (default: 1.0)
            max_tokens: Maximum tokens to generate (default: 100)
            stop_tokens: List of token IDs that end generation (default: [])
        """
        if stop_tokens is None:
            stop_tokens = []
        
        self._engine.add_request(
            request_id,
            prompt_token_ids,
            temperature,
            top_p,
            max_tokens,
            stop_tokens,
        )
    
    def step(self) -> SchedulerOutput:
        """
        Run one scheduling step.
        
        Returns:
            SchedulerOutput containing:
                - scheduled_requests: List of request IDs to process
                - block_tables: Mapping of request_id -> physical block IDs
                - slot_mappings: Token index -> physical slot mapping
                - num_tokens_per_request: Request_id -> number of tokens
        """
        rust_output = self._engine.step()
        return SchedulerOutput.from_rust(rust_output)
    
    def update(self, token_updates: Dict[str, int]) -> None:
        """
        Update requests with newly generated tokens.
        
        Args:
            token_updates: Mapping of request_id -> new_token_id
        """
        self._engine.update(token_updates)
