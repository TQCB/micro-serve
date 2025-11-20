enum Status {
    WaitingDecode,
    WaitingPrefill,
    Running,
    Finished,
}

pub struct Request {
    request_id: u32, // unique identifier
    prompt_token_ids: Vec<u32>, // initial input
    output_token_ids: Vec<u32>, // generated tokens
    pub status: Status, // state
    mmap: Vec<u32>, // map logical block to physical block (idx: logical, val: physical)
    max_tokens: u32,
    end_tokens: Vec<u32>,
}

impl Request {
    fn len(&self) -> usize {
        self.output_token_ids.len()
    }

    /// Indicates whether any of the stopping conditions of the request are met.
    pub fn should_end(&self) -> bool {
        // check if max_tokens is reached
        if self.len() as u32 >= self.max_tokens {
            return true
        }

        // check if end_tokens are in the last position
        if let Some(last_token) = self.output_token_ids.last() {
            if self.end_tokens.contains(last_token) {
                return true
            }
        }

        false
    }
}