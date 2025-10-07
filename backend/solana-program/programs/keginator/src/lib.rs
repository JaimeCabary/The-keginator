use anchor_lang::prelude::*;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod keginator {
    use super::*;

    /// Commit a dataset hash to the blockchain
    pub fn commit_hash(
        ctx: Context<CommitHash>,
        dataset_hash: [u8; 32],
        user_id: [u8; 32],
        timestamp: i64,
    ) -> Result<()> {
        let dataset_record = &mut ctx.accounts.dataset_record;
        
        // Store dataset information
        dataset_record.dataset_hash = dataset_hash;
        dataset_record.user_id = user_id;
        dataset_record.timestamp = timestamp;
        dataset_record.bump = *ctx.bumps.get("dataset_record").unwrap();
        
        msg!("Dataset hash committed!");
        msg!("Hash: {:?}", dataset_hash);
        msg!("Timestamp: {}", timestamp);
        
        Ok(())
    }

    /// Verify if a dataset hash exists
    pub fn verify_hash(
        _ctx: Context<VerifyHash>,
        _dataset_hash: [u8; 32],
    ) -> Result<bool> {
        // The existence of the account proves the hash was committed
        // This is called off-chain to check if account exists
        Ok(true)
    }
}

#[derive(Accounts)]
#[instruction(dataset_hash: [u8; 32])]
pub struct CommitHash<'info> {
    #[account(
        init,
        payer = payer,
        space = 8 + DatasetRecord::INIT_SPACE,
        seeds = [b"dataset", dataset_hash.as_ref()],
        bump
    )]
    pub dataset_record: Account<'info, DatasetRecord>,
    
    #[account(mut)]
    pub payer: Signer<'info>,
    
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(dataset_hash: [u8; 32])]
pub struct VerifyHash<'info> {
    #[account(
        seeds = [b"dataset", dataset_hash.as_ref()],
        bump = dataset_record.bump
    )]
    pub dataset_record: Account<'info, DatasetRecord>,
}

#[account]
#[derive(InitSpace)]
pub struct DatasetRecord {
    pub dataset_hash: [u8; 32],  // SHA-256 hash of cleaned dataset
    pub user_id: [u8; 32],        // User identifier
    pub timestamp: i64,           // Unix timestamp
    pub bump: u8,                 // PDA bump seed
}

#[error_code]
pub enum ErrorCode {
    #[msg("Dataset hash already exists")]
    HashAlreadyExists,
    
    #[msg("Invalid hash length")]
    InvalidHashLength,
    
    #[msg("Unauthorized access")]
    Unauthorized,
}