__all__ = ['MolDB']


# standard library
import re


# dependent packages
import radico as ra
import xarray as xr

# module constants


# classes
class MolDB:
    def __init__(self):
        pass

    @classmethod
    def from_cdms(cls, filename):
        pass

    @classmethod
    def from_lamda(cls, filename):
        pass

    def einstein_Aul(self, transition):
        pass
    
    def einstein_Bul(self, transition):
        pass
    
    def einstein_Blu(self, transition):
        pass
    
    def collision_Cul(self, transition, n_col, T_kin):
        pass
    
    def collition_Clu(self, transition, n_col, T_kin):
        pass
    
    def n_crit(self, transition, T_kin):
        pass
    
    def Q(self, T_ex):
        pass


# functions
def db_cdms(filename):
    pass


def db_lamda(filename):
    with ra.open_lamda(filename) as f:
        ra.read_until(f, '^!')
        name = next(f).strip()

        ra.read_until(f, '^!')
        weight = float(next(f).strip())

        ra.read_until(f, '^!')
        n_levels = int(next(f))

        ra.read_until(f, '^!')
        levels = ra.read_until(f, f'^\s*{n_levels}')

        ra.read_until(f, '^!')
        n_transitions = int(next(f))
    
        ra.read_until(f, '^!')
        transisions = ra.read_until(f, f'^\s*{n_transitions}')

        ra.read_until(f, '^!')
        n_partners = int(next(f))

        for i in range(n_partners):
            ra.read_until(f, '^!')
            partner = re.search('^(\d+)', next(f))[0]
        
            ra.read_until(f, '^!')
            n_colltrans = int(next(f))

            ra.read_until(f, '^!')
            n_colltemps = int(next(f))

            ra.read_until(f, '^!')
            colltemps = next(f).strip()

            ra.read_until(f, '^!')
            collrates = ra.read_until(f, f'^\s*{n_colltrans}')