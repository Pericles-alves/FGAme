# -*- coding: utf8 -*-

import cython as C
import mathfuncs as m
from base import auto_public
from util import pyinject
from exceptions import DoesNotHaveInverseMatrixError, InvalidAxisError
if not C.compiled:
    from vec3 import Vec3
__all__ = ['Mat3','RotMat3','mMat3']

number = (float,int)


#######################   Matriz 3 x 3  #################################

class Mat3(object):
    '''
        Implementa uma matriz tridimensional e operações básicas de álgebra linear

    Example
    -------
    Criamos uma matriz a partir de uma lista de listas

    >>> M = Mat3([ [1,2,3],
    ...            [4,5,6],
    ...            [7,8,9]])

    Podemos também utilizar classes especializadas, como por exemplo a `RotMat3`
    , que cria uma matriz de rotação de tridimensional

    >>> R = RotMat3(3.1415, 'z'); R
    |-1  -0  0|
    | 0  -1  0|
    | 0   0  1|
    '''

    __slots__ = ['_data']

    def __init__(self,obj):
        self._data = list()

        for line in obj:
            for element in line:
                self._data.append(element)

        for element in self._data:
            element += 0.0

    @classmethod
    def _from_lists_(cls,M):
        '''Inicia a matriz a partir de uma lista de linhas.Corresponde ao
           método de inicialização padrão, mas pode ser invocado por classes
           caso a assinatura do contrutor padrão seja diferente'''
        new = object.__new__(cls)
        Mat3.__init__(new,M)
        return new

    @classmethod
    def from_flat(cls,data):
        '''Constroi matriz a partir de dados linearizados'''
        return cls._from_flat(data, restype=cls)

    @classmethod
    def _from_flat(cls,data, restype=None):
        new = object.__new__(restype or cls)
        new._data = list()
        for element in data:
            new._data.append(element)

        return new


    # Métodos de apresentação da informação da matriz ##################

    def aslist(self):
        '''Retorna a matrix como uma lista de listas'''
        a,b,c,d,e,f,g,h,i = self.flat()
        return [[a,b,c],[d,e,f],[g,h,i]]

    def flat(self):
        '''Itera sobre todos os elementos da matriz, primeiro os
           elementos da primeira linha, depois o da segunda e
           por último o da terceira linha.'''
        for element in self._data:
            yield(element)

    def colvecs(self):
        '''Retorna uma lista com os vetores coluna da matriz.
        >>> M = Mat3([ [1,2,3],
        ...            [4,5,6],
        ...            [7,8,9]])
        >>> M.colvecs()
        [Vec3(1, 4, 7), Vec3(2, 5, 8), Vec3(3, 6, 9)]
        '''
        a,b,c,d,e,f,g,h,i = self.flat()
        return [Vec3(a,d,g),Vec3(b,e,h),Vec3(c,f,i)]

    def rowvecs(self):
        '''Retorna uma lista com os vetores das linhas da matriz.
        >>> M = Mat3([ [1,2,3],
        ...            [4,5,6],
        ...            [7,8,9]])
        >>> M.rowvecs()
        [Vec3(1, 2, 3), Vec3(4, 5, 6), Vec3(7, 8, 9)]
        '''
        a,b,c,d,e,f,g,h,i = self.flat()
        return [Vec3(a,b,c),Vec3(d,e,f),Vec3(g,h,i)]

    # Métodos para cálculo de propriedades lineares da matriz ###########
    def det(self):
        '''Retorna o determinante da matriz
        >>> M = Mat3([[1,2,3],[4,5,6],[7,8,9]])
        >>> M.det()
        0
        '''
        a,b,c,d,e,f,g,h,i = self.flat()
        d1 = + (a * e * i)
        d2 = + (b * f * g)
        d3 = + (c * d * h)
        d4 = - (c * e * g)
        d5 = - (a * f * h)
        d6 = - (b * d * i)
        return d1 + d2 + d3 + d4 + d5 + d6

    def trace(self):
        '''  retornar o traco da matriz
        >>> M = Mat3([[1,2,3],
        ...           [4,5,6],
        ...           [7,8,9]])
        >>> M.trace()
        15
        '''
        return self._data[0]+self._data[4]+self._data[8]

    def diag(self):
        '''Retorna uma lista com os valores na diagonal principal da matriz

        >>> M = Mat3([[1,2,3],
        ...           [4,5,6],
        ...           [7,8,9]])
        >>> M.diag()
        [1, 5, 9]
        '''
        return [self._data[0],self._data[4],self._data[8]]

    def eig(self):
        '''Retorna uma tupla com a lista de autovalores e a matriz dos
        autovetores'''
        #TODO: Vec3
        pass

    def eigval(self):
        '''Retorna uma tupla com os autovalores da matriz
        '''
        #TODO:
        pass


    def eigvec(self, transpose=False):
        '''Retorna uma lista com os autovetores normalizados da matriz.

        A ordem dos autovetores corresponde àquela retornada pelo método
        `M.eigval()`'''
        #TODO:
        pass

    def transpose(self):
        '''Retorna a transposta da matriz

        >>> M = Mat3([[1, 2, 3],
        ...           [4, 5, 6],
        ...           [7, 8, 9]])
        >>> M.transpose()
        |1  4  7|
        |2  5  8|
        |3  6  9|

        '''
        a, b, c, d, e, f, g, h, i = self.flat()
        M = [[ a, d, g ],
             [ b, e, h ],
             [ c, f, i ]]
        return self._from_lists_(M)


    def rotate(self, theta, axis):
        '''Retorna uma matriz rotacionada pro um ângulo theta
        >>> M = Mat3([[1,2,3],
        ...           [4,5,6],
        ...           [7,8,9]])
        >>> M.rotate(45, 'z')
        |-0.598   0.801  0|
        |-0.801  -0.598  0|
        |     0       0  1|

        '''
        R = RotMat3(theta, axis)
        return R * self * R.transpose()

    def inv(self):
        '''Retorna a inversa da matriz
        >>> M = Mat3([[1,2,3],
        ...           [0,1,4],
        ...           [5,6,0]])
        >>> M.inv()
        |-24   18   5|
        | 20  -15  -4|
        | -5    4   1|
        '''

        if self.det() == 0:
            raise DoesNotHaveInverseMatrixError(
                'Matrix does not have an inverse matrix')

        a,b,c,d,e,f,g,h,i = self.flat()

        multiplying_factor = 1 / (self.det())
        inv = [[((e * i) - (f * h)), ((c * h) - (b * i)), ((b * f) - (c * e))],
               [((f * g) - (d * i)), ((a * i) - (c * g)), ((c * d) - (a * f))],
               [((d * h) - (e * g)), ((b * g) - (a * h)), ((a * e) - (b * d))]]
        return self._from_lists_(inv) * multiplying_factor



    # Sobrescrita de operadores #################################
    def _fmt_number(self,x):
        '''Função auxiliar para __repr__: formata número para impressão'''
        return ('%.3f' % x).rstrip('0').rstrip('.')

    def __repr__(self):
        '''x.__repr__(): <==> repr(x)'''
        l  = []
        for element in self.flat():
             l.append(element)

        a, b, c, d, e, f, g, h, i = map(self._fmt_number, l)
        n = max(len(a), len(d),len(g))
        m = max(len(b), len(e),len(h))
        o = max(len(c), len(f), len(i))

        l1 = '|%s  %s  %s|' % (a.rjust(n), b.rjust(m), c.rjust(o))
        l2 = '|%s  %s  %s|' % (d.rjust(n), e.rjust(m), f.rjust(o))
        l3 = '|%s  %s  %s|' % (g.rjust(n), h.rjust(m), i.rjust(o))
        return '%s\n%s\n%s' % (l1, l2,l3)

    def __str__(self):
       '''x.__str__() <==> str(x)'''
       return repr(self)

    def __len__(self):
        return 3

    def __iter__(self):
        it = self.flat()
        yield Vec3(next(it),next(it),next(it))
        yield Vec3(next(it),next(it),next(it))
        yield Vec3(next(it),next(it),next(it))

    def __getitem__(self,idx):
        '''x.__getitem__(i) <==> x[i]

        >>> M = Mat3([[1,2,3],
        ...          [4,5,6],
        ...          [7,8,9]])
        >>> M[1,1]
        5
        '''
        return self._data[idx[0]*3+idx[1]]

    def _matrix_mult_matrix(self, other):
        a,b,c,d,e,f,g,h,i = self.flat()
        j,k,l,m,n,o,p,q,r = self.flat()

        line1 = [(a*j) + (b*m) + (c*p), (a*k) + (b*n) + (c*q), (a*l) + (b*o) + (c*r)]
        line2 = [(d*j) + (e*m) + (f*p), (d*k) + (e*n) + (f*q), (d*l) + (e*o) + (f*r)]
        line3 = [(g*j) + (h*m) + (i*p), (g*k) + (h*n) + (i*q), (g*l) + (h*o) + (i*r)]

        return self._from_lists_([line1, line2, line3])

    def _matrix_mult_vector(self, other):
        x, y, z = other
        a, b, c, d, e, f, g, h, i = self.flat()

        result = [a*x + d*y + g*z, b*x + e*y + h*z, c*x + f*y + i*z]
        # TODO: trocar para retornar vec3
        return result

    # Operações matemáticas###############
    def __mul__(self,other):
        '''x.__mul__(y) <==> x * y'''

        if isinstance(other, Mat3):
            return self._matrix_mult_matrix(other)
        elif isinstance(other, number):
            return self._from_flat(x * other for x in self.flat())
        elif isinstance(other, list):
            return self._matrix_mult_vector(other)

    def __rmul__(self,other):
        if isinstance(other, Mat3):
            return self._matrix_mult_matrix(other)
        elif isinstance(other, number):
            return self._from_flat(x * other for x in self.flat())
        elif isinstance(other, list):
            return self._matrix_mult_vector(other)

    def __div__(self, other):
        '''x.__div__(y) <==> x / y'''
        return self._from_flat(x / other for x in self.flat())

    def __truediv__(self, other):
        '''x.__div__(y) <==> x / y'''
        return self._from_flat(x / other for x in self.flat())

    def __floordiv__(self,other):
        '''x.__div__(y) <==> x / y'''
        return self._from_flat(x // other for x in self.flat())

    def __add__(self,other):
        '''x.__add__(y) <==> x + y'''
        return self._from_flat(x + y for (x,y) in
                               zip(self.flat(),other.flat()))
    def __radd__(self,other):
        '''x.__radd__(y) <==> y + x'''
        return self + other

    def __sub__(self,other):
        '''x.__sub__(y) <==> x - y'''
        return self._from_flat(x - y for (x,y) in
                               zip(self.flat(),other.flat()))

    def __rsub__(self,other):
        '''x.__rsub__(y) <==> y - x '''
        return self._from_flat(y - x for (x,y) in
                               zip(self.flat(),other.flat()))

    def __neg__(self):
        '''x.__neg__() <==> -x'''
        return self._from_flat(-x for x in self.flat())

    def __nonzero__(self):
        return any(self.flat())


class mMat3(Mat3):
    '''Versão mutável de Mat3'''

    __slots__ = ['_data']

    def __init__(self,data):
        super(mMat3,self).__init__(data)
        self._data = list(data)

    def __setattr__(self,idx,value):
        i, j, k = idx
        self._data[i][j] = value

    def irotate(self,theta):
        '''Rotaciona a matriz *inplace*'''
        R = RotMat3(theta)
        self._data = (R * self * R.transpose())._data

    def itranspose(self):
        '''Transpõe a matriz *inplace*'''
        self._data[0],self._data[1],self._data[2] = self._data[0],self._data[3],self._data[6]
        self._data[3],self._data[4],self._data[5] = self._data[1],self._data[4],self._data[7]
        self._data[6],self._data[7],self._data[8] = self._data[2],self._data[5],self._data[8]

class RotMat3(Mat3):
    '''
        Cria uma matriz de rotação que realiza a rotação pelo ângulo theta
        especificado
    '''
    __slots__ = ['_theta','_transposed']

    def __init__(self,theta, axis):
        self._theta = float(theta)
        self._transposed = None

        self.C = m.cos(theta)
        self.S = m.sin(theta)

        if isinstance(axis, str) and axis == 'x':
            M = [[1, 0, 0], [0, C, - S], [0, S, C]]
        elif isinstance(axis, str) and axis == 'y':
            M = [[C, 0, S], [0, 1, 0], [- S, 0, C]]
        elif isinstance(axis, str) and axis == 'z':
            M = [[C, - S, 0], [S, C, 0], [0, 0, 1]]
        # elif isinstance(axis, Vec3):
        #     M = self._rotate_by_vector_axis(axis)
        else:
            raise InvalidAxisError("Eixo '" + axis + "' invalido.")

        super(RotMat3,self).__init__(M)

    def rotate(self,theta):
        return RotMat3(self._theta + theta)

    def transpose(self):
        if self._transposed is None:
            self._transposed = super(RotMat3,self).transpose()
        return self._transposed

    def inv(self):
        return self.transpose()

    @property
    def theta(self):
        return self._theta

    def _rotate_by_vector_axis(self, vector):
        a, b, c = vector.as_tuple()

        line1 = [(self.C + (1 - self.C) * (a ** 2)),
                 (((1 - self.C) * a * b) + (self.S * c)),
                 (((1 - self.C) * a * c) - (self.S * b))]
        line2 = [(((1 - self.C) * b * a) - (self.S * c)),
                 (self.C + ((1 - self.C) * (b ** 2))),
                 (((1 - self.C) * b * c) + (self.S * a))]
        line3 = [(((1 - self.C) * c * a) + (self.S * b)),
                 (((1 - self.C) * c * b) - (self.S * a)),
                 (self.C + ((1 - self.C) * (c ** 2)))]

        M = [line1, line2, line3]
        return M


if __name__ == '__main__':
    import doctest
    doctest.testmod()
