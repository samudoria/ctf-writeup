from pwn import *
from gmpy2 import *
from Crypto.Util.number import long_to_bytes

r = remote("jupiter.challenges.picoctf.org", 58617)
r.recvuntil("q : ")
q = int(r.recvline())
r.recvuntil("p : ")
p = int(r.recvline())
n = p*q
r.recvuntil(":")
r.sendline("Y")
r.recvuntil("n: ")
r.sendline("{}".format(n))

r.recvuntil("p : ")
p = int(r.recvline())
r.recvuntil("n : ")
n = int(r.recvline())
r.recvuntil(":")
r.sendline("Y")
r.recvuntil("q: ")
q = n//p
r.sendline("{}".format(q))

r.recvuntil("e : ")
e = int(r.recvline())
r.recvuntil("n : ")
#n = mpz(r.recvline().split(":".encode())[1])
r.recvuntil(":")
#not possible
r.sendline("N")

r.recvuntil("q : ")
q = int(r.recvline())
r.recvuntil("p : ")
p = int(r.recvline())
totient = (p-1)*(q-1)
r.recvuntil(":")
r.sendline("Y")
r.recvuntil("totient(n): ")
r.sendline("{}".format(totient))

r.recvuntil("plaintext : ")
plain = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.recvuntil("e : ")
e = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.recvuntil("n : ")
n = gmpy2.mpz(r.recvline().split(":".encode())[-1])
c = gmpy2.powmod(plain, e, n)
r.recvuntil(":")
r.sendline("Y")
r.recvuntil("ciphertext: ")
r.sendline("{}".format(c))

r.recvuntil("(Y/N):")
r.sendline("N")

r.recvuntil("q : ")
q = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.recvuntil("p : ")
p = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.recvuntil("e : ")
e = gmpy2.mpz(r.recvline().split(":".encode())[-1])
totient = gmpy2.mul((p-1), (q-1))
n = gmpy2.mul(p, q)
d = gmpy2.invert(e, totient)
r.recvuntil(":")
r.sendline("Y")
r.recvuntil("d: ")
r.sendline("{}".format(d))

r.recvuntil("p : ")
p = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.recvuntil("ciphertext : ")
c = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.recvuntil("e : ")
e = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.recvuntil("n : ")
n = gmpy2.mpz(r.recvline().split(":".encode())[-1])
r.sendlineafter(":", "Y")
q = gmpy2.mpz(gmpy2.c_div(n, p))
totient = gmpy2.mpz(gmpy2.mul(p-1, q-1))
d = gmpy2.invert(e, totient)
plain = gmpy2.powmod(c, d, n)
r.sendlineafter("plaintext: ", "{}".format(plain))

print(long_to_bytes(plain))

r.interactive()
