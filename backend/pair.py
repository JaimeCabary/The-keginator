import os
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv("SOLANA_PRIVATE_KEY")
public_key = os.getenv("SOLANA_PUBLIC_KEY")
program_id = os.getenv("KEGINATOR_PROGRAM_ID")

print(f"SOLANA_PRIVATE_KEY: {private_key}")
print(f"SOLANA_PUBLIC_KEY: {public_key}")
print(f"KEGINATOR_PROGRAM_ID: {program_id}")

if not private_key:
    print("⚠️ SOLANA_PRIVATE_KEY is missing or empty")
if not public_key:
    print("⚠️ SOLANA_PUBLIC_KEY is missing or empty")
if not program_id or program_id == "11111111111111111111111111111111":
    print("⚠️ KEGINATOR_PROGRAM_ID is missing or default")