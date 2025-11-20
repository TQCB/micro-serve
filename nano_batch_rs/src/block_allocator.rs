use std::{collections::HashSet};

struct Block {
    block_id: u32
}

pub struct BlockAllocator {
    num_blocks: u32,
    block_size: u32,
    free_blocks: Vec<Block>,
    allocated_blocks: HashSet<u32>
}

impl BlockAllocator{
    fn new(num_blocks: u32, block_size: u32) -> BlockAllocator {
        let mut free_blocks: Vec<Block> = Vec::with_capacity(num_blocks as usize);

        for i in 0..num_blocks {
            free_blocks.push(Block { block_id: i });
        }

        // reverse list of free blocks to store as stack we can pop off of
        let free_blocks = free_blocks.into_iter().rev().collect();

        BlockAllocator {
            num_blocks,
            block_size,
            free_blocks,
            allocated_blocks: HashSet::new(),
        }
    }

    /// Return Some(free_block_id) from off the top of the free_blocks stack
    /// Returns None if there are no free blocks left.
    /// 
    /// Returned free block is inserted into set of allocated blocks.
    fn allocate(&mut self) -> Option<u32> {
        let free_block = self.free_blocks.pop()?;
        self.allocated_blocks.insert(free_block.block_id);

        Some(free_block.block_id)
    }

    /// Adds a block (that must be currently allocated) to free blocks,
    /// removing it from the set of allocated blocks.
    fn free(&mut self, block_id: u32) -> Result<(), String> {
        if !self.allocated_blocks.contains(&block_id) {
            return Err("Block not allocated or already freed".to_string());
        }

        self.allocated_blocks.remove(&block_id);
        self.free_blocks.push(Block { block_id });

        Ok(())
    }
}