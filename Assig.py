import numpy as np
import sys
import time
import os

start_time = time.time()

# Check if the correct number of command-line arguments is provided

print(str(sys.argv[2]).split)
if len(sys.argv) != 3:
    print("Usage: python3 program_name.py input1 input2")
    print("ERROR: missing input")
    sys.exit(1)
    
if sys.argv[1] != 'all' and sys.argv[1] != 'ones' and sys.argv[1] != 'zeros':
    print("Usage: python3 program_name.py input1 input2")
    print(f"ERROR: '{sys.argv[1]}' format not accetable, please insert: 'all' or 'ones' or 'zeros'")
    sys.exit(1)
    
# Get the command-line arguments

var_for_print = sys.argv[1]
file_name = sys.argv[2]

    
# FUNZIONE PRINT FINALE

def popcount_all(n,final_result):
    
    for j in range(2 ** n): #Ciclo che scorre sulle righe
        
        x = [ 0 ] * n    #Riempie tutte le righe di 0
        
        for k in range(n):  #Ciclo che scorre sulle colonne
            
            if ((j & (1 << k)) != 0):  x[k] = 1   #Posiziona gli 1
               
        s = ""   #Creazione di una stringa vuota
        
        for k in range(n): #Ciclo che scorre sulle colonne
            
            s = s + str(x[k]) #Trasformo gli x[k] in stringhe

        if var_for_print == 'all': print(f'{s[::-1]},{final_result[j]}')
        
        if var_for_print == 'ones':
            if final_result[j]==1: print(f'{s[::-1]},{final_result[j]}')
            
        if var_for_print == 'zeros':
            if final_result[j]==0: print(f'{s[::-1]},{final_result[j]}')
            

def print_output(f):
  
    if var_for_print == 'ones':
        if f[1]==1:
            for item in f[0]:
                print(item, end='')
            print(',',f[1],sep='')
            
    if var_for_print == 'zeros':
        if f[1]==0:
            for item in f[0]:
                print(item, end='')
            print(',',f[1],sep='')
            
    if var_for_print == 'all':
        for item in f[0]:
            print(item, end='')
        print(',',f[1],sep='')
                    
# FUNZIONE LEGGERE FILE CNF

def read_cnf(file_path):
    num_vars = 0
    num_clauses = 0
    clauses = []
    clause = []
    control_line = False
    numero_linea = 0

    with open(file_path,'r') as file:
        
        for line in file:
            numero_linea += 1
            line = line.strip() #Elimina gli spazi inutili nella stringa
            
            if line.startswith('c'):
                continue
                    
            elif line.startswith('p cnf'):
                control_line = True
                num_vars , num_clauses = line.split()[2:]
                
            elif control_line == False:
                if not line.startswith('c'):
                    print('Error:Il file in input non è valido')
                    sys.exit(1)
                        
            else:
                
                for x in line.split():
                    
                    if x!='0':
                        try:
                            int(x)
                        except ValueError:
                            print('Errore: Nella linea x è presente una varibile non intera')
                            sys.exit(1)
                        clause.append(int(x))
                    else:
                        if len(clause)==0 and var_for_print == 'ones': sys.exit(1)
                        elif len(clause)==0:
                            f=[0]*2**int(num_vars)
                            popcount_all(int(num_vars),f)
                            sys.exit(1)
                        
                        clauses.append(clause)
                        clause = []
                    
                    
    if len(clause) != 0: clauses.append(clause)
    return num_vars,num_clauses,clauses
        
###############################################################
## ADD CONDIZIONE PER CUI NON CONSIDERA RIGHE CON ALTRE LETTERE
###############################################################
    
# OPERATION OR

def operation_OR(cla,bin,n):
    
    sum=0
    
    for i in cla:
        if i>0 and bin[n-i]==1: sum+=1
        elif i<0 and bin[n+i]==0: sum+=1
        if sum!=0: return 1
    
    #if np.sum(bin[i for i in cla])>0: f_OR=1
    #for i in range(len(cla)):
    
        #if (cla[i]>0 and bin[n-cla[i]] == 1) or (cla[i]<0 and bin[n+cla[i]] == 0):
        #    f_OR=1
        #    return f_OR
    return 0

# OPERATION AND

def operation_AND(cla,binary_list,n):
    for sublist in cla:
        if operation_OR(sublist,binary_list,n) == 0:
            return 0
    return 1
        
def main(n):
    for i in range(2**n):
        f = []
        binary_representation = format(i, "0" + str(n) + "b")
        binary_list = [int(bit) for bit in binary_representation]
        f.append(binary_list)
        f.append(operation_AND(clauses,binary_list,n))
        print_output(f)
    
# MAIN

n,c,clauses = read_cnf(""+str(file_name)+"")

main(int(n))

end_time = time.time()

execution_time_seconds = end_time - start_time

# Calculate the execution time in minutes
execution_time_minutes = execution_time_seconds/60


print(f"Execution time: {execution_time_minutes:.2f} minutes")
print("var="+str(n)+"", "clauses="+str(c)+"")
