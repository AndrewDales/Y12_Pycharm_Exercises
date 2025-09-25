def encode_message(plain_text_message, p_shift):
    """ Encode a message using the Caesar Cipher"""
    plain_text_message = plain_text_message.lower()
    encoded_message = ""

    for letter in plain_text_message:

        if letter.isalpha():
            num = ord(letter)
            num += p_shift
            if num > ord("z"):
                num -= 26
            char = chr(num)
            encoded_message += char
        else:
            encoded_message += letter

    return encoded_message