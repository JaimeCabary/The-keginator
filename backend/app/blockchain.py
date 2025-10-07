from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair  # Changed from solana.keypair
from solana.transaction import Transaction
from solders.system_program import transfer, TransferParams  # Changed import
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from solders.transaction import Transaction as SoldersTransaction  # May need this
import base58
import os
import json
from typing import Tuple, Optional
import struct


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

        if private_key:
            try:
                # Case 1: JSON array format (from solana-keygen)
                if private_key.strip().startswith('['):
                    key_bytes = bytes(json.loads(private_key))
                else:
                    # Case 2: Base58 format (e.g., Phantom export)
                    decoded = base58.b58decode(private_key)
                    key_bytes = decoded[:64]  # Trim to 64 bytes if longer

                # solders.Keypair expects a 64-byte seed (secret key)
                self.payer = Keypair.from_bytes(key_bytes)
            except Exception as e:
                print(f"⚠️ Invalid SOLANA_PRIVATE_KEY format ({e}). Using ephemeral keypair instead.")
                self.payer = Keypair()
        else:
            # No key provided → ephemeral keypair for testing
            self.payer = Keypair()
            print("⚠️ Warning: Using ephemeral keypair. Set SOLANA_PRIVATE_KEY in production.")

        # Program ID (deployed Anchor program)
        program_id_str = os.getenv("KEGINATOR_PROGRAM_ID", "11111111111111111111111111111111")
        self.program_id = Pubkey.from_string(program_id_str)

        print(f"🔗 Solana client initialized: {self.rpc_url}")
        print(f"💼 Payer: {self.payer.pubkey()}")

    def is_connected(self) -> bool:
        """Check if connected to Solana"""
        try:
            return self.client is not None
        except:
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
            dataset_pda, bump = self._get_dataset_pda(dataset_hash)

            # Build instruction data
            instruction_data = self._build_commit_instruction(
                dataset_hash, user_id, timestamp, bump
            )

            # Create instruction
            instruction = Instruction(
                program_id=self.program_id,
                accounts=[
                    AccountMeta(pubkey=dataset_pda, is_signer=False, is_writable=True),
                    AccountMeta(pubkey=self.payer.pubkey(), is_signer=True, is_writable=True),
                    AccountMeta(pubkey=Pubkey.from_string("11111111111111111111111111111111"), is_signer=False, is_writable=False),
                ],
                data=instruction_data,
            )

            from solders.message import Message
            from solders.transaction import Transaction as SoldersTransaction

            blockhash_resp = await self.client.get_latest_blockhash()
            blockhash = blockhash_resp.value.blockhash

            message = Message.new_with_blockhash(
                [instruction],
                self.payer.pubkey(),
                blockhash
            )

            transaction = SoldersTransaction.new_unsigned(message)
            transaction = SoldersTransaction([self.payer], message, blockhash)

            response = await self.client.send_transaction(transaction)
            signature = str(response.value)

            await self.client.confirm_transaction(signature)

            print(f"✅ Hash committed to Solana: {signature}")
            return signature

        except Exception as e:
            print(f"❌ Solana commit failed: {e}")
            raise Exception(f"Failed to commit to Solana: {str(e)}")

    async def verify_hash(self, dataset_hash: str) -> Tuple[bool, Optional[int]]:
        """
        Verify if dataset hash exists on Solana
        Returns: (exists, timestamp)
        """
        try:
            dataset_pda, _ = self._get_dataset_pda(dataset_hash)
            account_info = await self.client.get_account_info(dataset_pda)

            if account_info.value is None:
                return False, None

            data = account_info.value.data
            if len(data) >= 81:
                timestamp = struct.unpack('<Q', data[72:80])[0]
                return True, timestamp

            return True, None

        except Exception as e:
            print(f"⚠️ Verification error: {e}")
            return False, None

    def _get_dataset_pda(self, dataset_hash: str) -> Tuple[Pubkey, int]:
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
            return balance.value / 1e9
        except:
            return 0.0

    async def close(self):
        """Close client connection"""
        await self.client.close()


# Utility function for testing
async def test_connection():
    client = SolanaClient()
    try:
        balance = await client.get_balance()
        print(f"✅ Connected to Solana")
        print(f"💰 Balance: {balance} SOL")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    finally:
        await client.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())
