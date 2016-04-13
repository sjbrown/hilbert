from pyprocessing import *
#from prettyprint import pprint
from functools import partial

size(520+20,620+20)
#background(60,60,80)
background(0,0,0)

debug = 0

posx = 0
posy = 0

xunit = 20
yunit = 20
origxunit = 20
origyunit = 20

lum = 255
sw = 1

vert = 'vert'
horiz = 'horiz'

count = 1
shap = None


def unitline(posx, posy, direction):
    if direction == vert:
        unitlinevert(posx, posy)

def unitlinevert(posx, posy):
    line( posx, posy, posx, posy+yunit)

def unitlinehoriz(posx, posy):
    line( posx, posy, posx+xunit, posy)

def shape1(posx, posy):
    global lum, sw, count
    print count, posx, posy
    #if count < 2:
    unitlinevert(posx, posy)
    unitlinehoriz(posx, posy+yunit)
    #ellipseMode(CENTER)
    #ellipse(posx + xunit/2, posy + yunit/2, 2,2)
    #text(str(count), posx+xunit/2, posy+yunit/2)
    if debug:
        text(str(count), posx, posy)
        lum -= 10
        lum %= 255
        stroke(lum)
        sw -= 1
        if sw == 0:
            sw = 8
        strokeWeight(sw)
    count += 1

def shape2(posx, posy):
    global lum, sw, count
    unitlinevert(posx+xunit, posy)
    stroke(200)
    unitlinevert((posx+xunit)-1, posy)
    stroke(100)
    unitlinevert((posx+xunit)-2, posy)
    stroke(255)
    unitlinehoriz(posx, posy+yunit)
    count += 1

def shape3(posx, posy):
    global count
    stroke(255)
    unitlinevert(posx, posy)
    unitlinehoriz(posx, posy)
    count += 1

def shape_feather(posx, posy):
    global lum, sw, count
    unitlinevert(posx+(xunit/2), posy)
    stroke(200)
    unitlinevert((posx+xunit)-1, posy+yunit)
    stroke(100)
    unitlinevert((posx+xunit)-2, posy)
    stroke(255)
    unitlinehoriz(posx, posy+yunit)
    count += 1

reddish = [255,10,10, 255]
bluish = [0,0,255, 200]
greenish = [0,255,0, 200]
rectMode(CENTER)
def shape_gasm(posx, posy):
    global lum, sw, count, reddish
    unitlinevert(posx+(xunit/2), posy)
    stroke(200)

    fill(*reddish)
    rect(posx, posy, 15, 9)
    reddish[0] = reddish[0]-12
    reddish[0] %= 255

    fill(*bluish)
    stroke(0)
    rect(posx+xunit/2, posy, xunit/2, 9)
    bluish[0] = bluish[0]-12
    bluish[0] %= 255
    bluish[1] = bluish[1]+19
    bluish[1] %= 255

    fill(*greenish)
    stroke(0)
    rect(posx-xunit/2, posy, xunit/2, 9)
    greenish[0] = greenish[0]-12
    greenish[0] %= 255
    greenish[2] = greenish[2]+19
    greenish[2] %= 255

    fill(255)
    rect(posx, posy, 5, 5)

    stroke(100)
    unitlinevert((posx+xunit)-2, posy)
    stroke(255)
    unitlinehoriz(posx, posy+yunit)
    count += 1

def hilbert(posx, posy, depth=0):
    global yunit
    global xunit

    scal = 2**depth
    yunit = origyunit * scal
    xunit = origxunit * scal
    if depth == 0:
        shp = shap
    else:
        shp = partial(hilbert, depth=depth-1)

    posx=0
    posy=0

    #print ' '*depth, 'drawing', shp, xunit, yunit, 'at norm'
    #printMatrix()
    shp(posx, posy)

    pushMatrix()
    translate(xunit*scal, 0)
    #print ' '*depth, 'drawing', shp, 'over one'
    #printMatrix()
    shp(posx, posy)
    popMatrix()

    pushMatrix()
    translate(xunit*scal, yunit*scal)
    rotate(HALF_PI)
    #print ' '*depth, 'drawing', shp, 'below and rotated'
    #printMatrix()

    shp(posx, posy)
    popMatrix()

    pushMatrix()
    # positive x strokes should be turned into positive y strokes and vice versa
    translate(xunit*scal+1, yunit*scal-1)
    rotate(HALF_PI)
    applyMatrix(1.0, 0.0, 1.0, 1.0,
                0.0, -1.0, 1.0, 1.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0)
    #print ' '*depth, 'drawing', shp, 'mirrored', yunit
    shp(posx, posy)

    popMatrix()

def setup():
    global shap
    # Change this to the different functions
    #shap = shape3
    #shap = shape_feather
    shap = shape_gasm

    if debug:
        stroke(255,0,0)
        strokeWeight(1)
        line(10,10, 350, 10)
        line(10,10, 10, 350)

    stroke(lum)
    strokeWeight(sw)

def draw():
    pushMatrix()
    translate(70,50)

    depth = 3
    hilbert(0,0,depth)

    popMatrix()
    save('/tmp/hilbert_%s_%s.png' % (shap.__name__, depth))
    import time; time.sleep(1)


run()

