import random



def generate_otp():
    new_otp = ''

    for i in range(0,5):
        otp = random.randint(0,9)
        new_otp += str(otp)

    return new_otp


