from mpi4py import MPI
import time

def f(x):
    return x*x*x*x

def Trap(a,b,n,h):
    integral =((a) + f(b))/2.0

    x=a 
    for i in range(1,int(n)):
        x = x+h  ##1er loop del proceso 0 x=0,00097...
        integral = integral + f(x) ##1er loop del proceso 0 integral 0,027....
    
    return integral*h

tic = time.perf_counter()
comm = MPI.COMM_WORLD #comunicación punto a punto
my_rank = comm.Get_rank()
p = comm.Get_size()

a=0.0
b=1.0
n=99999
dest=0
total=1.0

h = (b-a)/n
local_n = n/p

local_a = a + my_rank*local_n*h
local_b = local_a + local_n*h
integral = Trap(local_a, local_b, local_n, h)

if my_rank == 0:
    total = integral
    for source in range (1,p):
        integral = comm.recv(source=source)
        print("Proceso ", my_rank, "<-", source, ",", integral,"\n")
        total = total + integral

    toc=time.perf_counter()

    print(f"tiempo de ejecución: {toc - tic:0.4f} segundos")
else:
##    print("Proceso ", my_rank, "->", dest, ",", integral,"\n")
    comm.send(integral, dest=0) 

if(my_rank == 0):
    print("Con n=", n," trapezoides, \n")
    print("integral definida desde", a, "hasta", b, "=", total,"\n")

