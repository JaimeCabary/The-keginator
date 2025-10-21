from solders.keypair import Keypair
import json

print("Generating Solana keypair... 🔐")

keypair = Keypair()
secret_key = list(keypair.secret())
public_key = str(keypair.pubkey())

print("\n✅ Public Key:", public_key)
print("\n🔑 SOLANA_PRIVATE_KEY (paste this into your .env as one line):")
print(json.dumps(secret_key))
