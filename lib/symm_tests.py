import unittest
import random
from typing import Iterable, Sequence, Mapping, Any

from symm import *
class TestSymmFunc(unittest.TestCase):

    lib = symm

    def setUp(self) -> None:
        return super().setUp()
                
    def test_monomial(self):
        '''
        '''
        in_indecies:list[Iterable] = \
           [[], [0], [1,1,0,1,1], [2,1,0,1,1,0,0,0], [1,1,0,1,1,0,0,0]]
        in_terms:list[Sequence] = \
           [[], [5], [3,5,6,3,7], range(3,10), 
            [5,1,0,9,2,0,0,6]]
        output:list[int] = \
           [1, 1, 315, 1512, 90]
        for i in range(len(in_indecies)):
            with self.subTest(i = i):
                self.assertEqual(self.lib.monomial(Composition(in_indecies[i]),Composition(in_terms[i])),
                                  output[i])

    def test_pre(self):
        '''
        '''
        in_j:list[int] = \
            [0,0,1,2,2,3]
        in_parts:list = \
            [[],[1,2,3],[1,2,3],[2,3],[2,4,3,6],[1,2,2,3,5,7]]
        output:list = \
            [[1],[1],[1,2,3],[6],[8,6,12,12,24,18],
             [4,6,10,14,6,10,14,15,21,35,12,20,28,30,42,70,30,42,70,105]]
        
        for i in range(len(in_j)):
            with self.subTest(i = i):
                self.assertEqual(self.lib.pre(in_j[i], Partition(in_parts[i])), 
                                 Partition(output[i]))

    def test_prh(self):
        '''
        '''
        in_j:list[int] = \
            [0,0,1,1,2,5,3,2]
        in_parts:list = \
            [[],[1,2,3],[],[1,2,3],[2,3], [1,2],[2,3,6],[1,2,3,8,4,4]]
        output:list = \
            [[1],[1],[],[1,2,3],[4,6,9],[1,2,4,8,16,32],
             [8,12,24,18,36,72,27,54,108,216],
             [1,2,3,4,4,4,6,8,8,8,9,12,12,16,16,16,16,24,32,32,64]]
        
        for i in range(len(in_j)):
            with self.subTest(i = i):
                self.assertEqual(self.lib.prh(in_j[i], Partition(in_parts[i])), 
                                 Partition(output[i]))

    def test_prh_inv(self):
        '''
        '''
        in_j:list[int] = \
            [1,1,3,2]
        in_parts:list = \
            [[], [1,2,3], [8,12,24,18,36,72,27,54,108,216],
             [64,32,32,24,16,16,16,16,12,12,9,8,8,8,6,4,4,4,3,2,1]]
        output:list = \
            [[],[1,2,3],[2,3,6],[1,2,3,8,4,4]]
        
        for i in range(len(in_j)):
            with self.subTest(i = i):
                self.assertEqual(self.lib.prh_inv(in_j[i], Partition(in_parts[i])), 
                                 Partition(output[i]))
        
    @unittest.skip("Efficiency during development")
    def test_efficiency(self):
        raise(NotImplementedError('Current implementation is too memory intensive and slow. Use itertools for better performance'))
        #Random large scale inverse
        random_partition:Partition = Partition([random.randint(1,10) for i in range(40)])
        self.assertEqual(self.lib.prh_inv(5,self.lib.prh(5,random_partition)),random_partition)

        
if(__name__=='__main__'):
    '''
    Run the main tests with the unittest package
    '''
    unittest.main()
    #Runs any alternative testing
    pass