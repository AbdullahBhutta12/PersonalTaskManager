# import helpers
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash("correct horse battery staple")
a = ph.verify(hash, "correct horse battery staplea")
print(a)

