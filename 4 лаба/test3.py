from matplotlib import pyplot as plt

"""
Описание функции: определение границы, за которую точка выходит
"""


def edgeCode(x, y, yEdge, xEdge):
    code = 0
    if x < xEdge[0]:
        code = code | 1
    if x > xEdge[1]:
        code = code | 2
    if y < yEdge[0]:
        code = code | 4
    if y > yEdge[1]:
        code = code | 8
    return code


"""
 Описание функции: cohenSotherland 
 параметр: pointX: коллекция точки X
                       pointY: набор точки Y
                       yEdge: верхняя и нижняя граница
                       xEdge: левая и правая граница
                       pic: изображение
"""


def cohenSurtherland(xEdge, yEdge, pointX, pointY, pic):
    # Граница
    mid = 0
    leftEdge = 1
    rightEdege = 2
    bottomEdge = 4
    topEdge = 8

    pointX.append(pointX[0])
    pointY.append(pointY[0])

    for i in range(len(pointX)-1):

        time = 0  # Используется для определения, когда сегмент линии полностью выходит за пределы

        x0 = pointX[i]
        y0 = pointY[i]
        x1 = pointX[i+1]
        y1 = pointY[i+1]

        code0 = edgeCode(x0, y0, xEdge, yEdge)
        code1 = edgeCode(x1, y1, xEdge, yEdge)
        while True:
            if not (code0 | code1):  # Сегмент линии внутри
                pic.plot([x0, x1], [y0, y1], c='r')
                break
            elif (code0 & code1 or time > 3):  # Сегменты линии находятся снаружи
                break
            else:
                if (x1 != x0):
                    k = (y1 - y0) / (x1 - x0)
                    dk = 1/k  # k взаимно
                else:
                    dk = 0
                # Определить, какая конечная точка находится за пределами
                if code0:
                    codeout = code0
                    temp = 0
                else:
                    codeout = code1
                    temp = 1
                # Определить направление выхода за пределы и обновить точку
                if codeout & leftEdge:
                    y = pointY[i+temp]+k*(xEdge[0]-pointX[i+temp])
                    x = xEdge[0]
                elif codeout & rightEdege:
                    y = pointY[i+temp]+k*(xEdge[1]-pointX[i+temp])
                    x = xEdge[1]
                if codeout & topEdge:
                    x = pointX[i+temp]+dk*(yEdge[1]-pointY[i+temp])
                    y = yEdge[1]
                elif codeout & bottomEdge:
                    x = pointX[i+temp]+dk*(yEdge[0]-pointY[i+temp])
                    y = yEdge[0]
                if temp:
                    x1 = x
                    y1 = y
                    code1 = edgeCode(x1, y1, xEdge, yEdge)
                else:
                    x0 = x
                    y0 = y
                    code0 = edgeCode(x0, y0, xEdge, yEdge)
                time += 1


def tes(ax2):
    a = 8
    b = 0
    print(a | b)


if __name__ == '__main__':
    # Левая и правая нижняя и верхняя граница
    xEdge = [10, 30]
    yEdge = [10, 30]
    #
    pointX = [0, 40]
    pointY = [10, 30]

    pic0 = plt.subplot(1, 2, 1)
    pic0.axis([0, 50, 0, 50])
    pic0.plot([10, 30, 30, 10, 10], [10, 10, 30, 30, 10])
    pic0.plot(pointX, pointY, c='r')

    pic1 = plt.subplot(1, 2, 2)
    pic1.axis([0, 50, 0, 50])
    pic1.plot([10, 30, 30, 10, 10], [10, 10, 30, 30, 10])

    cohenSurtherland(xEdge, yEdge, pointX, pointY, pic1)

    plt.show()
