# # from solana.rpc.async_api import AsyncClient
# # from solders.keypair import Keypair  # Changed from solana.keypair
# # from solana.transaction import Transaction
# # from solders.system_program import transfer, TransferParams  # Changed import
# # from solders.pubkey import Pubkey
# # from solders.instruction import Instruction, AccountMeta
# # from solders.transaction import Transaction as SoldersTransaction  # May need this
# # import base58
# # import os
# # import json
# # from typing import Tuple, Optional
# # import struct


# # class SolanaClient:
# #     """
# #     Solana blockchain client for Keginator
# #     Commits dataset hashes to Solana devnet
# #     """

# #     def __init__(self):
# #         # Use devnet for hackathon
# #         self.rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
# #         self.client = AsyncClient(self.rpc_url)

# #         # Load payer keypair from env
# #         private_key = os.getenv("SOLANA_PRIVATE_KEY")

# #         if private_key:
# #             try:
# #                 # Case 1: JSON array format (from solana-keygen)
# #                 if private_key.strip().startswith('['):
# #                     key_bytes = bytes(json.loads(private_key))
# #                 else:
# #                     # Case 2: Base58 format (e.g., Phantom export)
# #                     decoded = base58.b58decode(private_key)
# #                     key_bytes = decoded[:64]  # Trim to 64 bytes if longer

# #                 # solders.Keypair expects a 64-byte seed (secret key)
# #                 self.payer = Keypair.from_bytes(key_bytes)
# #             except Exception as e:
# #                 print(f"⚠️ Invalid SOLANA_PRIVATE_KEY format ({e}). Using ephemeral keypair instead.")
# #                 self.payer = Keypair()
# #         else:
# #             # No key provided → ephemeral keypair for testing
# #             self.payer = Keypair()
# #             print("⚠️ Warning: Using ephemeral keypair. Set SOLANA_PRIVATE_KEY in production.")

# #         # Program ID (deployed Anchor program)
# #         program_id_str = os.getenv("KEGINATOR_PROGRAM_ID", "11111111111111111111111111111111")
# #         self.program_id = Pubkey.from_string(program_id_str)

# #         print(f"🔗 Solana client initialized: {self.rpc_url}")
# #         print(f"💼 Payer: {self.payer.pubkey()}")

# #     def is_connected(self) -> bool:
# #         """Check if connected to Solana"""
# #         try:
# #             return self.client is not None
# #         except:
# #             return False

# #     async def commit_hash(
# #         self,
# #         dataset_hash: str,
# #         user_id: str,
# #         timestamp: int
# #     ) -> str:
# #         """
# #         Commit dataset hash to Solana blockchain
# #         Returns: transaction signature
# #         """
# #         try:
# #             dataset_pda, bump = self._get_dataset_pda(dataset_hash)

# #             # Build instruction data
# #             instruction_data = self._build_commit_instruction(
# #                 dataset_hash, user_id, timestamp, bump
# #             )

# #             # Create instruction
# #             instruction = Instruction(
# #                 program_id=self.program_id,
# #                 accounts=[
# #                     AccountMeta(pubkey=dataset_pda, is_signer=False, is_writable=True),
# #                     AccountMeta(pubkey=self.payer.pubkey(), is_signer=True, is_writable=True),
# #                     AccountMeta(pubkey=Pubkey.from_string("11111111111111111111111111111111"), is_signer=False, is_writable=False),
# #                 ],
# #                 data=instruction_data,
# #             )

# #             from solders.message import Message
# #             from solders.transaction import Transaction as SoldersTransaction

# #             blockhash_resp = await self.client.get_latest_blockhash()
# #             blockhash = blockhash_resp.value.blockhash

# #             message = Message.new_with_blockhash(
# #                 [instruction],
# #                 self.payer.pubkey(),
# #                 blockhash
# #             )

# #             transaction = SoldersTransaction.new_unsigned(message)
# #             transaction = SoldersTransaction([self.payer], message, blockhash)

# #             response = await self.client.send_transaction(transaction)
# #             signature = str(response.value)

# #             await self.client.confirm_transaction(signature)

# #             print(f"✅ Hash committed to Solana: {signature}")
# #             return signature

# #         except Exception as e:
# #             print(f"❌ Solana commit failed: {e}")
# #             raise Exception(f"Failed to commit to Solana: {str(e)}")

# #     async def verify_hash(self, dataset_hash: str) -> Tuple[bool, Optional[int]]:
# #         """
# #         Verify if dataset hash exists on Solana
# #         Returns: (exists, timestamp)
# #         """
# #         try:
# #             dataset_pda, _ = self._get_dataset_pda(dataset_hash)
# #             account_info = await self.client.get_account_info(dataset_pda)

# #             if account_info.value is None:
# #                 return False, None

# #             data = account_info.value.data
# #             if len(data) >= 81:
# #                 timestamp = struct.unpack('<Q', data[72:80])[0]
# #                 return True, timestamp

# #             return True, None

# #         except Exception as e:
# #             print(f"⚠️ Verification error: {e}")
# #             return False, None

# #     def _get_dataset_pda(self, dataset_hash: str) -> Tuple[Pubkey, int]:
# #         seeds = [
# #             b"dataset",
# #             dataset_hash.encode()[:32]
# #         ]
# #         pda, bump = Pubkey.find_program_address(seeds, self.program_id)
# #         return pda, bump

# #     def _build_commit_instruction(
# #         self,
# #         dataset_hash: str,
# #         user_id: str,
# #         timestamp: int,
# #         bump: int
# #     ) -> bytes:
# #         discriminator = bytes([174, 39, 232, 127, 252, 3, 250, 87])

# #         hash_bytes = dataset_hash.encode()[:32].ljust(32, b'\0')
# #         user_bytes = user_id.encode()[:32].ljust(32, b'\0')
# #         timestamp_bytes = struct.pack('<Q', timestamp)
# #         bump_bytes = bytes([bump])

# #         return discriminator + hash_bytes + user_bytes + timestamp_bytes + bump_bytes

# #     async def get_balance(self) -> float:
# #         """Get payer account balance in SOL"""
# #         try:
# #             balance = await self.client.get_balance(self.payer.pubkey())
# #             return balance.value / 1e9
# #         except:
# #             return 0.0

# #     async def close(self):
# #         """Close client connection"""
# #         await self.client.close()


# # # Utility function for testing
# # async def test_connection():
# #     client = SolanaClient()
# #     try:
# #         balance = await client.get_balance()
# #         print(f"✅ Connected to Solana")
# #         print(f"💰 Balance: {balance} SOL")
# #         return True
# #     except Exception as e:
# #         print(f"❌ Connection failed: {e}")
# #         return False
# #     finally:
# #         await client.close()


# # if __name__ == "__main__":
# #     import asyncio
# #     asyncio.run(test_connection())




# from solana.rpc.async_api import AsyncClient
# from solders.keypair import Keypair
# from solana.transaction import Transaction
# from solders.system_program import transfer, TransferParams
# from solders.pubkey import Pubkey
# from solders.instruction import Instruction, AccountMeta
# from solders.transaction import Transaction as SoldersTransaction
# import base58
# import os
# import json
# from typing import Tuple, Optional
# import struct


# class SolanaClient:
#     """
#     Solana blockchain client for Keginator
#     Commits dataset hashes to Solana devnet
#     """

#     def __init__(self):
#         self.rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
#         self.client = AsyncClient(self.rpc_url)

#         # Load payer keypair from env
#         private_key = os.getenv("SOLANA_PRIVATE_KEY")

#         if private_key:
#             try:
#                 # Case 1: JSON array format (from solana-keygen)
#                 if private_key.strip().startswith('['):
#                     key_bytes = bytes(json.loads(private_key))
#                     # Trim to 64 bytes if needed
#                     if len(key_bytes) > 64:
#                         key_bytes = key_bytes[:64]
#                 else:
#                     # Case 2: Base58 format (e.g., Phantom export)
#                     decoded = base58.b58decode(private_key)
#                     key_bytes = decoded[:64]

#                 # FIXED: Use from_bytes (not from_secret_key)
#                 self.payer = Keypair.from_bytes(key_bytes)
                
#             except Exception as e:
#                 print(f"⚠️ Invalid SOLANA_PRIVATE_KEY format ({e}). Using ephemeral keypair instead.")
#                 self.payer = Keypair()
#         else:
#             self.payer = Keypair()
#             print("⚠️ Warning: Using ephemeral keypair. Set SOLANA_PRIVATE_KEY in production.")

#         # Program ID (deployed Anchor program)
#         program_id_str = os.getenv("KEGINATOR_PROGRAM_ID", "11111111111111111111111111111111")
#         self.program_id = Pubkey.from_string(program_id_str)

#         print(f"🔗 Solana client initialized: {self.rpc_url}")
#         print(f"💼 Payer: {self.payer.pubkey()}")

#     def is_connected(self) -> bool:
#         """Check if connected to Solana"""
#         try:
#             return self.client is not None
#         except:
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
#             dataset_pda, bump = self._get_dataset_pda(dataset_hash)

#             instruction_data = self._build_commit_instruction(
#                 dataset_hash, user_id, timestamp, bump
#             )

#             instruction = Instruction(
#                 program_id=self.program_id,
#                 accounts=[
#                     AccountMeta(pubkey=dataset_pda, is_signer=False, is_writable=True),
#                     AccountMeta(pubkey=self.payer.pubkey(), is_signer=True, is_writable=True),
#                     AccountMeta(pubkey=Pubkey.from_string("11111111111111111111111111111111"), is_signer=False, is_writable=False),
#                 ],
#                 data=instruction_data,
#             )

#             from solders.message import Message
#             from solders.transaction import Transaction as SoldersTransaction

#             blockhash_resp = await self.client.get_latest_blockhash()
#             blockhash = blockhash_resp.value.blockhash

#             message = Message.new_with_blockhash(
#                 [instruction],
#                 self.payer.pubkey(),
#                 blockhash
#             )

#             transaction = SoldersTransaction.new_unsigned(message)
#             transaction = SoldersTransaction([self.payer], message, blockhash)

#             response = await self.client.send_transaction(transaction)
#             signature = str(response.value)

#             await self.client.confirm_transaction(signature)

#             print(f"✅ Hash committed to Solana: {signature}")
#             return signature

#         except Exception as e:
#             print(f"❌ Solana commit failed: {e}")
#             raise Exception(f"Failed to commit to Solana: {str(e)}")

#     async def verify_hash(self, dataset_hash: str) -> Tuple[bool, Optional[int]]:
#         """
#         Verify if dataset hash exists on Solana
#         Returns: (exists, timestamp)
#         """
#         try:
#             dataset_pda, _ = self._get_dataset_pda(dataset_hash)
#             account_info = await self.client.get_account_info(dataset_pda)

#             if account_info.value is None:
#                 return False, None

#             data = account_info.value.data
#             if len(data) >= 81:
#                 timestamp = struct.unpack('<Q', data[72:80])[0]
#                 return True, timestamp

#             return True, None

#         except Exception as e:
#             print(f"⚠️ Verification error: {e}")
#             return False, None

#     def _get_dataset_pda(self, dataset_hash: str) -> Tuple[Pubkey, int]:
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
#             return balance.value / 1e9
#         except:
#             return 0.0

#     async def close(self):
#         """Close client connection"""
#         await self.client.close()


# async def test_connection():
#     client = SolanaClient()
#     try:
#         balance = await client.get_balance()
#         print(f"✅ Connected to Solana")
#         print(f"💰 Balance: {balance} SOL")
#         return True
#     except Exception as e:
#         print(f"❌ Connection failed: {e}")
#         return False
#     finally:
#         await client.close()


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_connection())



from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from solders.transaction import Transaction as SoldersTransaction
from solders.message import Message
import base58
import os
import json
from typing import Tuple, Optional
import struct
import logging

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
                # Handle JSON array format (from solana-keygen)
                if private_key.strip().startswith('['):
                    key_bytes = bytes(json.loads(private_key))
                else:
                    # Handle Base58 format (e.g., Phantom export)
                    key_bytes = base58.b58decode(private_key)[:64]

                # Validate key length
                if len(key_bytes) != 64:
                    raise ValueError(f"Invalid key length: {len(key_bytes)} bytes, expected 64")

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

        logger.info(f"Solana client initialized: {self.rpc_url}")
        logger.info(f"Payer public key: {self.payer.pubkey()}")

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

            message = Message.new_with_blockhash(
                [instruction],
                self.payer.pubkey(),
                blockhash
            )

            transaction = SoldersTransaction([self.payer], message, blockhash)
            response = await self.client.send_transaction(transaction)
            signature = str(response.value)

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

async def test_connection():
    """Utility function for testing Solana connection"""
    client = SolanaClient()
    try:
        balance = await client.get_balance()
        logger.info(f"Connected to Solana")
        logger.info(f"Balance: {balance} SOL")
        return True
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False
    finally:
        await client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())