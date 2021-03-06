""" pyrho -
    a python package for reduced density matrix techniques
"""

import numpy as np
from pyrho.lib import const, utils

class Hybrid(object):
    """A generic split-spectral-density "hybrid" dynamics class
    """

    def __init__(self, hamiltonian, dynamics_slow, dynamics_fast, omega_split=None, use_PD=False):
        """Initialize the Hybrid class

        Parameters
        ----------
        hamiltonian : Hamiltonian
            An instance of the pyrho Hamiltonian class.

        """

        raise NotImplementedError

        utils.print_banner("PERFORMING RDM DYNAMICS WITH HYBRID METHOD")
        self.ham = hamiltonian
        self.dynamics_slow = dynamics_slow
        self.dynamics_fast = dynamics_fast
        self.omega_split = omega_split
        self.use_PD = use_PD
        self.setup()

    def setup(self):
        if self.omega_split is None:
            # Determine splitting frequency
            self.omega_split = []
            if self.ham.nsite == 2:
                omega_R = rabi_two_level(self.ham.sys)
            else:
                print("Automated splitting frequency for Nsys > 2 not implemented!")
                raise SystemExit

            for n in range(self.ham.nbath):
                self.omega_split.append( omega_R/4. )

                print("\n--- Splitting energy for bath %d = %0.2lf"%(
                                n, const.hbar*self.omega_split[n] ))

        else:
            assert( len(self.omega_split) == self.ham.nbath )

        for n in range(self.ham.nbath):
            Jslow, Jfast = partition_specdens(self.ham.sd[n].J, self.omega_split[n], self.use_PD)
            self.dynamics_slow.ham.sd[n].J, self.dynamics_fast.ham.sd[n].J = Jslow, Jfast

    def propagate(self, rho_0, t_init, t_final, dt):
        return self.dynamics_slow.propagate(rho_0, t_init, t_final, dt, 
                                            dynamics=self.dynamics_fast) 


def switching(omega, omega_split):
    '''Switching function that switches smoothly from 1 (at omega=0) 
    to 0 (at omega=omega_split)
    '''
    if abs(omega) < omega_split:
        return (1 - (omega/omega_split)**2)**2
    else:
        return 0.0

def partition_specdens(J, omega_split, use_PD):
    def Jfast(omega):
        if use_PD:
            pure_dephasing = J(omega)*(abs(omega) < 1e-4)
        else:
            pure_dephasing = 0.
        return (1-switching(omega,omega_split))*J(omega) + pure_dephasing
    def Jslow(omega):
        return switching(omega,omega_split)*J(omega)

    return Jslow, Jfast

def rabi_two_level(ham):
    return 2*np.sqrt( (ham[0,0]-ham[1,1])**2/4.0 + ham[0,1]**2 )/const.hbar
    # from pyrho import hybrid
    # rabi = hybrid.rabi_two_level(ham[1:,1:])
    # omega_split = []
    # for n in range(nbath):
    #    omega_split.append( max(rabi/4.,omega_c) )
    # hybrid.Hybrid( ..., omega_split = omega_split)

