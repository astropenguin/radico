__all__ = ['MolDB']


# standard library
import re
from logging import getLogger
logger = getLogger(__name__)


# dependent packages
import numpy as np
import radico as ra
import xarray as xr
from astropy.io import ascii
from astropy.constants import h, c, k_B


# module constants
h   = h.value
c   = c.value
k_B = k_B.value

DIMS = 'lv_from', 'lv_to', 'T_kin', 'coll_p'

COLL_P_LAMDA = {'1': 'H2',
                '2': 'para-H2',
                '3': 'otrho-H2',
                '4': 'electrons',
                '5': 'H',
                '6': 'He'}


# classes
class MolDB:
    def __init__(self, *, db=None):
        if db is None:
            db = self._create_db()
        
        if 'rel_g' not in db:
            db = self._calc_rel_g(db)

        if 'ein_B' not in db:
            db = self._calc_ein_B(db)
        
        self.db = db

    @staticmethod
    def _create_db(db):
        pass

    @staticmethod
    def _calc_rel_g(db):
        g    = db.g.values
        freq = db.freq.values

        rel_g = g[:,None] / g
        rel_g[np.isnan(freq)] = np.nan

        db['rel_g'] = DIMS[:2], rel_g
        return db
    
    @staticmethod
    def _calc_ein_B(db):
        freq  = db.freq.values
        ein_A = db.ein_A.values
        rel_g = db.rel_g.values

        B_ul = (ein_A * c**2) / (2*h * freq**3)
        B_lu = (rel_g * B_ul).T

        ein_B = np.full_like(ein_A, np.nan)
        tril  = np.tril_indices_from(ein_B)
        triu  = np.triu_indices_from(ein_B)
        ein_B[tril] = B_ul[tril]
        ein_B[triu] = B_lu[triu]

        db['ein_B'] = DIMS[:2], ein_B
        return db

    @classmethod
    def from_cdms(cls, filename):
        pass

    @classmethod
    def from_lamda(cls, filename):
        db = create_db_lamda(filename)
        return cls(db=db)

    @classmethod
    def from_netcdf(cls, filename):
        db = xr.open_dataset(filename)
        return cls(db=db)

    def to_netcdf(self, filename):
        self.db.to_netcdf(filename)

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
def create_db_cdms(filename):
    pass


def create_db_lamda(filename):
    # read molecular data
    with ra.open_lamda(filename) as f:
        # step 1
        ra.read_until(f, '^!')
        name = next(f).strip()

        ra.read_until(f, '^!')
        weight = float(next(f).strip())

        ra.read_until(f, '^!')
        n_levels = int(next(f))

        ra.read_until(f, '^!')
        lines = ra.read_until(f, f'^\s*{n_levels}')
        table_1 = ascii.read(lines)

        # step 2
        ra.read_until(f, '^!')
        n_transitions = int(next(f))
    
        ra.read_until(f, '^!')
        lines = ra.read_until(f, f'^\s*{n_transitions}')
        table_2 = ascii.read(lines)

        # step 3
        li_partner = []
        li_n_colltrans = []
        li_n_colltemps = []
        li_colltemps = []
        li_table_3 = []

        ra.read_until(f, '^!')
        n_partners = int(next(f))

        for i in range(n_partners):
            ra.read_until(f, '^!')
        li_partner.append(COLL_P_LAMDA[index])
              index = re.search('^(\d+)', next(f))[0]
        
            ra.read_until(f, '^!')
            li_n_colltrans.append(int(next(f)))

            ra.read_until(f, '^!')
            li_n_colltemps.append(int(next(f)))

            ra.read_until(f, '^!')
            li_colltemps.append(np.array(next(f).split(), 'f8'))

            ra.read_until(f, '^!')
            lines = ra.read_until(f, f'^\s*{li_n_colltrans[i]}')
            li_table_3.append(ascii.read(lines))
    
    # create database as xarray.Dataset
    # step 1
    q = table_1['col4'].astype('U')
    E = table_1['col2'].astype('f8')
    g = table_1['col3'].astype('f8')
    Q = table_1['col4'].astype('U')

    dims = DIMS[0]
    coords = {dims: (dims, Q)}
    E = xr.DataArray(E, coords, dims)
    g = xr.DataArray(g, coords, dims)
    
    # step 2
    n_from = table_2['col2'].astype('i8')
    n_to   = table_2['col3'].astype('i8')
    A_ul   = table_2['col4'].astype('f8')
    f_ul   = table_2['col5'].astype('f8') * 1e9

    shape = n_levels, n_levels
    freq  = np.full(shape, np.nan)
    ein_A = np.full(shape, np.nan)

    for i, (u, l) in enumerate(zip(n_from, n_to)):
        freq[u-1, l-1]  = f_ul[i]
        freq[l-1, u-1]  = f_ul[i]
        ein_A[u-1, l-1] = A_ul[i]

    dims = DIMS[:2]
    coords = {dims[0]: (dims[0], Q),
              dims[1]: (dims[1], Q)}

    freq  = xr.DataArray(freq, coords, dims)
    ein_A = xr.DataArray(ein_A, coords, dims)

    # step 3
    li_gamma = []

    for i in range(n_partners):
        partner     = li_partner[i]
        n_colltrans = li_n_colltrans[i]
        n_colltemps = li_n_colltemps[i]
        colltemps   = li_colltemps[i]
        table_3     = li_table_3[i]

        n_from   = table_3['col2'].astype('i8')
        n_to     = table_3['col3'].astype('i8')
        gamma_ul = np.array(table_3.to_pandas())[:, 3:]

        shape = n_levels, n_levels, n_colltemps, 1
        gamma = np.full(shape, np.nan)

        for i, (u, l) in enumerate(zip(n_from, n_to)):
            gamma[u-1, l-1, :, 0] = gamma_ul[i]
        
        dims = DIMS
        coords = {dims[0]: (dims[0], Q),
                  dims[1]: (dims[1], Q),
                  dims[2]: (dims[2], colltemps),
                  dims[3]: (dims[3], [partner])}

        gamma = xr.DataArray(gamma, coords, dims)
        li_gamma.append(gamma)

    gamma = xr.concat(li_gamma, dim=dims[3])
    gamma[dims[3]] = gamma[dims[3]].astype('U')

    # step 4
    db = xr.Dataset()
    db['name']  = name
    db['E']     = E
    db['g']     = g
    db['freq']  = freq
    db['ein_A'] = ein_A
    db['gamma'] = gamma

    return db