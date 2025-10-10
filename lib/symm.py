import enum
import math
from collections import Counter as multiset
import itertools

# -------------- Global Variables ----------------

'''Categorizes combinatorial objects into three types of interest: Those without repetition; those with; and those of single variate.'''
CTYPE = enum.Enum('PartitionType', {'Elementary': 1, 'Monomial': 2, 'Polynomial': 3})

# --------------     Objects      ----------------

class Partition(multiset[int]):
    '''
    A Partition is some (x_1, x_2, ..., x_n) such that x_1 ≥ x_2 ≥ ... ≥ x_n, which is represented as a multiset.

    **Properties**:
    > parts: The composition [x_1,x_2, ..., x_n]\n

    **Functions**:
    > isType: Compare properties to those of a combinatorial type
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def parts(self):
        return Composition(list(self.elements()))
    
    @property
    def isempty(self)->bool:
        return self.parts.isempty
    
    @property
    def sum(self)->int:
        return sum(self.elements())

    def isType(self, type: CTYPE, j: int)->bool:
        if(type == CTYPE.Elementary):
            return self == Partition([1]*j)
        if(type == CTYPE.Monomial):
            return self.sum == j
        if(type == CTYPE.Polynomial):
            return self == Partition([j])

class Composition(list[int]):
    '''
    A *Composition* is some imutable [x_1, x_2, ..., x_n], with no restrictions on the ordering of x_i.
    Compositions can be compared in a partial ordering, >, as defined in the notes.

    **Properties**:
    >order: The unique *Partition* of *parts* [y_1,...,y_m] which are a permuation of [x_1,...,x_n] with zeroes removed\n
    
    **Instance Methods:**
    >norm: Scales the *Composition* so that the *gcd* is 1.

    **Static Methods:**
    >generate: Return a list of all *Composition*s with *length* number of elements and *max* ≥ x_i
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def order(self)->Partition:
        return Partition(filter(lambda x: x!=0, self))

    @property
    def elements(self)->list[int]:
        return list(self)
    
    @property
    def sum(self)->int:
        return sum(self.elements)

    @property
    def isempty(self)->bool:
        return self==Composition([])
    
    @property
    def iszero(self)->bool:
        return len(list(filter(lambda x: x!=0, self.elements))) == 0
    
    @property
    def gcd(self)->int:
        if(self.iszero): return 1
        return math.gcd(*self.elements)
    
    def norm(self):
        gcd = self.gcd
        for i in range(len(self)): self[i] = self[i]//gcd
        return self

    @staticmethod
    def generate(max: int , length: int):
        return list(map(Composition, itertools.product(list(range(0, max + 1)), repeat=length)))

    def __eq__(self, other)->bool:
        '''
        **Examples**:
        >>> Composition([1,2,3]) == Composition([2,4,6])
        True
        
        >>> Composition([0,0,0]) == Composition([2,4,6])
        False

        >>> Composition([1,2,3]) == Composition([2,4,5])
        False
        '''
        if(type(self)!=type(other)):
            return False
        if(self.iszero or other.iszero):
            return self.iszero and other.iszero
        else:
            for i in range(len(self)):
                if self[i]*other.sum != other[i]*self.sum: return False
            return True
        
    def exact_eq(self, other)->bool:
        '''Check if two compositions are identical'''
        if(type(self)!=type(other)):
            return False
        if(len(self)!=len(other)):
            return False
        for i in range(len(self)):
            if self[i] != other[i]: return False
        return True

    def __gt__(self, other)->bool:
        '''Provides a standard partial ordering on compositions deriving from definitions in the notes
        
        **Examples**:
        >>> Composition([3,2,0]) > Composition([2,2,1])
        True
        
        >>> Composition([1,0,0]) > Composition([4,0,1])
        True
        
        >>> Composition([2,0,1]) > Composition([1,2,0])
        False
        
        >>> Composition([1,2,0]) > Composition([2,0,1])
        False'''
        if(self.iszero or other.iszero):
            return False
        if(self==other):
            return False
        cumulative_dif = 0
        for i in range(min(len(self.elements), len(other.elements))):
            cumulative_dif += self[i]*other.sum - other[i]*self.sum
            if(cumulative_dif < 0):
                return False
        return True
    
    def __str__(self)->str:
        return ''.join([str(x) for x in self])


# --------------    Interfaces    ----------------

class symm:
    '''
    Implements various symmetric functions on Compositions and Partitions.

    **Methods**:
    >monomial: Return the evaluation of *alpha* on *values*, where *alpha* is interpreted as the exponents of a monomial.\n
    >prf: Return the general symmetric function applied to *lam*, with parameters *j*, and a *selector*.\n
    >pre, prh, prp, prm: Specific cases of *prf*.\n
    >prh_inv: Compute the unique input partition to *prh* given it's output.
    '''

    @staticmethod
    def monomial(alpha: Composition, values: Composition) -> int:
        '''Requires: alpha and vars have the same length'''
        if alpha.isempty: return 1
        else: return math.prod(values[i]**alpha[i] for i in range(0,len(values)))

    @classmethod
    def prf(cls, j: int, selector, lam: Partition)->Partition:
        '''The terms of f are defined as monomial given by compositions whose *order* Partition satisfies the selection criteria'''
        return Partition([cls.monomial(x, lam.parts) for 
                         x in filter(lambda y:  selector(y.order),
                                                Composition.generate(j, len(list(lam.elements()))))])
    
    @classmethod
    def pre(cls, j: int, lam: Partition)->Partition:
        return cls.prf(j, lambda x: x.isType(CTYPE.Elementary, j), lam)
    
    @classmethod
    def prh(cls, j: int, lam: Partition)->Partition:
        return cls.prf(j, lambda x: x.isType(CTYPE.Monomial, j), lam)
    
    @classmethod
    def prp(cls, j: int, lam: Partition)->Partition:
        return cls.prf(j, lambda x: x.isType(CTYPE.Polynomial, j), lam)
    
    @classmethod
    def prm(cls, mu: Partition, lam: Partition)->Partition:
        return cls.prf(max(mu.elements()), lambda x: x==mu, lam)

    @classmethod
    def prh_inv(cls, j: int,pr: Partition)->multiset:
        '''
        Iteratively deduce the inverse of prh, using an iterative process to determine the next largest term.
        More details can be found in the accompanying notes.
        '''
        assert(0 < j)
        lam = Partition()
        q = -2**32
        pr_size = pr.sum #Used to terminate the loop when lambda is too large
        while (pr.total() > 0  and lam.sum <= pr_size):
            
            if(not lam):
                #Base case
                l_n = round(max(pr.elements())**(1/j)) #Can have large floating point errors for large powers
                q:int = l_n**(j-1)
            else:
                #Inductive step
                l_n = max(filter(lambda x: x!=0, pr.elements()))//q
            lam.update([l_n])
            pr.subtract(x*l_n for x in cls.prh(j-1, lam).elements())
        return lam