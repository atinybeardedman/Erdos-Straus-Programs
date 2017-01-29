from colorama import init, Fore
import tkinter as tk
from tkinter import filedialog
import os
init()
root = tk.Tk()
root.withdraw()


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


def parseFns(s):
    fns = []
    if len(s) > 0:
        for item in s.split(','):
            fns.append(convert_frac(item.strip()))
    return fns


def testFn(fn, n, d_limit=2000):
    ds = [3 + 4 * i for i in range(d_limit)]
    for d in ds:
        top = fn + 4 * n + 1
        x = top / d
        str_x = "%d/%d" % (top, d)
        a = (n + (d + 1) / 4) * x
        if check_all(a, fn):
            return str_x
    return


def findFNs(p, no_print=False, d_limit=2000, fn_num_limit=200,
            fn_den_limit=10,
            highlight_fns=[], write_to_file=False):
    found_fns = {}
    tested_fns = []
    if p.lower() == 'stop':
        return
    else:
        p = int(p)
    user_n = (p - 1) / 4
    if user_n != int(user_n):
        print("That isn't part of 4n + 1")
        return
    n = user_n
    if write_to_file:
        FOLDER_PATH = filedialog.askdirectory(title="Select the folder to save the files")
        with open(os.path.join(FOLDER_PATH, '%d.txt' % p), 'w') as f:
            f.write("Paramenters used to generate this file:\n")
            f.write('fn numerator limit = %d\n' % fn_num_limit)
            f.write('fn denomenator limit (2^n) = %d\n' % fn_den_limit)
            f.write('d limit = %d\n' % d_limit)
            f.write('--------------------------------\n')
    denoms = [2 ** den for den in range(fn_den_limit)]
    for denom in denoms:
        for numer in range(1, fn_num_limit):
            fn = numer / denom
            if fn in tested_fns:
                continue
            else:
                tested_fns.append(fn)
            test = testFn(fn, n, d_limit)
            if test is not None:
                if numer % denom == 0:
                    str_fn = '%d' % (numer / denom)
                else:
                    str_fn = '%d/%d' % (numer, denom)
                if str_fn not in found_fns:
                    found_fns[str_fn] = p
                if no_print:
                    continue
                if not write_to_file:
                    if fn in highlight_fns:
                        print(Fore.RED
                            + 'n = {0:10} fn = {1:10} x = {2:10}'
                            .format(str(n), str_fn, test))
                    else:
                        print(Fore.RESET
                            + 'n = {0:10} fn = {1:10} x = {2:10}'
                            .format(str(n), str_fn, test))
                else:
                    with open(os.path.join(FOLDER_PATH, '%d.txt' % p), 'a') as f:
                        if fn in highlight_fns:
                            f.write('n = {0:10} fn = {1:10} x = {2:10}*'
                                    .format(str(n), str_fn, test))
                        else:
                            f.write('n = {0:10} fn = {1:10} x = {2:10}'
                                    .format(str(n), str_fn, test))
                        f.write('\n')
            else:
                continue
    return found_fns


def singleVersion():
    ask = input('Would you like to change the default parameters? (y/n)').lower()
    if ask == 'y':
        FN_NUM_LIMIT = int(input('What is the upper limit of fn\'s numerator? '
                                 '(default is 200)'))
        FN_DEN_LIMIT = int(input("What is the upper limit of fn\'s denomenator? "
                                 'You will give a number "n" as 2^n '
                                 '(default is 2^10)'))
        D_LIMIT = int(input("what is upper limit for d? (default is 2000)"))
        HIGHLIGHT_FNS = parseFns(input('What fns would you like to highlight? '
                                       'Seperate each fn with a comma.'
                                       'Type 0 for none (default is 0)'))
        WRITE_TO_FILE = input('Write output to file named for the prime? (y/n) '
                              '(default is n)').lower() == 'y'
    again = True
    while again:
        p = input("What p would you like to check: ")
        if ask == 'y':
            check = findFNs(p, False, D_LIMIT, FN_NUM_LIMIT, FN_DEN_LIMIT, HIGHLIGHT_FNS, WRITE_TO_FILE)
        else:
            check = findFNs(p)
        if check is None:
            return


def familyVersion():
    print("We will assume the family takes the form ak + b")
    a = int(input("What is a: "))
    b = int(input("What is b: "))
    change = input("would you like to change the default parameters (y/n): ") == 'y'
    if change:
        upper_limit = int(input("How many of this family should we test? (default is 10)"))
        min_display = int(input("Only display the fn if it works for how many primes? (default is 5): "))
        d = int(input("What should be the upper limit of d (default is 2000): "))
    else:
        upper_limit = 10
        min_display = 5
        d = 2000
    fns = {}
    correction = 0
    for k in range(1, upper_limit + 1):
        p = a * k + b
        if p < 0:
            correction += 1
            continue
        temp = findFNs(str(p), True, d)
        for fn in temp:
            if fn not in fns:
                fns[fn] = [temp[fn]]
            else:
                fns[fn].append(temp[fn])
    print("For family {}k + {}".format(a, b))
    print("{0:10} {1:10}".format('fn', 'primes'))
    for key in fns:
        if len(fns[key]) >= min_display:
            if len(fns[key]) == upper_limit - correction:
                print("{0:10} {1:10}*".format(key, str(fns[key])))
            else:
                print("{0:10} {1:10}".format(key, str(fns[key])))


def checkFamilyFn():
    print("We will assume the family takes the form ak + b")
    a = int(input("What is a: "))
    b = int(input("What is b: "))
    fn = parseFns(input("What fn would you like to test?"))[0]
    change = input("Would you like to change the default perameters? (y/n) ").lower() == 'y'
    if change:
        limit = int(input("How many of this family should we test? (default is 10) "))
        save_breaking_case = input("Would you like to know what prime caused it to fail? (y/n) ") == 'y'
    else:
        limit = 10
        save_breaking_case = True
    all_work = True
    working_xs = {}
    for k in range(1, limit):
        p = a * k + b
        n = (a * k + b - 1) / 4
        if n > 0:
            x = testFn(fn, n)
            if x is None:
                all_work = False
                if save_breaking_case:
                    print('Test failed for {}'.format(p))
                break
            else:
                working_xs[str(p)] = x
    if all_work:
        print("That worked.")
        for prime in working_xs:
            print("{:10} {:10}".format(prime, working_xs[prime]))
    else:
        print("That didn't work for all tested values in that family")


choice = input("Choose from the following options:\n"
               "1 - Enter primes manually and view working fns\n"
               "2 - Look for fns that work for an entire family\n"
               "3 - Try an fn for a family\n")
if choice == "1":
    singleVersion()
elif choice == '2':
    familyVersion()
elif choice == '3':
    checkFamilyFn()




