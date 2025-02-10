
import key_recovery.single_key as kr
from key_recovery.utils import pqhash
import random

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from demos.single_key_recovery import KeyRecoveryApp

app = QApplication(sys.argv)
ex = KeyRecoveryApp()
sys.exit(app.exec_())

threadhold = 2
prime = 4567
secret = 1234
number_of_shares = 5
password = "password"

random.seed()  # Initialize the random number generator
generator = kr.SingleKeyGenerator(threadhold, prime)
generator.commit(secret)
# print(generator.commitment)
shares = generator.generate_shares(password, number_of_shares)
# for share in shares:
#     print(share.share, share.tag, share.commitment)


recoverer = kr.SingleKeyRecoverer(threadhold, prime)
key = recoverer.recover(shares)

print(key)

validator = kr.SingleKeyValidator(generator.commitment)

print("Changing the first share")   
shares[0].share = ('1', '1')

for share in shares:
    if validator.validate_share(share, password):
        print("Share is valid")
    else:
        print("Share is invalid")

key = recoverer.recover(shares)
print(key)

if validator.validate_secret(key):
    print("Secret is valid")
else:
    print("Secret is invalid")

key = recoverer.recover(shares[1:])
print("Without the first share")  
print(key)

if validator.validate_secret(key):
    print("Secret is valid")
else:
    print("Secret is invalid")

