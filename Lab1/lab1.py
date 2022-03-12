from math import ceil, sqrt
from matplotlib import pyplot as plt

def get_graphic(x, y, name):
    plt.plot(x, y)
    plt.title(name)
    plt.ylabel('Y axis')
    plt.xlabel('X axis')
    plt.show()

# Вывод результата разной природы в формате строки
def output(s):
    if type(s) == float:
        if s > 1000000:
            return '{:.8e}'.format(s)
        return '{:.8f}'.format(s)
    elif type(s) == int:
        return str(s)
    else:
        return s


def func(x, u):
    return x ** 2 + u ** 2

# Рунге-Кутта
def runge(n, h, x, y):
    y_out = []
    coeff = h / 2

    for i in range(n):
        try:
            y_out.append(y)
            y = y + h * func(x + coeff, y + coeff * func(x, y))
            x += h
        except OverflowError:
            y_out.append('overflow')
            for j in range(i, n - 1):
                y_out.append('-----')
            break
    return y_out

# Эйлер
def euler(n, h, x, y):
    y_out = []
    for i in range(n):
        try:
            y += h * func(x, y)
            y_out.append(y)
            x += h
        except OverflowError:
            y_out.append('overflow')
            for j in range(i, n - 1):
                y_out.append('-----')
            break
    return y_out

# Пикар
def picar(n, h, x, y0):
    def f1(a):
        return a ** 3 / 3

    def f2(a):
        return f1(a) + a ** 7 / 63

    def f3(a):
        return f2(a) + (a ** 11) * (2 / 2079) + (a ** 15) / 59535

    def f4(a):
        return f3(a) + (a ** 15) * (2 / 93555) + (a ** 19) * (2 / 3393495) + (a ** 19) * (2 / 2488563) + \
               (a ** 23) * (2 / 86266215) + (a ** 23) * (1 / 99411543) + (a ** 27) * (2 / 3341878155) + (a ** 31) * (
                           1 / 109876902975)

    y_out = [[y0], [y0], [y0], [y0]]
    for i in range(n - 1):
        x += h
        y_out[0].append(f1(x))
        y_out[1].append(f2(x))
        y_out[2].append(f3(x))
        y_out[3].append(f4(x))
    return y_out


def work():
    h = 10 ** -5  # 10**-5 это хороший шаг для численных методов

    x = 0
    y0 = 0
    end = 2.0

    n = ceil(abs(end - x) / h) + 1  # количество повторений

    x_arr = [x + h * i for i in range(n)]
    y1 = euler(n, h, x, y0)
    y2 = runge(n, h, x, y0)
    y3 = picar(n, h, x, y0)

    print("|    x    |   Пикара 1    |   Пикара 2    |   Пикара 3    |    Пикара 4   |    Эйлера     |  Рунге-Кутты  |")
    print("-" * 107)
    output_step = int(n / 100)  # выводим только 100 значений в таблице
    for i in range(0, n, output_step):
        print("|{:^9.5f}|{:^15.8f}|{:^15.8f}|{:^15.8f}|{:^15.8f}|{:^15s}|{:^15s}|".format(x_arr[i], y3[0][i], y3[1][i],
                                                                        y3[2][i], y3[3][i], output(y1[i]), output(y2[i])))


    x_arr2 = [x - h * i for i in range(n)]
    y12 = euler(n, h, x, y0)
    y22 = runge(n, h, x, y0)
    y32 = picar(n, -h, x, y0)

    x_arr2.reverse()
    x_arrF = x_arr2+x_arr
    (y32[0]).reverse()
    (y32[1]).reverse()
    (y32[2]).reverse()
    (y32[3]).reverse()
    y12.reverse()
    y22.reverse()

    get_graphic(x_arrF, y32[0]+y3[0], "Пикар 1")
    get_graphic(x_arrF, y32[1]+y3[1], "Пикар 2")
    get_graphic(x_arrF, y32[2]+y3[2], "Пикар 3")
    get_graphic(x_arrF, y32[3]+y3[3], "Пикар 4")
    get_graphic(x_arrF, y12+y1, "Эйлер")
    get_graphic(x_arrF, y22+y2, "Рунге-Кутта")

work()
