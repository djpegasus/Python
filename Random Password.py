import random
import string
digits = random.sample(string.digits,4)
lower = random.sample(string.ascii_lowercase,8)
upper = random.sample(string.ascii_uppercase,2)
special = random.sample(["$","@","!","_"],2)
pass_list = upper + lower + digits + special
password = "".join(pass_list) #oluşan şifre arasındaki boşlukları silme veya tırnak arasına eklenen karakteri harflarin arasına ekler
print("RANDOM PASSWORD: " + password)