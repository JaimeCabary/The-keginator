# from solana.rpc.async_api import AsyncClient
# from solders.keypair import Keypair
# from solders.pubkey import Pubkey
# from solders.instruction import Instruction, AccountMeta
# from solders.transaction import Transaction as SoldersTransaction
# from solders.message import Message
# import base58
# import os
# import json
# from typing import Tuple, Optional
# import struct
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class SolanaClient:
#     """
#     Solana blockchain client for Keginator
#     Commits dataset hashes to Solana devnet
#     """

#     def __init__(self):
#         # Use devnet for hackathon
#         self.rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
#         self.client = AsyncClient(self.rpc_url)

#         # Load payer keypair from env
#         private_key = os.getenv("SOLANA_PRIVATE_KEY")
#         if not private_key:
#             logger.warning("No SOLANA_PRIVATE_KEY provided. Using ephemeral keypair.")
#             self.payer = Keypair()
#         else:
#             try:
#                 # Handle JSON array format (from solana-keygen)
#                 if private_key.strip().startswith('['):
#                     key_bytes = bytes(json.loads(private_key))
#                 else:
#                     # Handle Base58 format (e.g., Phantom export)
#                     key_bytes = base58.b58decode(private_key)[:64]

#                 # Validate key length
#                 if len(key_bytes) != 64:
#                     raise ValueError(f"Invalid key length: {len(key_bytes)} bytes, expected 64")

#                 self.payer = Keypair.from_bytes(key_bytes)
#             except Exception as e:
#                 logger.error(f"Invalid SOLANA_PRIVATE_KEY format: {e}")
#                 self.payer = Keypair()
#                 logger.warning("Using ephemeral keypair due to invalid private key.")

#         # Program ID (deployed Anchor program)
#         program_id_str = os.getenv("KEGINATOR_PROGRAM_ID")
#         if not program_id_str or program_id_str == "11111111111111111111111111111111":
#             logger.warning("Invalid or default KEGINATOR_PROGRAM_ID. Using placeholder.")
#             self.program_id = Pubkey.from_string("11111111111111111111111111111111")
#         else:
#             try:
#                 self.program_id = Pubkey.from_string(program_id_str)
#             except Exception as e:
#                 logger.error(f"Invalid KEGINATOR_PROGRAM_ID format: {e}")
#                 raise ValueError("KEGINATOR_PROGRAM_ID is invalid")

#         logger.info(f"Solana client initialized: {self.rpc_url}")
#         logger.info(f"Payer public key: {self.payer.pubkey()}")

#     def is_connected(self) -> bool:
#         """Check if connected to Solana"""
#         try:
#             return self.client is not None and not self.client.is_closed()
#         except Exception as e:
#             logger.error(f"Connection check failed: {e}")
#             return False

#     async def commit_hash(
#         self,
#         dataset_hash: str,
#         user_id: str,
#         timestamp: int
#     ) -> str:
#         """
#         Commit dataset hash to Solana blockchain
#         Returns: transaction signature
#         """
#         try:
#             if not dataset_hash or not user_id:
#                 raise ValueError("Dataset hash and user ID must not be empty")

#             dataset_pda, bump = self._get_dataset_pda(dataset_hash)
#             instruction_data = self._build_commit_instruction(dataset_hash, user_id, timestamp, bump)

#             instruction = Instruction(
#                 program_id=self.program_id,
#                 accounts=[
#                     AccountMeta(pubkey=dataset_pda, is_signer=False, is_writable=True),
#                     AccountMeta(pubkey=self.payer.pubkey(), is_signer=True, is_writable=True),
#                     AccountMeta(
#                         pubkey=Pubkey.from_string("11111111111111111111111111111111"),
#                         is_signer=False,
#                         is_writable=False
#                     ),
#                 ],
#                 data=instruction_data,
#             )

#             blockhash_resp = await self.client.get_latest_blockhash()
#             blockhash = blockhash_resp.value.blockhash

#             message = Message.new_with_blockhash(
#                 [instruction],
#                 self.payer.pubkey(),
#                 blockhash
#             )

#             transaction = SoldersTransaction([self.payer], message, blockhash)
#             response = await self.client.send_transaction(transaction)
#             signature = str(response.value)

#             await self.client.confirm_transaction(signature)
#             logger.info(f"Hash committed to Solana: {signature}")
#             return signature

#         except Exception as e:
#             logger.error(f"Solana commit failed: {e}")
#             raise Exception(f"Failed to commit to Solana: {str(e)}")

#     async def verify_hash(self, dataset_hash: str) -> Tuple[bool, Optional[int]]:
#         """
#         Verify if dataset hash exists on Solana
#         Returns: (exists, timestamp)
#         """
#         try:
#             if not dataset_hash:
#                 raise ValueError("Dataset hash must not be empty")

#             dataset_pda, _ = self._get_dataset_pda(dataset_hash)
#             account_info = await self.client.get_account_info(dataset_pda)

#             if account_info.value is None:
#                 logger.info(f"No account found for dataset hash: {dataset_hash[:16]}...")
#                 return False, None

#             data = account_info.value.data
#             if len(data) >= 81:
#                 timestamp = struct.unpack('<Q', data[72:80])[0]
#                 logger.info(f"Hash verified: {dataset_hash[:16]}... with timestamp {timestamp}")
#                 return True, timestamp

#             logger.info(f"Hash exists but no timestamp: {dataset_hash[:16]}...")
#             return True, None

#         except Exception as e:
#             logger.error(f"Verification error: {e}")
#             return False, None

#     def _get_dataset_pda(self, dataset_hash: str) -> Tuple[Pubkey, int]:
#         """Generate Program Derived Address (PDA) for dataset hash"""
#         if not dataset_hash:
#             raise ValueError("Dataset hash cannot be empty")

#         seeds = [
#             b"dataset",
#             dataset_hash.encode()[:32]
#         ]
#         pda, bump = Pubkey.find_program_address(seeds, self.program_id)
#         return pda, bump

#     def _build_commit_instruction(
#         self,
#         dataset_hash: str,
#         user_id: str,
#         timestamp: int,
#         bump: int
#     ) -> bytes:
#         """Build instruction data for Solana transaction"""
#         discriminator = bytes([174, 39, 232, 127, 252, 3, 250, 87])

#         hash_bytes = dataset_hash.encode()[:32].ljust(32, b'\0')
#         user_bytes = user_id.encode()[:32].ljust(32, b'\0')
#         timestamp_bytes = struct.pack('<Q', timestamp)
#         bump_bytes = bytes([bump])

#         return discriminator + hash_bytes + user_bytes + timestamp_bytes + bump_bytes

#     async def get_balance(self) -> float:
#         """Get payer account balance in SOL"""
#         try:
#             balance = await self.client.get_balance(self.payer.pubkey())
#             sol_balance = balance.value / 1_000_000_000
#             logger.info(f"Payer balance: {sol_balance} SOL")
#             return sol_balance
#         except Exception as e:
#             logger.error(f"Failed to get balance: {e}")
#             return 0.0

#     async def close(self):
#         """Close client connection"""
#         try:
#             await self.client.close()
#             logger.info("Solana client connection closed")
#         except Exception as e:
#             logger.error(f"Failed to close client: {e}")

# async def test_connection():
#     """Utility function for testing Solana connection"""
#     client = SolanaClient()
#     try:
#         balance = await client.get_balance()
#         logger.info(f"Connected to Solana")
#         logger.info(f"Balance: {balance} SOL")
#         return True
#     except Exception as e:
#         logger.error(f"Connection failed: {e}")
#         return False
#     finally:
#         await client.close()




# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_connection())


# blockchain.py

from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from solders.transaction import Transaction as SoldersTransaction
from solders.message import Message
import base58
import base64
import os
import json
from typing import Tuple, Optional
import struct
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolanaClient:
    """
    Solana blockchain client for Keginator
    Commits dataset hashes to Solana devnet
    """

    def __init__(self):
        # Use devnet for hackathon
        self.rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
        self.client = AsyncClient(self.rpc_url)

        # Load payer keypair from env
        private_key = os.getenv("SOLANA_PRIVATE_KEY")
        if not private_key:
            logger.warning("No SOLANA_PRIVATE_KEY provided. Using ephemeral keypair.")
            self.payer = Keypair()
        else:
            try:
                private_key = private_key.strip()
                
                # Case 1: JSON array format (from solana-keygen)
                if private_key.startswith('['):
                    key_bytes = bytes(json.loads(private_key))
                
                # Case 2: Base58 format
                elif re.match(r'^[1-9A-HJ-NP-Za-km-z]+$', private_key):
                    key_bytes = base58.b58decode(private_key)
                
                # Case 3: Base64 format (New requirement)
                elif re.match(r'^[A-Za-z0-9+/=]+$', private_key):
                    key_bytes = base64.b64decode(private_key)
                
                else:
                    raise ValueError("Key format is not recognized (JSON, Base58, or Base64)")

                # Validate and process key bytes
                if len(key_bytes) < 64:
                    # Pad with null bytes if the decoded secret key is less than 64 bytes (shouldn't happen for valid keys)
                    key_bytes = key_bytes.ljust(64, b'\0')
                else:
                    # Trim to 64 bytes (secret key)
                    key_bytes = key_bytes[:64]

                self.payer = Keypair.from_bytes(key_bytes)
                
            except Exception as e:
                logger.error(f"Invalid SOLANA_PRIVATE_KEY format: {e}")
                self.payer = Keypair()
                logger.warning("Using ephemeral keypair due to invalid private key.")

        # Program ID (deployed Anchor program)
        program_id_str = os.getenv("KEGINATOR_PROGRAM_ID")
        if not program_id_str or program_id_str == "11111111111111111111111111111111":
            logger.warning("Invalid or default KEGINATOR_PROGRAM_ID. Using placeholder.")
            self.program_id = Pubkey.from_string("11111111111111111111111111111111")
        else:
            try:
                self.program_id = Pubkey.from_string(program_id_str)
            except Exception as e:
                logger.error(f"Invalid KEGINATOR_PROGRAM_ID format: {e}")
                raise ValueError("KEGINATOR_PROGRAM_ID is invalid")

        logger.info(f"🔗 Solana client initialized: {self.rpc_url}")
        logger.info(f"💼 Payer public key: {self.payer.pubkey()}")

    def is_connected(self) -> bool:
        """Check if connected to Solana"""
        try:
            return self.client is not None and not self.client.is_closed()
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False

    async def commit_hash(
        self,
        dataset_hash: str,
        user_id: str,
        timestamp: int
    ) -> str:
        """
        Commit dataset hash to Solana blockchain
        Returns: transaction signature
        """
        try:
            if not dataset_hash or not user_id:
                raise ValueError("Dataset hash and user ID must not be empty")

            dataset_pda, bump = self._get_dataset_pda(dataset_hash)
            instruction_data = self._build_commit_instruction(dataset_hash, user_id, timestamp, bump)

            instruction = Instruction(
                program_id=self.program_id,
                accounts=[
                    AccountMeta(pubkey=dataset_pda, is_signer=False, is_writable=True),
                    AccountMeta(pubkey=self.payer.pubkey(), is_signer=True, is_writable=True),
                    AccountMeta(
                        pubkey=Pubkey.from_string("11111111111111111111111111111111"),
                        is_signer=False,
                        is_writable=False
                    ),
                ],
                data=instruction_data,
            )

            blockhash_resp = await self.client.get_latest_blockhash()
            blockhash = blockhash_resp.value.blockhash

            # --- Streamlined Solders Transaction Construction (The fix) ---
            message = Message.new_with_blockhash(
                [instruction],
                self.payer.pubkey(),
                blockhash
            )
            
            # Use the new_signed_with_payer method which handles blockhash and signing
            transaction = SoldersTransaction.new_signed_with_payer(
                message,
                self.payer.pubkey(),
                self.payer,
                [self.payer]
            )
            
            # Send the transaction (already signed)
            response = await self.client.send_transaction(transaction)
            signature = str(response.value)

            # Wait for confirmation
            await self.client.confirm_transaction(signature)
            logger.info(f"Hash committed to Solana: {signature}")
            return signature

        except Exception as e:
            logger.error(f"Solana commit failed: {e}")
            raise Exception(f"Failed to commit to Solana: {str(e)}")

    async def verify_hash(self, dataset_hash: str) -> Tuple[bool, Optional[int]]:
        """
        Verify if dataset hash exists on Solana
        Returns: (exists, timestamp)
        """
        try:
            if not dataset_hash:
                raise ValueError("Dataset hash must not be empty")

            dataset_pda, _ = self._get_dataset_pda(dataset_hash)
            account_info = await self.client.get_account_info(dataset_pda)

            if account_info.value is None:
                logger.info(f"No account found for dataset hash: {dataset_hash[:16]}...")
                return False, None

            data = account_info.value.data
            if len(data) >= 81:
                # The timestamp is typically at byte 72 in Anchor PDAs
                timestamp = struct.unpack('<Q', data[72:80])[0]
                logger.info(f"Hash verified: {dataset_hash[:16]}... with timestamp {timestamp}")
                return True, timestamp

            logger.info(f"Hash exists but no timestamp: {dataset_hash[:16]}...")
            return True, None

        except Exception as e:
            logger.error(f"Verification error: {e}")
            return False, None

    def _get_dataset_pda(self, dataset_hash: str) -> Tuple[Pubkey, int]:
        """Generate Program Derived Address (PDA) for dataset hash"""
        if not dataset_hash:
            raise ValueError("Dataset hash cannot be empty")

        seeds = [
            b"dataset",
            dataset_hash.encode()[:32]
        ]
        pda, bump = Pubkey.find_program_address(seeds, self.program_id)
        return pda, bump

    def _build_commit_instruction(
        self,
        dataset_hash: str,
        user_id: str,
        timestamp: int,
        bump: int
    ) -> bytes:
        """Build instruction data for Solana transaction"""
        discriminator = bytes([174, 39, 232, 127, 252, 3, 250, 87])

        hash_bytes = dataset_hash.encode()[:32].ljust(32, b'\0')
        user_bytes = user_id.encode()[:32].ljust(32, b'\0')
        timestamp_bytes = struct.pack('<Q', timestamp)
        bump_bytes = bytes([bump])

        return discriminator + hash_bytes + user_bytes + timestamp_bytes + bump_bytes

    async def get_balance(self) -> float:
        """Get payer account balance in SOL"""
        try:
            balance = await self.client.get_balance(self.payer.pubkey())
            sol_balance = balance.value / 1_000_000_000
            logger.info(f"Payer balance: {sol_balance} SOL")
            return sol_balance
        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            return 0.0

    async def close(self):
        """Close client connection"""
        try:
            await self.client.close()
            logger.info("Solana client connection closed")
        except Exception as e:
            logger.error(f"Failed to close client: {e}")




