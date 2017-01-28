def generatePrimes(stop):
    primes = [2]
    for test in range(3, stop + 1):
        flag = True
        for prime in primes:
            if test % prime == 0:
                flag = False
                break
        if flag:
            primes.append(test)
    return primes


def testPrime(p):
    for test in generatePrimes(int(p ** 0.5)):
        if p % test == 0:
            return False
    return True


p = int(input("What number would you like to test: "))

if testPrime(p):
    print("Prime")
else:
    print("Composite")


