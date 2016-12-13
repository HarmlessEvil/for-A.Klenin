import unittest
from functools import reduce
from math import sin, cos, pi

class Quaternion: 
    def __init__(self, a = 0, b = 0, c = 0, d = 0):
        self._a = a
        if isinstance(b, tuple) or isinstance(b, list):
            self._b, self._c, self._d = b[0], b[1], b[2]
        else:
            self._b, self._c, self._d = b, c, d

    @staticmethod
    def AxisAngle(angle, axis):
        norm = reduce((lambda a, x: a + x ** 2), axis, 0) ** 0.5
        axis = [ i/norm for i in axis ]
        return Quaternion(cos(angle/2),[ i*sin(angle/2) for i in axis ])

    def turnAround(self, angle, axis):
        return self * Quaternion.AxisAngle(angle, axis)

    def setAll(self, list):
        (self._a, self._b, self._c, self._d) = list

    def setA(self, a):
        self._a = a

    def setB(self, b):
        self._b = b

    def setC(self, c):
        self._c = c

    def setD(self, d):
        self._d = d

    def getAll(self):
        return (self._a, self._b, self._c, self._d)
    
    def getA(self):
        return self._a

    def getB(self):
        return self._b

    def getC(self):
        return self._c

    def getD(self):
        return self._d

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self._a + other._a, self._b + other._b, self._c + other._c, self._d + other._d)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self._a * other._a - self._b * other._b - self._c * other._c - self._d * other._d,
                              self._a * other._b + other._a * self._b + self._d * other._c - self._c * other._d,
                              self._a * other._c + other._a * self._c + self._b * other._d - self._d * other._b,
                              self._a * other._d + other._a * self._d + self._c * other._b - self._b * other._c)

    def abs(self):
        return (self._a ** 2 + self._b ** 2 + self._c ** 2 + self._d ** 2) ** 0.5

    def inverse(self):
        norm = self.abs() ** 2
        return Quaternion(self._a / norm, self._b / norm, self._c / norm, self._d / norm)

    def rotateVec(self, vec):
        Qvec = Quaternion(0, vec)
        return (self * Qvec * self.inverse()).getAll()[1:4]

class Test1(unittest.TestCase):
    A = Quaternion(1,2,3,4)
    B = Quaternion(-1,-2,-3,-4)
    C = Quaternion(8,0,0,6)

    def test_addition(self):
        self.assertEqual((self.A+self.B).getAll(), (0,0,0,0))

    def test_multiplication(self):
        self.assertEqual((self.A*self.B).getAll(), (28,-4,-6,-8))
        self.assertEqual((Quaternion(4)*Quaternion(0,1,1,1)).getAll(),(0,4,4,4))
        self.assertEqual((Quaternion(4)*Quaternion(4)).getAll(), (16,0,0,0))

    def test_inversion(self):
        self.assertEqual(self.A.abs(),self.B.abs())

    def test_inversion(self):
        self.assertEqual((self.C.inverse()).getAll(),(0.08,0,0,0.06))

    def test_onVector(self):
        self.assertEqual(self.C.rotateVec((1,2,3)),(1,2,0.8399999999999999))

    def test_AxisAngle(self):
        a = (Quaternion.AxisAngle(pi,(0,1,0))).getAll()
        b = (0,0,1,0)
        for i in range (3):
            self.assertAlmostEqual(a[i], b[i], places=5)

    def test_turnAround(self):
        a = ((Quaternion(0,0,-1,0)).turnAround(pi,(0,1,0))).getAll()
        b = (1, 0, 0, 0)
        for i in range(3):
            self.assertAlmostEqual(a[i], b[i], places=5)

unittest.main()
