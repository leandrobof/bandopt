import fitband as ft
import os
from PyGMO import *
from PyGMO.problem import base

skgen_path="/home/leandro/Documents/C++/skgen/scr/skgen"

class dftb(base):
    """
    

    
    """

    def __init__(self, dim=3):
        # First we call the constructor of the base class telling PyGMO
        # what kind of problem to expect ('dim' dimensions, 1 objective, 0 contraints etc.)
        super(dftb,self).__init__(dim,0,2)

        # We set the problem bounds (in this case equal for all components)
        self.set_bounds([0.,0.5,2.], [10.,10.,6.])

    # Reimplement the virtual method that defines the objective function.
    def _objfun_impl(self, x):

        # Compute the sphere function
        try:
            os.remove("W-W.skf")
        except OSError:
            pass

        f=open("test","w")
        f.write("Atoms\nW basis={"+str(x[0])+" "+str(x[1])+" "+str(x[2])+"} \n/")
        f.close()
        os.system(skgen_path+" test >tmp.log ")
        os.system("sed -i \'s/Udd  Upp  Uss/0.  0. 0./\' W-W.skf")
        os.system("sed -i 's/-0.0473147/0.040/' W-W.skf")
 
        f1=ft.band("wbandqe.dat","bulk",4,-3,1,-4)
        f2=ft.band("w_fcc_qe_band.dat","bulk2",4,-3,1,-4)
        #*******************************************************************************     
   
        print x
        print f1,f2
        return (f1,f2)

        # Note that we return a tuple with one element only. In PyGMO the objective functions
        # return tuples so that multi-objective optimization is also possible.
        

    # Finally we also reimplement a virtual method that adds some output to the __repr__ method
    def human_readable_extra(self):
        return "\n\t Problem dimension: " + str(self.__dim)

#f=open("param_mo","w")
prob = dftb(dim = 3)
pop = population(prob,12)



algo = algorithm.nsga_II(gen = 10)


"""
pop.plot_pareto_fronts()
plt.show()
plt.savefig('mo_parameter_inicial.png')
"""
pop = algo.evolve(pop)

pop.plot_pareto_fronts()

plt.savefig('mo_parameter_final.png')
plt.show()


individuos=[ind.cur_x for ind in pop]
fit=[ind.cur_f for ind in pop]

f=open("param_mo","w")


f.write(str(pop.compute_pareto_fronts()))
f.write("\n\n")
for i in range(len(individuos)):
    f.write(str(individuos[i])+"    "+str(fit[i])+"\n")

f.close()





   
