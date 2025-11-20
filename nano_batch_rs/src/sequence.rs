enum Status {
    Waiting,
    Running,
    Finished,
}

pub struct Sequence {
    request_id: u32, // unique identifier
    prompt_token_ids: Vec<u32>, // initial input
    output_token_ids: Vec<u32>, // generated tokens
    status: Status, // state
    mmap: Vec<u32>, // map logical block to physical block (idx: logical, val: physical)
}