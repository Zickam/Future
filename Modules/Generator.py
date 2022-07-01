from hashlib import sha256

def Double_SHA256(text):
    return sha256(sha256(text.encode()).hexdigest().encode()).hexdigest()

def Generator(string_to_hash):

    login = string_to_hash.upper()
    login_reversed = login[::-1]

    license_code_part_1 = Double_SHA256(login)
    license_code_part_2 = Double_SHA256(login_reversed)
    license_code_part_3 = Double_SHA256(str(len(login)))

    license_code = license_code_part_3 + license_code_part_1 + license_code_part_2

    return license_code
