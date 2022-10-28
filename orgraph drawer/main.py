# предупреждаю перед прочтением кода: код говно
from PIL import Image, ImageDraw
from math import sqrt, atan, atan2, sin, cos, degrees, radians, floor


SCALE = 666

DOTR = SCALE//30
LOOPR = SCALE//10
ARCR = sqrt(5*SCALE**2)
LINEWIDTH = SCALE*3//200

ARROWANGLE = 13
ARROWINDENT = SCALE//13
ARROWLENGTH = SCALE//10
ARROWALONGATION = 1.2

LOOPARROWINDENT = 10
LOOPARROWANGLE = ARROWANGLE+5
LOOPARROWLENGTH = 50
LOOPARROWFROTATION = 1.05
LOOPARROWBROTATION = 0.91

ARCARROWINDENT = 1.9
ARCARROWLENGTH = 2.5
ARCARROWFROTATION = 0.9975
ARCARROWBROTATION = 0.9975

def create_arrow(ax1, ay1, ax2, ay2, aangle):
    angle = degrees(atan2(ay2-ay1, ax2-ax1))
    rangle, langle = radians(angle-aangle), radians(angle+aangle)
    l = sqrt((ax1-ax2)**2 + (ay1-ay2)**2) * ARROWALONGATION
    axr, ayr = ax1+l*cos(rangle), ay1+l*sin(rangle)
    axl, ayl = ax1+l*cos(langle), ay1+l*sin(langle)
    return axr, ayr, axl, ayl

def draw_graph(x: int, y: int, matrix: list[list[int]], draw: ImageDraw.ImageDraw):
    dots =  [[x, y],       [x+SCALE, y],       [x+2*SCALE, y],
             [x, y+SCALE], [x+SCALE, y+SCALE], [x+2*SCALE, y+SCALE]]
    loops_rotation = [[-1, -1], [0, -1], [1, -1],
                      [-1,  1], [0,  1], [1,  1]]
    n = len(matrix)

    for dot in range(n):
        draw.ellipse([(dots[dot][0]-DOTR, dots[dot][1]-DOTR), (dots[dot][0]+DOTR, dots[dot][1]+DOTR)], "black")

    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                if i == j:
                    x, y = dots[i]
                    t = LOOPR/(sqrt(2) if i not in (1, 4) else 1)
                    cx = x+t*loops_rotation[i][0]
                    cy = y+t*loops_rotation[i][1]
                    draw.ellipse([(cx-LOOPR, cy-LOOPR), (cx+LOOPR, cy+LOOPR)], None, "black", LINEWIDTH)

                    angle = atan2(y-cy, x-cx)
                    angle -= radians(LOOPARROWINDENT)
                    ax1, ay1 = cx+LOOPR*cos(angle)*LOOPARROWFROTATION, cy+LOOPR*sin(angle)*LOOPARROWFROTATION
                    angle -= radians(LOOPARROWLENGTH)
                    ax2, ay2 = cx+LOOPR*cos(angle)*LOOPARROWBROTATION, cy+LOOPR*sin(angle)*LOOPARROWBROTATION

                    axr, ayr, axl, ayl = create_arrow(ax1, ay1, ax2, ay2, LOOPARROWANGLE)

                    draw.polygon([(ax1, ay1), (axr, ayr), (ax2, ay2), (axl, ayl)], "black", "black", LINEWIDTH)
                elif i in (0, 2) and j in (0, 2) or i in (3, 5) and j in (3, 5):
                    top = i in (0, 2)
                    dot = dots[4 if top else 1]
                    x, y = dot[0], dot[1]+(SCALE if top else -SCALE)
                    if top:
                        fangle = -degrees(atan(2))
                        sangle = -fangle-180
                    else:
                        sangle = degrees(atan(2))
                        fangle = -sangle+180

                    xs, ys, xf, yf = *dots[i], *dots[j]
                    angle = radians(fangle if i < j else sangle)
                    angle += radians(ARCARROWINDENT)*(-1 if i < j else 1)
                    ax1, ay1 = x+ARCR*ARCARROWFROTATION*cos(angle), y+ARCR*ARCARROWFROTATION*sin(angle)
                    angle += radians(ARCARROWLENGTH)*(-1 if i < j else 1)
                    ax2, ay2 = x+ARCR*ARCARROWBROTATION*cos(angle), y+ARCR*ARCARROWBROTATION*sin(angle)
                    if i < j:
                        fangle = degrees(angle)
                        if matrix[j][i]: sangle = 180+degrees(angle)*(1 if top else -1)
                    else:
                        sangle = degrees(angle)
                        if matrix[j][i]: fangle = 180+degrees(angle)*(1 if top else -1)

                    axr, ayr, axl, ayl = create_arrow(ax1, ay1, ax2, ay2, ARROWANGLE)

                    draw.arc([(x-ARCR, y-ARCR), (x+ARCR, y+ARCR)], sangle, fangle, "black", LINEWIDTH)
                    draw.polygon([(ax1, ay1), (axr, ayr), (ax2, ay2), (axl, ayl)], "black", "black", 1)
                else:
                    xs, ys, xf, yf = *dots[i], *dots[j]
                    angle = atan2(ys-yf, xs-xf)
                    if matrix[j][i]:
                        xs -= (ARROWINDENT+ARROWLENGTH)*cos(angle)
                        ys -= (ARROWINDENT+ARROWLENGTH)*sin(angle)
                    ax1, ay1 = xf+ARROWINDENT*cos(angle), yf+ARROWINDENT*sin(angle)
                    angle = atan2(ys-ay1, xs-ax1)
                    ax2, ay2 = ax1+ARROWLENGTH*cos(angle), ay1+ARROWLENGTH*sin(angle)

                    axr, ayr, axl, ayl = create_arrow(ax1, ay1, ax2, ay2, ARROWANGLE)

                    draw.line([(xs, ys), (ax2, ay2)], "black", LINEWIDTH)
                    draw.polygon([(ax1, ay1), (axr, ayr), (ax2, ay2), (axl, ayl)], "black", "black", 1)


matrixes = []
i = 0
lines = open("matrixes.txt", 'r', encoding="utf-8").readlines()
while i < len(lines):
    n = int(lines[i]); i += 1
    matrixes.append([[int(i) for i in vector.split()] for vector in lines[i:i+n]])
    i += n

WIDTH = floor(2.5*SCALE)
HEIGHT = floor(1.5*SCALE)
for i in range(15):
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    img_draw = ImageDraw.Draw(img)
    draw_graph(0.25*SCALE, 0.25*SCALE, matrixes[i], img_draw)
    img.save(open(f"{i+1}.png", 'wb'), "PNG")
