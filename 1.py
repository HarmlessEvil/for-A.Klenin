from ctypes import *
import unittest

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

class Iterator(Structure):
#как бы сделать его вложенным в дерево?
        _fields_ = [("data", c_void_p)]
        def deref(self):
            return cast(deref(self.data), POINTER(c_int))
        def isDerefable(self):
            return bool(dable(self.data))
        def isPastRear(self):
            return bool(pastRear(self.data))
        def isBeforeFirst(self):
            return bool(beforeFirst(self.data))
        def dec(self):
            rew(self.data)
            return self
        def inc(self):
            adv(self.data)
            return self
        def key(self):
            return getKey(self.data)
        def moveInto(self, amount):
            shift(self.data, amount)
            return self
        def setPos(self, pos):
            setp(self.data, pos)
            return self

class Tree:
    __slots__ = ['data']
    def __init__(self):
        self.data = cast(create(), c_void_p)
    def __del__(self):
        destroy(self.data)    
    def __setitem__(self, key, value):
        insert(self.data, key, value)
    def __getitem__(self, key):
        res = Iterator()
        res.data = cast(getByIndex(self.data, key), c_void_p)
        return res
    def __len__(self):
        return getSize(self.data)
    def getFront(self):
        res = Iterator()
        res.data = cast(gotFront(self.data), c_void_p)
        return res
    def getPastRear(self):
        res = Iterator()
        res.data = cast(gotPastRear(self.data), c_void_p)
        return res
    def deleteFront(self):
        delFront(self.data)
    def deleteRear(self):
        delRear(self.data)
    def removeExactly(self, key):
        delByKey(self.data, key)

class ComplexTest(unittest.TestCase):
    def setUp(self):
        self.A = Tree()
    
    def test_in_out(self):
        A = self.A
        
        A[2] = 5
        self.assertEqual(((A[2].deref()).contents).value, 5)

    def test_amount(self):
        A = self.A
        
        A[7] = 11
        A[4] = 25
        A[18] = -0
        self.assertEqual(len(A), 3)

    def test_iterator_methods(self):
        A = self.A
        A[4] = 40
        
        self.assertTrue(A[4].isDerefable())
        self.assertTrue(A[88].isPastRear())
        self.assertTrue(A.getPastRear().isPastRear())
        self.assertTrue(A[4], A.getFront())
        self.assertTrue(A[4].dec().isBeforeFirst())

        self.assertFalse(A[4].dec().isDerefable())
        self.assertFalse(A.getPastRear().isDerefable())

        self.assertEqual(A[4].key(), 4)

        A[5] = -2502
        self.assertEqual(A[4].inc().key(), 5)

        A[71] = 0
        self.assertEqual(A[71].moveInto(-2).deref().contents.value,
                         A[4].deref().contents.value)
        self.assertEqual(A.getPastRear().setPos(2).key(), A.getFront().inc().key())

    def test_destruction(self):
        A = self.A

        
        A[1] = 1
        A[2] = 50

        A.deleteFront()
        self.assertEqual(A.getFront().deref().contents.value, 50)

        A.deleteRear()
        self.assertFalse(A.getFront().isDerefable())

        A[90] = -30
        A[-30] = 90
        A.removeExactly(90)
        self.assertEqual(A.getFront().key(), -30)

if __name__ == '__main__':
    unittest.main()
