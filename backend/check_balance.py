from solders.pubkey import Pubkey
from solana.rpc.api import Client

# Connect to Solana Devnet
client = Client("https://api.devnet.solana.com")

# Your wallet public key
pubkey = Pubkey.from_string("6mNTeA3u4DccZQzcjwSXcDD9kH3f69ctnocn5yHyNxRf")

# Get balance (returns lamports — 1 SOL = 1 000 000 000 lamports)
balance = client.get_balance(pubkey)
sol_balance = balance.value / 1_000_000_000

print(f"Your balance: {sol_balance} SOL")
