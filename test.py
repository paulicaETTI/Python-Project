print("ana are mere")
print("Project update from 2nd computer")

#EXERCITIUL 1
def sumNumbers1(*args, **kwargs):

    numbers = []
    for i in args:
        if isinstance(i, (int, float)):         #append parameters without key to an empty list
            numbers.append(i)
        # sau: if type(i) == int or type(i) == float

    for key, value in kwargs.items():
        if isinstance(value, (int, float)):     #append parameters with key to the numbers list
            numbers.append(value)
        # sau: if type(value) == int or type(value) == float

    return sum(numbers)                         #sum of the numbers list

print(sumNumbers1(2,-10,10.8,'haha',[1,2,3], param_1=2, param_3=5.2))

#EXERCITIUL 2
def sumNumbers2(n):
    if n == 0:
        return 0
    return n + sumNumbers2(n-1)

def sumNumbers2even(n):
    if n == 0 or n == 1:
        return 0
    if n % 2 == 0:
        return n + sumNumbers2even(n - 2)
    else:
        return n - 1 + sumNumbers2even(n - 3)

def sumNumbers2odd(n):
    if n <= 0:
        return 0
    if n % 2 == 1:
        return n + sumNumbers2odd(n - 2)
    else:
        return n - 1 + sumNumbers2odd(n - 3)

print(f"Gauss = {sumNumbers2(10)}, Even Gauss = {sumNumbers2even(10)}, Odd Gauss = {sumNumbers2odd(10)}")









