# Final Checked Code with Fixes

import math

# Vernam Cipher
def vernam_encrypt(plaintext, key):
    plaintext = ''.join(filter(str.isalpha, plaintext.upper()))  # Ensure only letters
    key = ''.join(filter(str.isalpha, key.upper()))  # Ensure only letters
    ciphertext = ''.join(
        chr(((ord(p) - 65) ^ (ord(k) - 65)) + 65) for p, k in zip(plaintext, key)
    )
    return ''.join(filter(str.isalpha, ciphertext))  # Return only letters

def vernam_decrypt(ciphertext, key):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))  # Ensure only letters
    key = ''.join(filter(str.isalpha, key.upper()))  # Ensure only letters
    plaintext = ''.join(
        chr(((ord(c) - 65) ^ (ord(k) - 65)) + 65) for c, k in zip(ciphertext, key)
    )
    return ''.join(filter(str.isalpha, plaintext))  # Return only letters

# Columnar Transposition Cipher
def columnar_encrypt(text, key):
    text = ''.join(filter(str.isalpha, text.upper()))  # Ensure only letters
    key = ''.join(filter(str.isalpha, key.upper()))  # Ensure only letters
    
    if not key:  # Check if the key is empty
        raise ValueError("Key cannot be empty. Please provide a valid key.")
    
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)
    grid = [text[i:i + num_cols] for i in range(0, len(text), num_cols)]
    grid[-1] = grid[-1].ljust(num_cols, 'X')  # Padding with 'X'

    ciphertext = ''.join([''.join([row[col] for row in grid]) for col in key_order])
    return ''.join(filter(str.isalpha, ciphertext))  # Return only letters

def columnar_decrypt(ciphertext, key):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))  # Ensure only letters
    key = ''.join(filter(str.isalpha, key.upper()))  # Ensure only letters
    
    if not key:  # Check if the key is empty
        raise ValueError("Key cannot be empty. Please provide a valid key.")
    
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)
    
    # Calculate column lengths
    full_cols = len(ciphertext) % num_cols
    col_lengths = [num_rows if i < full_cols else num_rows - 1 for i in range(num_cols)]

    # Recreate columns from the ciphertext
    cols = []
    idx = 0
    for col_len in col_lengths:
        cols.append(ciphertext[idx:idx + col_len])
        idx += col_len

    # Decrypt by arranging rows back in order
    decrypted_grid = [''.join([cols[key_order.index(c)][r] for c in range(num_cols) if r < len(cols[key_order.index(c)])]) for r in range(num_rows)]
    return ''.join(filter(str.isalpha, ''.join(decrypted_grid).strip('X')))  # Return only letters

# Rail Fence Cipher
def rail_fence_encrypt(text, depth):
    text = ''.join(filter(str.isalpha, text.upper()))  # Ensure only letters
    rail = [''] * depth
    row = 0
    direction = 1  # 1 for down, -1 for up

    for char in text:
        rail[row] += char
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1

    return ''.join(filter(str.isalpha, ''.join(rail)))  # Return only letters

def rail_fence_decrypt(ciphertext, depth):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))  # Ensure only letters
    length = len(ciphertext)
    rail = [[''] * length for _ in range(depth)]
    
    row, direction = 0, 1
    for i in range(length):
        rail[row][i] = '*'
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1

    idx = 0
    for r in range(depth):
        for c in range(length):
            if rail[r][c] == '*' and idx < len(ciphertext):
                rail[r][c] = ciphertext[idx]
                idx += 1

    result = []
    row, direction = 0, 1
    for i in range(length):
        result.append(rail[row][i])
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1

    return ''.join(filter(str.isalpha, ''.join(result)))  # Return only letters

# Main Program
if __name__ == "__main__":
    try:
        print("Choose Operation:")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        choice = int(input("Enter your choice (1 or 2): "))

        if choice == 1:
            print("\n=== Encryption ===")
            plaintext = input("Enter the plaintext: ")
            method = input("Choose a method (Vernam, Columnar, RailFence): ").lower()

            if method == "vernam":
                key = input("Enter the key (same length as plaintext): ")
                encrypted = vernam_encrypt(plaintext, key)
                print(f"Encrypted text: {encrypted}")
            
            elif method == "columnar":
                key = input("Enter the key (letters or numbers): ").upper()
                encrypted = columnar_encrypt(plaintext, key)
                print(f"Encrypted text: {encrypted}")
            
            elif method == "railfence":
                depth = int(input("Enter the depth (number): "))
                encrypted = rail_fence_encrypt(plaintext, depth)
                print(f"Encrypted text: {encrypted}")
            
            else:
                print("Invalid method selected.")

        elif choice == 2:
            print("\n=== Decryption ===")
            ciphertext = input("Enter the ciphertext: ")
            method = input("Choose a method (Vernam, Columnar, RailFence): ").lower()

            if method == "vernam":
                key = input("Enter the key (same length as ciphertext): ")
                decrypted = vernam_decrypt(ciphertext, key)
                print(f"Decrypted text: {decrypted}")
            
            elif method == "columnar":
                key = input("Enter the key (letters or numbers): ").upper()
                decrypted = columnar_decrypt(ciphertext, key)
                print(f"Decrypted text: {decrypted}")
            
            elif method == "railfence":
                depth = int(input("Enter the depth (number): "))
                decrypted = rail_fence_decrypt(ciphertext, depth)
                print(f"Decrypted text: {decrypted}")
            
            else:
                print("Invalid method selected.")

        else:
            print("Invalid choice.")

    except Exception as e:
        print(f"Error: {e}")