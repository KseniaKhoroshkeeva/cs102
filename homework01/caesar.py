def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    ciphertext = ""
    for letter in plaintext:
        if ("A" <= letter <= "Z") or ("a" <= letter <= "z"):
            if letter == "X":
                letter = "A"
            elif letter == "Y":
                letter = "B"
            elif letter == "Z":
                letter = "C"
            elif letter == "x":
                letter = "a"
            elif letter == "y":
                letter = "b"
            elif letter == "z":
                letter = "c"
            else:
                letter= chr(ord(letter) + 3)
        ciphertext += letter
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    plaintext = ""
    for letter in ciphertext:
        if ("A" <= letter <= "Z") or ("a" <= letter <= "z"):
            if letter == "a":
                letter = "x"
            elif letter == "b":
                letter = "y"
            elif letter == "c":
                letter = "z"
            elif letter == "A":
                letter = "X"
            elif letter == "B":
                letter = "Y"
            elif letter == "C":
                letter = "Z"
            else:
                letter= chr(ord(letter) - 3)
        plaintext += letter
    return plaintext
