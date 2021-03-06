from scipy import optimize
import numpy
import matplotlib.pyplot as plt
import inspect

def gaus1d_function(x,p0,p1,p2,p3): return p0*numpy.exp(-((x-p1)/p2)**2)+p3
def exp_function(x,p0,p1,p2): return p0*numpy.exp(-(x)/p1)+p2
def sine_function(x,p0,p1,p2,p3): return p0*numpy.sin(p1*x*numpy.pi*2-p2)+p3
def expsine_function(x,p0,p1,p2,p3,p4): return p0*numpy.sin(p1*x*numpy.pi*2-p2)*numpy.exp(-x*p3)+p4
def temperature_function(x,p0,p1): return (p0**2+13.85e-6*1e8*2*p1*x**2)**0.5

def fit_function(p,data,function):
    # Chekck the length of p
    pLen = len(inspect.getargspec(function)[0])-1
    p0 = p[0:pLen]
    
    datax=data[:,0]
    datay=data[:,1]	   
    pfit, pvariance = optimize.curve_fit(function,datax,datay,p0)
    error=[]
    for i in range(len(pfit)):
        error.append(pvariance[i][i]**0.5)
    
    error = numpy.append(numpy.array(error),numpy.zeros(5-len(p0))).reshape(5,1)
    
    # Return same length of pfit
    pfit = numpy.append(pfit,numpy.zeros(5-len(p0))).reshape(5,1)
    
    return pfit,error

def plot_function(p,datax,function):

    # Chekck the length of p
    pLen = len(inspect.getargspec(function)[0])-1
    p0 = p[0:pLen]
    x = numpy.linspace(numpy.min(datax), numpy.max(datax), 100)
    y = numpy.array([function(i,*p0) for i in x])
    return x, y

def test_function(p,function):
	# generate random data
	ax=numpy.linspace(0,1000,100)
	x,dat = plot_function( p, ax, function)
	ay = numpy.array(dat)
	noise = 1*numpy.random.rand(100)-1
	noisydat = ay+noise-1
	# fit noisy data, starting from a random p0
	p0 = p + numpy.random.rand(len(p))-1
	pFit , error = fit_function( p0, numpy.transpose(numpy.array((ax,noisydat))),function)
	# Get a plot of the fit results
	fitX, fitY = plot_function(pFit,numpy.transpose(numpy.array((ax,noisydat))),function)
	# Show the plot on screen 
	plt.plot(ax, noisydat,'.')
	plt.plot(fitX,fitY,'-')
	plt.show()
	
if __name__ == "__main__":
	print ""
	print "------ Testing fitlibrary.py ------"
	print ""

	test_function([100,1e7],temperature_function)



    
