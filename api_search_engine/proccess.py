class MyEx(Exception):

    def __init__(self, message, data):
        self.message = message
        self.data = data




def calcular(a, b):
    if a + b == 4:
        a = MyEx('falha', [2, 3, 4,])
        raise a
    else:
        print("safe")


if __name__ == '__main__':
    try:
        calcular(2, 2)
    except Exception as e:
        print(e)