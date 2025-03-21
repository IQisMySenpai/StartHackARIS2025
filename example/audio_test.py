import base64
import hashlib
import hmac
from Crypto.Cipher import AES
import requests


def download_enc_file(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download file: Status Code {response.status_code}")


def derive_keys(media_key: bytes):
    expanded_key = hmac.new(b'WhatsApp Media Keys', media_key, hashlib.sha256).digest()
    enc_key = expanded_key[:32]  # First 32 bytes are the encryption key
    mac_key = expanded_key[32:]  # Last 32 bytes are the MAC key
    return enc_key, mac_key


def pad_to_multiple_of_16(data: bytes) -> bytes:
    """
    If data is not a multiple of 16 bytes, pad with zeroes.
    """
    padding_length = (16 - len(data) % 16) % 16
    return data + (b'\x00' * padding_length)


def decrypt_file(enc_data: bytes, enc_key: bytes) -> bytes:
    iv = enc_data[:16]  # Initialization Vector (IV)
    cipher = AES.new(enc_key, AES.MODE_CBC, iv)

    # Get encrypted payload
    encrypted_payload = enc_data[16:]
    padded_payload = pad_to_multiple_of_16(encrypted_payload)

    decrypted = cipher.decrypt(padded_payload)
    return decrypted


def verify_decryption(decrypted_data: bytes, expected_hash_b64: str) -> bool:
    # Compare the fileEncSha256 hash
    calculated_hash = hashlib.sha256(decrypted_data).digest()
    expected_hash = base64.b64decode(expected_hash_b64)
    return calculated_hash == expected_hash


def save_file(file_path: str, data: bytes):
    with open(file_path, 'wb') as f:
        f.write(data)


if __name__ == "__main__":
    # Convert media key to Uint8Array
    media_key_b64 = "MifkAe9CpZ1urle+3h3WU8y/TGrBoPVL3bYhebk0hW0="
    media_key = base64.b64decode(media_key_b64)

    # Derive encryption keys
    enc_key, mac_key = derive_keys(media_key)

    # URL of the encrypted file
    file_url = "https://mmg.whatsapp.net/v/t62.7117-24/34597152_2004757583343163_556445408732480372_n.enc?ccb=11-4&oh=01_Q5AaIXNvst0stw_6G22M-4n3yHpClvxMUicjf0JD1kuc3Xok&oe=6803E3A7&_nc_sid=5e03e0"

    # Provided hash for verification
    file_enc_sha256_b64 = "1Sa9u0VSiEloBefZtE95qB4xnusTKkOhQ1gLnG7CFqA="

    # Download encrypted file
    enc_data = download_enc_file(file_url)

    # Decrypt file
    decrypted_data = decrypt_file(enc_data, enc_key)

    # Verify the decrypted file
    if verify_decryption(decrypted_data, file_enc_sha256_b64):
        save_file("decrypted_audio.ogg", decrypted_data)
        print("✅ File decrypted successfully and saved as 'decrypted_audio.ogg'")
    else:
        print("❌ Decryption failed: The decrypted file hash does not match the expected hash.")
