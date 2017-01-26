from colorama import init, Fore
init()


def check_a(a):
    return int(a) == a


def check_afn(a, fn):
    return a % fn == 0


def check_all(a, fn):
    return check_a(a) and check_afn(a, fn)


def convert_frac(s):
    slash = s.find('/')
    if slash > 0:
        ans = float(s[:slash]) / float(s[slash + 1:])
    else:
        ans = float(s)
    return ans


again = True
ask = input('Would you like to change the default parameters? (y/n)').lower()
if ask == 'y':
    FN_NUM_LIMIT = int(input('What is the upper limit of fn\'s numerator? '
                             '(default is 200)'))
    FN_DEN_LIMIT = int(input("What is the upper limit of fn\'s denomenator? "
                             'You will give a number "n" as 2^n '
                             '(default is 2^10)'))
    D_LIMIT = int(input("what is upper limit for d? (default is 2000)"))
    HIGHLIGHT_FN = convert_frac(input('What fn would you like to highlight? '
                                      'Type 0 for none (default is 0)'))
    WRITE_TO_FILE = input('Write output to file named for the prime? (y/n) '
                          '(default is n)').lower() == 'y'
else:
    FN_NUM_LIMIT = 200
    FN_DEN_LIMIT = 10
    D_LIMIT = 2000
    HIGHLIGHT_FN = 0
    WRITE_TO_FILE = 'n'
print('This program will now run using these parameters until it is run again.'
      ' Type stop to end the program.')
print('\n')
while again:
    usedFns = []
    found_n = []
    ns = []
    p = input("What p would you like to check: ")
    if p.lower() == 'stop':
        break
    else:
        p = int(p)
    user_n = (p - 1) / 4
    if user_n != int(user_n):
        print("That isn't part of 4n + 1")
        continue
    ns.append(user_n)
    with open('%d.txt' % p, 'w') as f:
        f.write("Paramenters used to generate this file:\n")
        f.write('fn numerator limit = %d\n' % FN_NUM_LIMIT)
        f.write('fn denomenator limit (2^n) = %d\n' % FN_DEN_LIMIT)
        f.write('d limit = %d\n' % D_LIMIT)
        f.write('--------------------------------\n')
    print('\n')
    ds = [3 + 4 * i for i in range(D_LIMIT)]
    denoms = [2 ** den for den in range(FN_DEN_LIMIT)]
    for denom in denoms:
        for numer in range(1, FN_NUM_LIMIT):
            fn = numer / denom
            if fn not in usedFns:
                usedFns.append(fn)
            else:
                continue
            if numer % denom == 0:
                str_fn = '%d' % (numer / denom)
            else:
                str_fn = '%d/%d' % (numer, denom)

            for d in ds:
                for n in ns:
                    top = fn + 4 * n + 1
                    x = top / d
                    str_x = "%d/%d" % (top, d)
                    a = (n + (d + 1) / 4) * x
                    if check_all(a, fn):
                        if WRITE_TO_FILE == 'n':
                            if fn == HIGHLIGHT_FN:
                                print(Fore.RED
                                      + 'n = {0:10} fn = {1:10} x = {2:10}'
                                      .format(str(n), str_fn, str_x))
                            else:
                                print(Fore.RESET
                                      + 'n = {0:10} fn = {1:10} x = {2:10}'
                                      .format(str(n), str_fn, str_x))
                        else:
                            with open('%d.txt' % p, 'a') as f:
                                if fn == HIGHLIGHT_FN:
                                    f.write('n = {0:10} fn = {1:10} x = {2:10}*'
                                            .format(str(n), str_fn, str_x))
                                else:
                                    f.write('n = {0:10} fn = {1:10} x = {2:10}'
                                            .format(str(n), str_fn, str_x))
                                f.write('\n')





