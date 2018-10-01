""" Preamble """
import numpy
import numpy.random as np
import matplotlib.pyplot as plt
import math

""" Initialization """
N_pop = 100000 #Population size
cell_num=numpy.array([4*10**5, 2*10**6, 10**7, 5*10**7, 2.5*10**8, 1.25*10**9, 6.25*10**9, 3.125*10**10, 1.5625*10**11, 7.8125*10**11, 3.90625*10**12, 1.953125*10**13])   #Stem cell carrying capacity
p = 2*10**-8  #Mutation probability

growth_rate=numpy.array(np.normal (0.2, 3.5, N_pop))
increment=numpy.arange (0, 0.9, 0.001)


ndiv=10 #Number of cell divisions per year
age=90 #Lifespan
time=ndiv*age #Duration of the simulation
age_rate=numpy.zeros((19)) #Age-specific rates adjusted to the US 2000 standard population
wts=[0.013818048555027355, 0.0553159434123515, 0.07253241028642805, 0.07303103455912367, 0.07216711636515384, 0.06647847243710951, 0.06452984736662379, 0.07104508339877749, 0.08076197744193335, 0.08185169462960405, 0.07211714069611326, 0.06271758577923968, 0.048454493422914295, 0.038794489715138394, 0.034263609991378986, 0.03177168658747205, 0.026997999757072733, 0.017842803104216928, 0.01550856249432107] #Weights from the US 2000 standard population
g_initial=[0]*age
increment = 0.1*((increment-1)**9) #Linear increasing function

""" Main simulation """
##for n in cell_num:
n = 10**7
cancer_count=[0]*age #Age-wise incidence of cancer
num_surv=[0]*age #Number of survivors in each age/generation
cancer_fract=[0]*age #Normalized incidence of cancer
cumul_count=[0]*age #Cumulative count of cancer
crude_rate=[0]*age #Calculated age-wise cancer incidence per 100000

for j in range ( 0, N_pop ):
    g_time = [growth_rate[j]]*time
    g_time += increment #Effect of age at each step
    t = 0 #Index to track time
    n_mut = [0]*time
    m = 0 #Initial mutant population
    p_mut = 1-((1-p)**n) #Initial probabiltiy of first mutation arising in the population
     
    for t in range(0, time):
        
        n_mut[t]=n_mut[t-1]
        g = g_time[t]

        #Negative growth is physiologically undefined and mathematically unbounded
        if p_mut > np.random_sample() and g > 0: #New mutant population
            m=1
            n_mut[t]+=1
            p_mut=1-((1-p)**m)
        elif n_mut[t-1 or t] > 0 and g > 0: #Growth of existing mutant or normal population, as the case may be
            m_inc = math.copysign(1.0, g)*math.fabs(m*g*(1-(m/n)))
            m += 0.017*m_inc #This multiplicative factor is part of the growth rate determination that adds on to the distribution; a measure for convenience
            p_mut=1-((1-p)**m)
        elif g < 0:
            pass

        if n_mut[t] == 5: #Recording actual cancer cases
            cancer_count[int(t/ndiv)] += 1
            g_initial[int(t/ndiv)] = g
            break

""" Calculations """
num_surv[0]=N_pop
for t in range(1, age):
    num_surv[t]=num_surv[t-1]-cancer_count[t-1] #Number of individuals surviving at given age
    cumul_count[t]=cumul_count[t-1] + cancer_count[t]

t=0
while (t <= (age-1) and num_surv[t] != 0 ):
    cancer_fract[t]=cancer_count[t] / (cancer_count[t]+num_surv[t]) #Fraction of surviving population getting cancer
    crude_rate[t]=cancer_fract[t]*100000
    t+=1

age_rate[0]=crude_rate[0]
age_rate[1]=sum(crude_rate[1:4])
age_rate[-1]=sum(crude_rate[85:len(crude_rate)])
for i in range(2,18):
    age_rate[i]=sum(crude_rate[(5*(i-1)):(5*(i-1)+4)])

wtd_rate=wts*age_rate #Age adjusted rate calculation-weighted sum of age-specific rates
total_inc = sum(wtd_rate)