a,b,c = map(float, input().split())
x1=x2=D=0
if b**2 - 4*a*c >= 0:
    D = b**2 - 4*a*c
    x1 = (-b + D**0.5) / (2*a)
    x2 = (-b - D**0.5) / (2*a)
    print('x1 =' ,x1, 'x2 =', x2)
else:
    print('Нет корней')
