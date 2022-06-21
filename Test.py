import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np
import math
def drawShape(Xk: np.ndarray,numCircles: int, mult: int = 0):
    N = len(Xk)
    numSamples = mult*N
    freq = np.fft.fftfreq(N) 
    w = 2*np.pi

    Xk_zero: int = Xk[0]
    Xk_dict: list[dict] = [{'coefficents' : Xk[i], 'freq': freq[i]}  for i in range(1,len(freq))]
    Xk_dict.sort(key = lambda a: np.abs(a.get('freq')))

    xn: np.ndarray = Xk_zero*np.ones(numSamples,dtype = 'complex_')
    for n in range(numSamples):
        for k, X in enumerate(Xk_dict[0:(numCircles)]):
            xn[n] = xn[n] + X.get('coefficents')*np.exp(1j*(w*X.get('freq')*n/mult))
    return (1/N)*xn

def shapeLinearTransformation(shape : np.array, angle, pose = 0):
    shapePolar = [shape.real,shape.imag]
    A = np.array([[math.cos(angle), math.sin(angle)],\
                  [-math.sin(angle), math.cos(angle)]])
    return np.matmul(A,shapePolar) + pose

def upscaleShape(shape, mult: int = 2):
    N = shape.shape[0]
    return np.array([shape[i//mult] + (1/mult)*(i - mult*(i//mult))*(shape[(i//mult + 1)%N] - shape[i//mult]) for i in range(mult*N)])

def polar2imag(shape):
    return np.array([shape[0][i] + 1j*shape[1][i] for i in range(shape.shape[1])])

maxCircles = 40
shapeK: np.ndarray = np.transpose(np.array([[-.5,-1],[-.5,0],[-.5,1],[0,1],[0,.5],[.5,1],[1,1],[0,0],[1,-1],[.5,-1],[0,-.5],[0,-1]])) #K
shapeL: np.ndarray = np.transpose(np.array([[-1,-1],[-1,0],[-1,1],[0,1],[0,0],[1,0],[1,-1],[0,-1]])) #L

originalShape: np.ndarray = shapeL
originalShapeComplex: np.ndarray = np.array([originalShape[0][i] + 1j*originalShape[1][i] for i in range(originalShape.shape[1])])

fig, ax = plt.subplots()

lineShape, = ax.plot(originalShape[0], originalShape[1])
lineShape.set_linestyle("none")
lineShape.set_marker("o")
lineShape.set_c("orange")

lineDrawing, = ax.plot([], [])
lineDrawing.set_c("b")


plt.xlim([-3, 3])
plt.ylim([-3, 3])

plt.subplots_adjust(bottom=0.25)

axCircle = plt.axes([0.25, 0.12, 0.65, 0.03])
circlesSlider =  Slider(
    ax=axCircle,
    label='Circle',
    valmin = 0,
    valstep = 1,
    valmax = maxCircles,
    valinit = 0
)

axAngle = plt.axes([0.25, 0.08, 0.65, 0.03])
angleSlider =  Slider(
    ax=axAngle,
    label='Angle',
    valmin=0,
    valmax = 2*np.pi,
    valinit = 0
)

axRes = plt.axes([0.25, 0.04, 0.65, 0.03])
resSlider =  Slider(
    ax=axRes,
    label= 'Resolution',
    valmin= 1,
    valstep = 1,
    valmax = 20,
    valinit = 20
)

axUpscale = plt.axes([0.25, 0.0, 0.65, 0.03])
upscaleSlider =  Slider(
    ax=axUpscale,
    label= 'Upscale',
    valmin= 1,
    valstep = 1,
    valmax = 5,
    valinit = 1
)

shapeChangeAx = plt.axes([0.05, 0.1, 0.1, 0.04])
button = Button(shapeChangeAx, 'Shape', hovercolor='0.975')

def update(val):
    shapeTransformed = upscaleShape(polar2imag(shapeLinearTransformation(originalShapeComplex, angleSlider.val, 0)),upscaleSlider.val)
    newShapeComplex: np.ndarray = drawShape(np.fft.fft(shapeTransformed), circlesSlider.val, resSlider.val)

    lineDrawing.set_xdata(newShapeComplex.real)
    lineDrawing.set_ydata(newShapeComplex.imag)

    lineShape.set_xdata(shapeTransformed.real)
    lineShape.set_ydata(shapeTransformed.imag)
    circlesSlider.valmax = shapeTransformed.shape[0]


circlesSlider.on_changed(update)
angleSlider.on_changed(update)
resSlider.on_changed(update)
upscaleSlider.on_changed(update)
plt.show()