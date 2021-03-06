" Import of modules "
import numpy.random as np
import xlsxwriter

" Initialization "
prob = [0] * 5 #Range of mutational probabilities
a = len ( prob )
for i in range ( 0, a ):
    prob [i] = 10 ** -(i+4)

growth_rate = [0] * 20 #Range of growth rates
b = len ( growth_rate )
for i in range ( 0, b ):
    growth_rate [i] = 0.25 * (i+1)

mut_pop = [ [0 for i in range ( 0, b )] for j in range ( 0, a ) ] #Threshold values for mutant population sizes
product = [ [0 for i in range ( 0, b )] for j in range ( 0, a ) ] #Product of p and mut_pop will be stored here
mutant_prev = [ [0 for i in range ( 0, b )] for j in range ( 0, a ) ] #Size of mutant population at the step preceding transition

iter_num = 100 #Number of iterations for the entire simuation
n = 8 * 10 ** 9 #Stem cell carrying capacity for the tissue

" Main simulation "

for i in range ( 0,a ):
    p = prob [i]
    
    for j in range ( 0, b ):
        g = growth_rate [j]
        time = 100 #Duration of each simulation
        
        for x in range ( 0, iter_num ):
            t = 0 #Index to track time
            n_mut = [0] * time
            m = 0 #Initial mutant population
            g_total = 0 #Total number of mutant cells with a particular set of mutations
            m_prev = 0 #Number of cells in the previous step
            m_hold = 0 #Holding variable for previous population size
            avg = 0 #Average mutant population size per mutation
            p_mut  = 1 - ( (1-p) ** n ) #Initial probabiltiy of first mutation arising in the population

            if p_mut > np.random_sample ( ): #At t = 0
                n_mut [0] += 1
                m = 1
            else:
                m = 0

            for t in range ( 1, time ): #From t = 1 to end of time
                n_mut [t] = n_mut [t-1]
                m_hold = m
                m += ( ( m*g ) * ( 1 -  ( m/n ) ) )
                p_mut = 1 - ( (1-p) ** m )

                if p_mut > np.random_sample ( ):
                    n_mut [t] += 1
                    m_prev += m_hold
                    g_total += m
                    m = 1
            
            den = n_mut [time-1] - 1 #Number of mutations - 1 = number of transitions between subsequent mutant populations
            avg = g_total / den #Average mutant population size per iteration
            m_prev = m_prev / den
            mut_pop [i][j] += avg / iter_num #Average mutant population size over all iterations
            mutant_prev [i][j] += m_prev / iter_num

" Calculation of the product, p * mut_pop "
for i in range ( 0, a ):
    for j in range ( 0, b ):
        product [i][j] = prob [i] * mutant_prev [i][j]

""" Export to Excel """
workbook = xlsxwriter.Workbook ( 'Model.xlsx' )
worksheet = workbook.add_worksheet ( )
row = 0
col = 0

for i in range ( 0, a ):
    for j in range ( 0, b ):
        worksheet.write ( row, col, mut_pop [i][j] )
        worksheet.write ( row + 7, col, mutant_prev [i][j] )
        col += 1
    row += 1
    col = 0

workbook.close ( )
        

        
        
            
        
