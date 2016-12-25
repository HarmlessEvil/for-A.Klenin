from ctypes import *
import unittest

class Lib:
        LIBtree = CDLL('Win32Project1.dll')

        create = LIBtree.LSQ_CreateSequence
        insert = LIBtree.LSQ_InsertElement
        getByIndex = LIBtree.LSQ_GetElementByIndex
        deref = LIBtree.LSQ_DereferenceIterator
        destroy = LIBtree.LSQ_DestroySequence
        getSize = LIBtree.LSQ_GetSize
        dable = LIBtree.LSQ_IsIteratorDereferencable
        pastRear = LIBtree.LSQ_IsIteratorPastRear
        beforeFirst = LIBtree.LSQ_IsIteratorBeforeFirst
        rew = LIBtree.LSQ_RewindOneElement
        adv = LIBtree.LSQ_AdvanceOneElement
        gotFront = LIBtree.LSQ_GetFrontElement
        gotPastRear = LIBtree.LSQ_GetPastRearElement
        getKey = LIBtree.LSQ_GetIteratorKey
        shift = LIBtree.LSQ_ShiftPosition
        setp = LIBtree.LSQ_SetPosition
        delFront = LIBtree.LSQ_DeleteFrontElement
        delRear = LIBtree.LSQ_DeleteRearElement
        delByKey = LIBtree.LSQ_DeleteElement

        insert.argtypes = [c_void_p, c_int, c_int]
        getByIndex.argtypes = [c_void_p]
        deref.argtypes = [c_void_p]
        destroy.argtypes = [c_void_p]
        getSize.argtypes = [c_void_p]
        dable.argtypes = [c_void_p]
        pastRear.argtypes = [c_void_p]
        beforeFirst.argtypes = [c_void_p]
        rew.argtypes = [c_void_p]
        adv.argtypes = [c_void_p]
        gotFront.argtypes = [c_void_p]
        getKey.argtypes = [c_void_p]
        gotPastRear.argtypes = [c_void_p]
        delFront.argtypes = [c_void_p]
        delRear.argtypes = [c_void_p]
        shift.argtypes = [c_void_p, c_int]
        setp.argtypes = [c_void_p, c_int]
        delByKey.argtypes = [c_void_p, c_int]

        create.restype = c_void_p
        getByIndex.restype = c_void_p
        deref.restype = POINTER(c_int)
        gotFront.restype = POINTER(c_int)
        gotPastRear.restype = POINTER(c_int)
        getSize.restype = c_int
        dable.restype = c_int
        pastRear.restype = c_int
        getKey.restype = c_int

class Tree:
    __slots__ = ['data']
    def __init__(self, other = None):
        #*args и **kwargs не получились :(
        self.data = cast(Lib.create(), c_void_p)
        if type(other) == type({}):
            for key in other:
                self[key] = other[key]
        elif type(other) == list or type(other) == tuple:
            for each in other:
                if len(each) < 2:
                    raise TypeError
                elif len(each) > 2:
                    raise ValueError
                if  type(each) != list or type(each) == tuple:
                    raise ValueError
            for each in other:
                self[each[0]] = each[1]
        elif other == None:
            return
        else:
            raise TypeError
    @staticmethod
    def fromkeys(somelist, value = 0):
        return Tree([[i, value] for i in somelist])

    class Iterator(Structure):
        _fields_ = [("data", c_void_p)]
        def deref(self):
            return cast(Lib.deref(self.data), POINTER(c_int))
        def isDerefable(self):
            return bool(Lib.dable(self.data))
        def isPastRear(self):
            return bool(Lib.pastRear(self.data))
        def isBeforeFirst(self):
            return bool(Lib.beforeFirst(self.data))
        def dec(self):
            Lib.rew(self.data)
            return self
        def inc(self):
            Lib.adv(self.data)
            return self
        def key(self):
            return Lib.getKey(self.data)
        def moveInto(self, amount):
            Lib.shift(self.data, amount)
            return self
        def setPos(self, pos):
            Lib.setp(self.data, pos)
            return self
        
    def __setitem__(self, key, value):
        Lib.insert(self.data, key, value)
    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)
        res = Tree.Iterator()
        res.data = cast(Lib.getByIndex(self.data, key), c_void_p)
        return res.deref().contents.value
    def __len__(self):
        return Lib.getSize(self.data)
    def __iter__(self):
        it = self.getFront()
        while not it.isPastRear():
            yield it.key(), it.deref().contents.value
            it.inc()
    def __contains__(self, key):
        return not self.getIter(key).isPastRear()
    def __eq__(self, other):
        if len(self) != len (other):
            return False
        for key, value in other:
            if self[key] != value:
                return False
        return True
    def __str__(self):
        res = '{'
        l = len(self)
        for k, v in self:
            l -= 1
            res += str(k) + ': ' + str(v)
            if l:
                res += ', '
        res += '}'
        return res
    def __repr__(self):
        return str(self)
    def getIter(self, key):
        res = Tree.Iterator()
        res.data = cast(Lib.getByIndex(self.data, key), c_void_p)
        return res
    def getFront(self):
        res = Tree.Iterator()
        res.data = cast(Lib.gotFront(self.data), c_void_p)
        return res
    def getPastRear(self):
        res = Tree.Iterator()
        res.data = cast(Lib.gotPastRear(self.data), c_void_p)
        return res
    def clear(self):
        Lib.destroy(self.data)
        self.data = cast(Lib.create(), c_void_p)
    def copy(self):
        res = Tree()
        #Есть ли нормальный способ сделать это?
        for key, value in self:
            res[key] = value
        return res
    def deleteFront(self):
        Lib.delFront(self.data)
    def __delitem__(self, key):
        Lib.delByKey(self.data, key)
    def get(self, key, default = None):
        if key in self:
            return self[key]
        else:
            return default
    def items(self):
        return [(key, value) for key, value in self]
    def keys(self):
        return [key[0] for key in self]
    def values(self):
        return [key[1] for key in self]
    def pop(self, key, default = KeyError):
        if key not in self:
            if default == KeyError:
                raise default
            else:
                return default
        else:
            res = self[key]
            del self[key]
            return res
    def popitem(self):
        if len(self) > 0:
            res = self.getFront().key(), self.getFront().deref().contents.value
            self.deleteFront()
            return res
        else:
            raise KeyError
    def setdefault(self, key, default = 0):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default
    def update(self, other):
        for key, value in other:
            self[key] = value
                
class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.A = Tree()
    
    def test_in_out(self):
        A = self.A
        
        A[2] = 5
        self.assertEqual(A[2], 5)

    def test_amount(self):
        A = self.A
        
        A[7] = 11
        A[4] = 25
        A[18] = -0
        self.assertEqual(len(A), 3)

    def test_iterator_methods(self):
        A = self.A
        if A.__class__ == Tree:
            A[4] = 40
                
            self.assertTrue(A.getIter(4).isDerefable())
            self.assertTrue(A.getIter(88).isPastRear())
            self.assertTrue(A.getPastRear().isPastRear())
            self.assertTrue(A[4], A.getFront())
            self.assertTrue(A.getIter(4).dec().isBeforeFirst())

            self.assertFalse(A.getIter(4).dec().isDerefable())
            self.assertFalse(A.getPastRear().isDerefable())

            self.assertEqual(A.getIter(4).key(), 4)

            A[5] = -2502
            self.assertEqual(A.getIter(4).inc().key(), 5)

            A[71] = 0
            self.assertEqual(A.getIter(71).moveInto(-2).deref().contents.value,
                             A.getIter(4).deref().contents.value)
            self.assertEqual(A.getPastRear().setPos(2).key(), A.getFront().inc().key())

    def test_destruction(self):
        A = self.A

        if A.__class__ == Tree:
            A[1] = 1
            A[2] = 50

            A.deleteFront()
            self.assertEqual(A.getFront().deref().contents.value, 50)

    def test_contains(self):
        A = self.A

        A[5] = 70
        self.assertTrue(5 in A)

    def test_clear(self):
        A = self.A
        A[4] = 0
        A[400] = 0
        B = A
        A.clear()
        
        self.assertEqual(A, B)
        self.assertEqual(len(A), 0)

    def test_not_wow_its_memcpy(self):
        A = Tree()

        A[4] = 90
        A[5] = -50
        B = A.copy()

        self.assertTrue(4 in B)
        self.assertTrue(5 in B)
        self.assertFalse(B is A)

    def test_canonical_get(self):
        A = self.A

        A[1] = 6
        self.assertEqual(A.get(1), 6)
        self.assertEqual(A.get(2), None)
        self.assertEqual(A.get(2, 'редиска'), 'редиска')
        self.assertRaises(KeyError, A.__getitem__, 2)

    def test_items_and_keys_and_values(self):
        A = self.A

        A[1] = 2
        A[2] = 3
        self.assertEqual(list(A.items()), [(1, 2), (2, 3)])
        self.assertEqual(list(A.keys()), [1, 2])
        self.assertEqual(list(A.values()), [2, 3])

    def test_pop__item__(self):
        A = self.A

        A[1] = 1
        self.assertTrue(1 in A)
        self.assertEqual(A.pop(1), 1)
        self.assertFalse(1 in A)

        self.assertRaises(KeyError, A.pop, 1)
        self.assertEqual(A.pop(1, tuple()), tuple())

        A[1] = 1
        A[2] = 2
        self.assertTrue(set([A.popitem()]) < set([(1,1),(2,2)]))
        self.assertTrue(set([A.popitem()]) < set([(1,1),(2,2)]))
        self.assertRaises(KeyError, A.popitem)

    def test_setdefault(self):
        A = self.A
        if A.__class__ == Tree:
            self.assertEqual(A.setdefault(1), 0)
            self.assertEqual(A.setdefault(1), 0)
            self.assertEqual(A[1], 0)
        else:
            self.assertEqual(A.setdefault(1), None)
            self.assertEqual(A.setdefault(1), None)
            self.assertEqual(A[1], None)
            
        self.assertEqual(A.setdefault(2, 3), 3)
        self.assertEqual(A.setdefault(2, 5), 3)
        self.assertEqual(A[2], 3)

    def test_update(self):
        A = self.A
        A[1] = -5

        B = Tree()
        B[1] = 4
        B[2] = 3

        self.assertTrue(1 in A)
        self.assertFalse(2 in A)
        self.assertRaises(KeyError, A.__getitem__, 2)

        self.assertEqual(A.update(B), None)
        self.assertEqual(A[1], 4)
        self.assertEqual(A[2], 3)

    def test_yummy_constructors(self):
        A = self.A
            
        self.assertRaises(TypeError, A.__class__, 4)
        self.assertRaises(TypeError, A.__class__, [4])
        self.assertRaises(ValueError, A.__class__, [[4, 5, 2]])

        A[1] = 2
        A[4] = 6

        self.assertEqual(A, A.__class__({1:2, 4:6}))
        self.assertEqual(A, A.__class__([[1, 2], [4, 6]]))

        if A.__class__ == Tree:
            A[1] = 0
            A[4] = 0
        else:
            A[1] = None
            A[4] = None

        self.assertTrue(A == A.__class__.fromkeys([1, 4]))

        A[1] = 5
        A[4] = 5

        self.assertTrue(A == A.__class__.fromkeys([1, 4], 5))

class DicktEqualityTest(SimpleTest):
        def setUp(self):
            self.A = dict()

if __name__ == '__main__':
    unittest.main()

