def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    ciphertext = ""
    temp = keyword
    while len(keyword) < len(plaintext):
        keyword += temp
    number = -1
    for letter in plaintext:
        number += 1
        if ('A' <= letter <= 'Z') or ('a' <= letter <= 'z'):
            a = (ord(letter) % 32) - 1
            a += (ord(keyword[number]) % 32) - 1
            a = a % 26 + 1
            if letter <= 'Z':
                newletter = chr(a + 64)
            else:
                newletter = chr(a + 96)  
        else:
            newletter = letter
        ciphertext += newletter
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    return plaintext
