import sys
import math
import random as rng

def bernoulli(nVal,args):
	X = []
	if len(args) != 1: sys.exit('Incorrect number of arguments')
	p = float(args[0])	
	if p < 0.0 or p > 1.0: sys.exit('Incorrect probability value : '+str(p))
	for i in range(nVal):
		if rng.random() <= p:
			X.append(1)
		else:
			X.append(0)
	return X

def binomial(nVal, args):
	X = []
	if len(args) != 2: sys.exit('Incorrect number of arguments')
	n = int(args[0])
	p = float(args[1])
	if p < 0.0 or p > 1.0: sys.exit('Incorrect probability value : '+str(p))
	for i in range(nVal):
		nS = 0
		for j in range(n):
			if rng.random() <= p:
				nS = nS + 1
		X.append(nS)
	return X

def geometric(nVal, args):
	X = []
	if len(args) != 1: sys.exit('Incorrect number of arguments')
	p = float(args[0])	
	if p < 0.0 or p > 1.0: sys.exit('Incorrect probability value : '+str(p))
	for i in range(nVal):
		t = 1
		while rng.random() > p:
			t = t + 1
		X.append(t)
	return X

def negBinomial(nVal, args):
	X = []
	if len(args) != 2: sys.exit('Incorrect number of arguments')
	k = int(args[0])
	p = args[1:len(args)]
	for i in range(nVal):
		X.append(sum(geometric(k,p)))
	return X

def poisson(nVal, args):
	X = []
	if len(args) != 1: sys.exit('Incorrect number of arguments')
	lda = float(args[0])
	for i in range(nVal):
		k = 0
		u = rng.random()
		while u >= math.exp((0.0-lda)):
			k = k + 1
			u = u * rng.random()
		X.append(k)
	return X

def cdfDisc(p):
	F = []
	for i in range(len(p)):
		F.append(sum(p[0:i+1]))
	return F

def arbDiscrete(nVal,args):
	X = []
	p = []
	for v in args:
		p.append(float(v))
	F = cdfDisc(p)
	if F[-1] != 1: sys.exit('Probabilites need to add up 1')
	for i in range(nVal):
		t = 0
		u = rng.random()
		while  F[t] <= u:
			t = t + 1
		X.append(t)
	return X

def uniform(nVal, args):
	X = []
	if len(args) != 2: sys.exit('Incorrect number of arguments')
	a = float(args[0])
	b = float(args[1])
	if a>b:
		t = a;
		a = b;
		b = t;
	for i in range(nVal):
		X.append(a+((b-a)*rng.random()))
	return X

def exponential(nVal, args):
	X = []
	if len(args) != 1: sys.exit('Incorrect number of arguments')
	lda = float(args[0])
	for i in range(nVal):
		X.append((0-(1/lda))*math.log(1-rng.random()))
	return X

def gamma(nVal, args):
	X = []
	if len(args) != 2: sys.exit('Incorrect number of arguments')
	alp  = int(args[0])
	lda = args[1:len(args)]
	for i in range(nVal):
		X.append(sum(exponential(alp,lda)))
	return X

def normal(nVal, args):
	X = []
	if len(args) != 2: sys.exit('Incorrect number of arguments')
	nVal2 = int(math.ceil(float(nVal)/2))
	mu = float(args[0])
	sd = float(args[1])
	for i in range(nVal2):
		u1 = rng.random()
		u2 = rng.random()
		z1 = math.sqrt((0-2)*math.log(u1))*math.cos(2*math.pi*u2)
		z2 = math.sqrt((0-2)*math.log(u1))*math.sin(2*math.pi*u2)
		X.append(mu + z1 * sd)
		X.append(mu + z1 * sd)
	if nVal % 2 == 0:
		return X
	else:
		return X[0:len(X)-1]

def sMean(smpl):
	return (float(sum(smpl))/float(len(smpl)))

def sVar(smpl, mean):
	t = 0.0
	for i in smpl:
		t = t + float((i - mean)*(i - mean))
	if len(smpl) == 1:
		return t
	return t/float(len(smpl)-1)
	
def main(argv):
	try:		 
		rng.seed(8) #set seed of random number generator
		nVal = int(argv[1])
		args = argv[3:len(argv)]
		if argv[2].lower() == 'bernoulli':
			res = bernoulli(nVal, args)
		elif argv[2].lower() == 'binomial':
			res = binomial(nVal, args)
		elif argv[2].lower() == 'geometric':
			res = geometric(nVal, args)
		elif argv[2].lower() == 'neg-binomial':
			res = negBinomial(nVal, args)
		elif argv[2].lower() == 'poisson':
			res = poisson(nVal, args)
		elif argv[2].lower() == 'arb-discrete':
			res = arbDiscrete(nVal, args)
		elif argv[2].lower() == 'uniform':
			res = uniform(nVal, args)
		elif argv[2].lower() == 'exponential':
			res = exponential(nVal, args)
		elif argv[2].lower() == 'gamma':
			res = gamma(nVal, args)
		elif argv[2].lower() == 'normal':
			res = normal(nVal, args)
		else:
			sys.exit('Distribution ' + argv[2] + ' is not supported')
		print 'Values: ' + str(res)
		mean = sMean(res)
		print '\nSample Mean: ' + str(mean) #This is just here to verify the values. For large number of samples this value should be similar to what the you get from the parameters
		print 'Sample Variance: '+ str(sVar(res, mean)) #This is just here to verify the values. For large number of samples this value should be similar to what the you get from the parameters
	except ValueError:
		print 'Incorrect number format'

if __name__ == '__main__':
	main(sys.argv)