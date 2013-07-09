# -*- coding: utf-8 -*-
# Horton is a development platform for electronic structure methods.
# Copyright (C) 2011-2013 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of Horton.
#
# Horton is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Horton is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--
'''Auxiliary routines related to multipole moments

   This module fixes all the conventions with respect to multipole moments. Some
   of the code below may (in some way) reoccur in the low-level routines. In any
   case, such low-level code should be consistent with the conventions in this
   module. See for example, horton.gobasis.cext.cart_to_pur_low.
'''


# TODO: remove duplicate code with gobasis, e.g. get_shell_nbasis


import numpy as np


__all__ = ['get_cartesian_powers', 'get_ncart', 'get_ncart_cumul',
           'rotate_cartesian_moments', 'get_npure', 'get_npure_cumul']


def get_cartesian_powers(lmax):
    '''Return an ordered list of power for x, y and z up to angular moment lmax

       **Arguments:**

       lmax
            The maximum angular momentum (0=s, 1=p, 2=d, ...)

       **Returns:** an array where each row corresponds to a multipole moment
       and each column corresponds to a power of x, y and z respectively. The
       rows are grouped per angular momentum, first s, them p, then d, and so
       on. Within one angular momentum the rows are sorted 'alphabetically',
       e.g. for l=2: xxx, xxy, xxz, xyy, xyz, xzz, yyy, yyz, yzz, zzz.
    '''
    cartesian_powers = np.zeros((get_ncart_cumul(lmax), 3), dtype=int)
    counter = 0
    for l in xrange(0, lmax+1):
        for nx in xrange(l+1, -1, -1):
            for ny in xrange(l-nx, -1, -1):
                nz = l - ny - nx
                cartesian_powers[counter] = [nx, ny, nz]
                counter += 1
    return cartesian_powers


def get_ncart(l):
    '''The number of cartesian powers for a given angular momentum, l'''
    return ((l+2)*(l+1))/2


def get_ncart_cumul(lmax):
    '''The number of cartesian powers up to a given angular momentum, lmax.'''
    return ((lmax+1)*(lmax+2)*(lmax+3))/6



# Each item in the following list:
#  - defines how a cartesian multipole is transformed.
#  - corresponds to the multipole moments defined by get_cartesian_powers.
#  - consists of a list of rules.
# Each rule contains at least two integer and corresponds to a single term:
#  - that accounts for the contrubution of the rotation of a multipole
#  - first an index for the multipole that the rotated form contributes to
#  - second a linear coefficient for the term
#  - then a number of indexes that refer to coefficients in the rotation matrix
#    that occur as factors in the term.

cartesian_transforms = [
    [[ 0,  1]],
    [[ 1,  1,  0],
     [ 2,  1,  1],
     [ 3,  1,  2]],
    [[ 1,  1,  3],
     [ 2,  1,  4],
     [ 3,  1,  5]],
    [[ 1,  1,  6],
     [ 2,  1,  7],
     [ 3,  1,  8]],
    [[ 4,  1,  0,  0],
     [ 5,  2,  0,  1],
     [ 6,  2,  0,  2],
     [ 7,  1,  1,  1],
     [ 8,  2,  1,  2],
     [ 9,  1,  2,  2]],
    [[ 4,  1,  0,  3],
     [ 5,  1,  1,  3],
     [ 5,  1,  0,  4],
     [ 6,  1,  2,  3],
     [ 6,  1,  0,  5],
     [ 7,  1,  1,  4],
     [ 8,  1,  2,  4],
     [ 8,  1,  1,  5],
     [ 9,  1,  2,  5]],
    [[ 4,  1,  0,  6],
     [ 5,  1,  1,  6],
     [ 5,  1,  0,  7],
     [ 6,  1,  2,  6],
     [ 6,  1,  0,  8],
     [ 7,  1,  1,  7],
     [ 8,  1,  2,  7],
     [ 8,  1,  1,  8],
     [ 9,  1,  2,  8]],
    [[ 4,  1,  3,  3],
     [ 5,  2,  3,  4],
     [ 6,  2,  3,  5],
     [ 7,  1,  4,  4],
     [ 8,  2,  4,  5],
     [ 9,  1,  5,  5]],
    [[ 4,  1,  3,  6],
     [ 5,  1,  4,  6],
     [ 5,  1,  3,  7],
     [ 6,  1,  5,  6],
     [ 6,  1,  3,  8],
     [ 7,  1,  4,  7],
     [ 8,  1,  5,  7],
     [ 8,  1,  4,  8],
     [ 9,  1,  5,  8]],
    [[ 4,  1,  6,  6],
     [ 5,  2,  6,  7],
     [ 6,  2,  6,  8],
     [ 7,  1,  7,  7],
     [ 8,  2,  7,  8],
     [ 9,  1,  8,  8]],
    [[10,  1,  0,  0,  0],
     [11,  3,  0,  0,  1],
     [12,  3,  0,  0,  2],
     [13,  3,  0,  1,  1],
     [14,  6,  0,  1,  2],
     [15,  3,  0,  2,  2],
     [16,  1,  1,  1,  1],
     [17,  3,  1,  1,  2],
     [18,  3,  1,  2,  2],
     [19,  1,  2,  2,  2]],
    [[10,  1,  0,  0,  3],
     [11,  1,  0,  0,  4],
     [11,  2,  0,  1,  3],
     [12,  1,  0,  0,  5],
     [12,  2,  0,  2,  3],
     [13,  1,  1,  1,  3],
     [13,  2,  0,  1,  4],
     [14,  2,  1,  2,  3],
     [14,  2,  0,  2,  4],
     [14,  2,  0,  1,  5],
     [15,  1,  2,  2,  3],
     [15,  2,  0,  2,  5],
     [16,  1,  1,  1,  4],
     [17,  1,  1,  1,  5],
     [17,  2,  1,  2,  4],
     [18,  1,  2,  2,  4],
     [18,  2,  1,  2,  5],
     [19,  1,  2,  2,  5]],
    [[10,  1,  0,  0,  6],
     [11,  1,  0,  0,  7],
     [11,  2,  0,  1,  6],
     [12,  1,  0,  0,  8],
     [12,  2,  0,  2,  6],
     [13,  1,  1,  1,  6],
     [13,  2,  0,  1,  7],
     [14,  2,  1,  2,  6],
     [14,  2,  0,  2,  7],
     [14,  2,  0,  1,  8],
     [15,  1,  2,  2,  6],
     [15,  2,  0,  2,  8],
     [16,  1,  1,  1,  7],
     [17,  1,  1,  1,  8],
     [17,  2,  1,  2,  7],
     [18,  1,  2,  2,  7],
     [18,  2,  1,  2,  8],
     [19,  1,  2,  2,  8]],
    [[10,  1,  0,  3,  3],
     [11,  1,  1,  3,  3],
     [11,  2,  0,  3,  4],
     [12,  1,  2,  3,  3],
     [12,  2,  0,  3,  5],
     [13,  1,  0,  4,  4],
     [13,  2,  1,  3,  4],
     [14,  2,  2,  3,  4],
     [14,  2,  1,  3,  5],
     [14,  2,  0,  4,  5],
     [15,  1,  0,  5,  5],
     [15,  2,  2,  3,  5],
     [16,  1,  1,  4,  4],
     [17,  1,  2,  4,  4],
     [17,  2,  1,  4,  5],
     [18,  1,  1,  5,  5],
     [18,  2,  2,  4,  5],
     [19,  1,  2,  5,  5]],
    [[10,  1,  0,  3,  6],
     [11,  1,  1,  3,  6],
     [11,  1,  0,  4,  6],
     [11,  1,  0,  3,  7],
     [12,  1,  2,  3,  6],
     [12,  1,  0,  5,  6],
     [12,  1,  0,  3,  8],
     [13,  1,  1,  4,  6],
     [13,  1,  1,  3,  7],
     [13,  1,  0,  4,  7],
     [14,  1,  2,  4,  6],
     [14,  1,  2,  3,  7],
     [14,  1,  1,  5,  6],
     [14,  1,  1,  3,  8],
     [14,  1,  0,  5,  7],
     [14,  1,  0,  4,  8],
     [15,  1,  2,  5,  6],
     [15,  1,  2,  3,  8],
     [15,  1,  0,  5,  8],
     [16,  1,  1,  4,  7],
     [17,  1,  2,  4,  7],
     [17,  1,  1,  5,  7],
     [17,  1,  1,  4,  8],
     [18,  1,  2,  5,  7],
     [18,  1,  2,  4,  8],
     [18,  1,  1,  5,  8],
     [19,  1,  2,  5,  8]],
    [[10,  1,  0,  6,  6],
     [11,  1,  1,  6,  6],
     [11,  2,  0,  6,  7],
     [12,  1,  2,  6,  6],
     [12,  2,  0,  6,  8],
     [13,  1,  0,  7,  7],
     [13,  2,  1,  6,  7],
     [14,  2,  2,  6,  7],
     [14,  2,  1,  6,  8],
     [14,  2,  0,  7,  8],
     [15,  1,  0,  8,  8],
     [15,  2,  2,  6,  8],
     [16,  1,  1,  7,  7],
     [17,  1,  2,  7,  7],
     [17,  2,  1,  7,  8],
     [18,  1,  1,  8,  8],
     [18,  2,  2,  7,  8],
     [19,  1,  2,  8,  8]],
    [[10,  1,  3,  3,  3],
     [11,  3,  3,  3,  4],
     [12,  3,  3,  3,  5],
     [13,  3,  3,  4,  4],
     [14,  6,  3,  4,  5],
     [15,  3,  3,  5,  5],
     [16,  1,  4,  4,  4],
     [17,  3,  4,  4,  5],
     [18,  3,  4,  5,  5],
     [19,  1,  5,  5,  5]],
    [[10,  1,  3,  3,  6],
     [11,  1,  3,  3,  7],
     [11,  2,  3,  4,  6],
     [12,  1,  3,  3,  8],
     [12,  2,  3,  5,  6],
     [13,  1,  4,  4,  6],
     [13,  2,  3,  4,  7],
     [14,  2,  4,  5,  6],
     [14,  2,  3,  5,  7],
     [14,  2,  3,  4,  8],
     [15,  1,  5,  5,  6],
     [15,  2,  3,  5,  8],
     [16,  1,  4,  4,  7],
     [17,  1,  4,  4,  8],
     [17,  2,  4,  5,  7],
     [18,  1,  5,  5,  7],
     [18,  2,  4,  5,  8],
     [19,  1,  5,  5,  8]],
    [[10,  1,  3,  6,  6],
     [11,  1,  4,  6,  6],
     [11,  2,  3,  6,  7],
     [12,  1,  5,  6,  6],
     [12,  2,  3,  6,  8],
     [13,  1,  3,  7,  7],
     [13,  2,  4,  6,  7],
     [14,  2,  5,  6,  7],
     [14,  2,  4,  6,  8],
     [14,  2,  3,  7,  8],
     [15,  1,  3,  8,  8],
     [15,  2,  5,  6,  8],
     [16,  1,  4,  7,  7],
     [17,  1,  5,  7,  7],
     [17,  2,  4,  7,  8],
     [18,  1,  4,  8,  8],
     [18,  2,  5,  7,  8],
     [19,  1,  5,  8,  8]],
    [[10,  1,  6,  6,  6],
     [11,  3,  6,  6,  7],
     [12,  3,  6,  6,  8],
     [13,  3,  6,  7,  7],
     [14,  6,  6,  7,  8],
     [15,  3,  6,  8,  8],
     [16,  1,  7,  7,  7],
     [17,  3,  7,  7,  8],
     [18,  3,  7,  8,  8],
     [19,  1,  8,  8,  8]],
    [[20,  1,  0,  0,  0,  0],
     [21,  4,  0,  0,  0,  1],
     [22,  4,  0,  0,  0,  2],
     [23,  6,  0,  0,  1,  1],
     [24, 12,  0,  0,  1,  2],
     [25,  6,  0,  0,  2,  2],
     [26,  4,  0,  1,  1,  1],
     [27, 12,  0,  1,  1,  2],
     [28, 12,  0,  1,  2,  2],
     [29,  4,  0,  2,  2,  2],
     [30,  1,  1,  1,  1,  1],
     [31,  4,  1,  1,  1,  2],
     [32,  6,  1,  1,  2,  2],
     [33,  4,  1,  2,  2,  2],
     [34,  1,  2,  2,  2,  2]],
    [[20,  1,  0,  0,  0,  3],
     [21,  1,  0,  0,  0,  4],
     [21,  3,  0,  0,  1,  3],
     [22,  1,  0,  0,  0,  5],
     [22,  3,  0,  0,  2,  3],
     [23,  3,  0,  1,  1,  3],
     [23,  3,  0,  0,  1,  4],
     [24,  3,  0,  0,  2,  4],
     [24,  3,  0,  0,  1,  5],
     [24,  6,  0,  1,  2,  3],
     [25,  3,  0,  2,  2,  3],
     [25,  3,  0,  0,  2,  5],
     [26,  1,  1,  1,  1,  3],
     [26,  3,  0,  1,  1,  4],
     [27,  3,  1,  1,  2,  3],
     [27,  3,  0,  1,  1,  5],
     [27,  6,  0,  1,  2,  4],
     [28,  3,  1,  2,  2,  3],
     [28,  3,  0,  2,  2,  4],
     [28,  6,  0,  1,  2,  5],
     [29,  1,  2,  2,  2,  3],
     [29,  3,  0,  2,  2,  5],
     [30,  1,  1,  1,  1,  4],
     [31,  1,  1,  1,  1,  5],
     [31,  3,  1,  1,  2,  4],
     [32,  3,  1,  2,  2,  4],
     [32,  3,  1,  1,  2,  5],
     [33,  1,  2,  2,  2,  4],
     [33,  3,  1,  2,  2,  5],
     [34,  1,  2,  2,  2,  5]],
    [[20,  1,  0,  0,  0,  6],
     [21,  1,  0,  0,  0,  7],
     [21,  3,  0,  0,  1,  6],
     [22,  1,  0,  0,  0,  8],
     [22,  3,  0,  0,  2,  6],
     [23,  3,  0,  1,  1,  6],
     [23,  3,  0,  0,  1,  7],
     [24,  3,  0,  0,  2,  7],
     [24,  3,  0,  0,  1,  8],
     [24,  6,  0,  1,  2,  6],
     [25,  3,  0,  2,  2,  6],
     [25,  3,  0,  0,  2,  8],
     [26,  1,  1,  1,  1,  6],
     [26,  3,  0,  1,  1,  7],
     [27,  3,  1,  1,  2,  6],
     [27,  3,  0,  1,  1,  8],
     [27,  6,  0,  1,  2,  7],
     [28,  3,  1,  2,  2,  6],
     [28,  3,  0,  2,  2,  7],
     [28,  6,  0,  1,  2,  8],
     [29,  1,  2,  2,  2,  6],
     [29,  3,  0,  2,  2,  8],
     [30,  1,  1,  1,  1,  7],
     [31,  1,  1,  1,  1,  8],
     [31,  3,  1,  1,  2,  7],
     [32,  3,  1,  2,  2,  7],
     [32,  3,  1,  1,  2,  8],
     [33,  1,  2,  2,  2,  7],
     [33,  3,  1,  2,  2,  8],
     [34,  1,  2,  2,  2,  8]],
    [[20,  1,  0,  0,  3,  3],
     [21,  2,  0,  1,  3,  3],
     [21,  2,  0,  0,  3,  4],
     [22,  2,  0,  2,  3,  3],
     [22,  2,  0,  0,  3,  5],
     [23,  1,  1,  1,  3,  3],
     [23,  1,  0,  0,  4,  4],
     [23,  4,  0,  1,  3,  4],
     [24,  2,  1,  2,  3,  3],
     [24,  2,  0,  0,  4,  5],
     [24,  4,  0,  2,  3,  4],
     [24,  4,  0,  1,  3,  5],
     [25,  1,  2,  2,  3,  3],
     [25,  1,  0,  0,  5,  5],
     [25,  4,  0,  2,  3,  5],
     [26,  2,  1,  1,  3,  4],
     [26,  2,  0,  1,  4,  4],
     [27,  2,  1,  1,  3,  5],
     [27,  2,  0,  2,  4,  4],
     [27,  4,  1,  2,  3,  4],
     [27,  4,  0,  1,  4,  5],
     [28,  2,  2,  2,  3,  4],
     [28,  2,  0,  1,  5,  5],
     [28,  4,  1,  2,  3,  5],
     [28,  4,  0,  2,  4,  5],
     [29,  2,  2,  2,  3,  5],
     [29,  2,  0,  2,  5,  5],
     [30,  1,  1,  1,  4,  4],
     [31,  2,  1,  2,  4,  4],
     [31,  2,  1,  1,  4,  5],
     [32,  1,  2,  2,  4,  4],
     [32,  1,  1,  1,  5,  5],
     [32,  4,  1,  2,  4,  5],
     [33,  2,  2,  2,  4,  5],
     [33,  2,  1,  2,  5,  5],
     [34,  1,  2,  2,  5,  5]],
    [[20,  1,  0,  0,  3,  6],
     [21,  1,  0,  0,  4,  6],
     [21,  1,  0,  0,  3,  7],
     [21,  2,  0,  1,  3,  6],
     [22,  1,  0,  0,  5,  6],
     [22,  1,  0,  0,  3,  8],
     [22,  2,  0,  2,  3,  6],
     [23,  1,  1,  1,  3,  6],
     [23,  1,  0,  0,  4,  7],
     [23,  2,  0,  1,  4,  6],
     [23,  2,  0,  1,  3,  7],
     [24,  1,  0,  0,  5,  7],
     [24,  1,  0,  0,  4,  8],
     [24,  2,  1,  2,  3,  6],
     [24,  2,  0,  2,  4,  6],
     [24,  2,  0,  2,  3,  7],
     [24,  2,  0,  1,  5,  6],
     [24,  2,  0,  1,  3,  8],
     [25,  1,  2,  2,  3,  6],
     [25,  1,  0,  0,  5,  8],
     [25,  2,  0,  2,  5,  6],
     [25,  2,  0,  2,  3,  8],
     [26,  1,  1,  1,  4,  6],
     [26,  1,  1,  1,  3,  7],
     [26,  2,  0,  1,  4,  7],
     [27,  1,  1,  1,  5,  6],
     [27,  1,  1,  1,  3,  8],
     [27,  2,  1,  2,  4,  6],
     [27,  2,  1,  2,  3,  7],
     [27,  2,  0,  2,  4,  7],
     [27,  2,  0,  1,  5,  7],
     [27,  2,  0,  1,  4,  8],
     [28,  1,  2,  2,  4,  6],
     [28,  1,  2,  2,  3,  7],
     [28,  2,  1,  2,  5,  6],
     [28,  2,  1,  2,  3,  8],
     [28,  2,  0,  2,  5,  7],
     [28,  2,  0,  2,  4,  8],
     [28,  2,  0,  1,  5,  8],
     [29,  1,  2,  2,  5,  6],
     [29,  1,  2,  2,  3,  8],
     [29,  2,  0,  2,  5,  8],
     [30,  1,  1,  1,  4,  7],
     [31,  1,  1,  1,  5,  7],
     [31,  1,  1,  1,  4,  8],
     [31,  2,  1,  2,  4,  7],
     [32,  1,  2,  2,  4,  7],
     [32,  1,  1,  1,  5,  8],
     [32,  2,  1,  2,  5,  7],
     [32,  2,  1,  2,  4,  8],
     [33,  1,  2,  2,  5,  7],
     [33,  1,  2,  2,  4,  8],
     [33,  2,  1,  2,  5,  8],
     [34,  1,  2,  2,  5,  8]],
    [[20,  1,  0,  0,  6,  6],
     [21,  2,  0,  1,  6,  6],
     [21,  2,  0,  0,  6,  7],
     [22,  2,  0,  2,  6,  6],
     [22,  2,  0,  0,  6,  8],
     [23,  1,  1,  1,  6,  6],
     [23,  1,  0,  0,  7,  7],
     [23,  4,  0,  1,  6,  7],
     [24,  2,  1,  2,  6,  6],
     [24,  2,  0,  0,  7,  8],
     [24,  4,  0,  2,  6,  7],
     [24,  4,  0,  1,  6,  8],
     [25,  1,  2,  2,  6,  6],
     [25,  1,  0,  0,  8,  8],
     [25,  4,  0,  2,  6,  8],
     [26,  2,  1,  1,  6,  7],
     [26,  2,  0,  1,  7,  7],
     [27,  2,  1,  1,  6,  8],
     [27,  2,  0,  2,  7,  7],
     [27,  4,  1,  2,  6,  7],
     [27,  4,  0,  1,  7,  8],
     [28,  2,  2,  2,  6,  7],
     [28,  2,  0,  1,  8,  8],
     [28,  4,  1,  2,  6,  8],
     [28,  4,  0,  2,  7,  8],
     [29,  2,  2,  2,  6,  8],
     [29,  2,  0,  2,  8,  8],
     [30,  1,  1,  1,  7,  7],
     [31,  2,  1,  2,  7,  7],
     [31,  2,  1,  1,  7,  8],
     [32,  1,  2,  2,  7,  7],
     [32,  1,  1,  1,  8,  8],
     [32,  4,  1,  2,  7,  8],
     [33,  2,  2,  2,  7,  8],
     [33,  2,  1,  2,  8,  8],
     [34,  1,  2,  2,  8,  8]],
    [[20,  1,  0,  3,  3,  3],
     [21,  1,  1,  3,  3,  3],
     [21,  3,  0,  3,  3,  4],
     [22,  1,  2,  3,  3,  3],
     [22,  3,  0,  3,  3,  5],
     [23,  3,  1,  3,  3,  4],
     [23,  3,  0,  3,  4,  4],
     [24,  3,  2,  3,  3,  4],
     [24,  3,  1,  3,  3,  5],
     [24,  6,  0,  3,  4,  5],
     [25,  3,  2,  3,  3,  5],
     [25,  3,  0,  3,  5,  5],
     [26,  1,  0,  4,  4,  4],
     [26,  3,  1,  3,  4,  4],
     [27,  3,  2,  3,  4,  4],
     [27,  3,  0,  4,  4,  5],
     [27,  6,  1,  3,  4,  5],
     [28,  3,  1,  3,  5,  5],
     [28,  3,  0,  4,  5,  5],
     [28,  6,  2,  3,  4,  5],
     [29,  1,  0,  5,  5,  5],
     [29,  3,  2,  3,  5,  5],
     [30,  1,  1,  4,  4,  4],
     [31,  1,  2,  4,  4,  4],
     [31,  3,  1,  4,  4,  5],
     [32,  3,  2,  4,  4,  5],
     [32,  3,  1,  4,  5,  5],
     [33,  1,  1,  5,  5,  5],
     [33,  3,  2,  4,  5,  5],
     [34,  1,  2,  5,  5,  5]],
    [[20,  1,  0,  3,  3,  6],
     [21,  1,  1,  3,  3,  6],
     [21,  1,  0,  3,  3,  7],
     [21,  2,  0,  3,  4,  6],
     [22,  1,  2,  3,  3,  6],
     [22,  1,  0,  3,  3,  8],
     [22,  2,  0,  3,  5,  6],
     [23,  1,  1,  3,  3,  7],
     [23,  1,  0,  4,  4,  6],
     [23,  2,  1,  3,  4,  6],
     [23,  2,  0,  3,  4,  7],
     [24,  1,  2,  3,  3,  7],
     [24,  1,  1,  3,  3,  8],
     [24,  2,  2,  3,  4,  6],
     [24,  2,  1,  3,  5,  6],
     [24,  2,  0,  4,  5,  6],
     [24,  2,  0,  3,  5,  7],
     [24,  2,  0,  3,  4,  8],
     [25,  1,  2,  3,  3,  8],
     [25,  1,  0,  5,  5,  6],
     [25,  2,  2,  3,  5,  6],
     [25,  2,  0,  3,  5,  8],
     [26,  1,  1,  4,  4,  6],
     [26,  1,  0,  4,  4,  7],
     [26,  2,  1,  3,  4,  7],
     [27,  1,  2,  4,  4,  6],
     [27,  1,  0,  4,  4,  8],
     [27,  2,  2,  3,  4,  7],
     [27,  2,  1,  4,  5,  6],
     [27,  2,  1,  3,  5,  7],
     [27,  2,  1,  3,  4,  8],
     [27,  2,  0,  4,  5,  7],
     [28,  1,  1,  5,  5,  6],
     [28,  1,  0,  5,  5,  7],
     [28,  2,  2,  4,  5,  6],
     [28,  2,  2,  3,  5,  7],
     [28,  2,  2,  3,  4,  8],
     [28,  2,  1,  3,  5,  8],
     [28,  2,  0,  4,  5,  8],
     [29,  1,  2,  5,  5,  6],
     [29,  1,  0,  5,  5,  8],
     [29,  2,  2,  3,  5,  8],
     [30,  1,  1,  4,  4,  7],
     [31,  1,  2,  4,  4,  7],
     [31,  1,  1,  4,  4,  8],
     [31,  2,  1,  4,  5,  7],
     [32,  1,  2,  4,  4,  8],
     [32,  1,  1,  5,  5,  7],
     [32,  2,  2,  4,  5,  7],
     [32,  2,  1,  4,  5,  8],
     [33,  1,  2,  5,  5,  7],
     [33,  1,  1,  5,  5,  8],
     [33,  2,  2,  4,  5,  8],
     [34,  1,  2,  5,  5,  8]],
    [[20,  1,  0,  3,  6,  6],
     [21,  1,  1,  3,  6,  6],
     [21,  1,  0,  4,  6,  6],
     [21,  2,  0,  3,  6,  7],
     [22,  1,  2,  3,  6,  6],
     [22,  1,  0,  5,  6,  6],
     [22,  2,  0,  3,  6,  8],
     [23,  1,  1,  4,  6,  6],
     [23,  1,  0,  3,  7,  7],
     [23,  2,  1,  3,  6,  7],
     [23,  2,  0,  4,  6,  7],
     [24,  1,  2,  4,  6,  6],
     [24,  1,  1,  5,  6,  6],
     [24,  2,  2,  3,  6,  7],
     [24,  2,  1,  3,  6,  8],
     [24,  2,  0,  5,  6,  7],
     [24,  2,  0,  4,  6,  8],
     [24,  2,  0,  3,  7,  8],
     [25,  1,  2,  5,  6,  6],
     [25,  1,  0,  3,  8,  8],
     [25,  2,  2,  3,  6,  8],
     [25,  2,  0,  5,  6,  8],
     [26,  1,  1,  3,  7,  7],
     [26,  1,  0,  4,  7,  7],
     [26,  2,  1,  4,  6,  7],
     [27,  1,  2,  3,  7,  7],
     [27,  1,  0,  5,  7,  7],
     [27,  2,  2,  4,  6,  7],
     [27,  2,  1,  5,  6,  7],
     [27,  2,  1,  4,  6,  8],
     [27,  2,  1,  3,  7,  8],
     [27,  2,  0,  4,  7,  8],
     [28,  1,  1,  3,  8,  8],
     [28,  1,  0,  4,  8,  8],
     [28,  2,  2,  5,  6,  7],
     [28,  2,  2,  4,  6,  8],
     [28,  2,  2,  3,  7,  8],
     [28,  2,  1,  5,  6,  8],
     [28,  2,  0,  5,  7,  8],
     [29,  1,  2,  3,  8,  8],
     [29,  1,  0,  5,  8,  8],
     [29,  2,  2,  5,  6,  8],
     [30,  1,  1,  4,  7,  7],
     [31,  1,  2,  4,  7,  7],
     [31,  1,  1,  5,  7,  7],
     [31,  2,  1,  4,  7,  8],
     [32,  1,  2,  5,  7,  7],
     [32,  1,  1,  4,  8,  8],
     [32,  2,  2,  4,  7,  8],
     [32,  2,  1,  5,  7,  8],
     [33,  1,  2,  4,  8,  8],
     [33,  1,  1,  5,  8,  8],
     [33,  2,  2,  5,  7,  8],
     [34,  1,  2,  5,  8,  8]],
    [[20,  1,  0,  6,  6,  6],
     [21,  1,  1,  6,  6,  6],
     [21,  3,  0,  6,  6,  7],
     [22,  1,  2,  6,  6,  6],
     [22,  3,  0,  6,  6,  8],
     [23,  3,  1,  6,  6,  7],
     [23,  3,  0,  6,  7,  7],
     [24,  3,  2,  6,  6,  7],
     [24,  3,  1,  6,  6,  8],
     [24,  6,  0,  6,  7,  8],
     [25,  3,  2,  6,  6,  8],
     [25,  3,  0,  6,  8,  8],
     [26,  1,  0,  7,  7,  7],
     [26,  3,  1,  6,  7,  7],
     [27,  3,  2,  6,  7,  7],
     [27,  3,  0,  7,  7,  8],
     [27,  6,  1,  6,  7,  8],
     [28,  3,  1,  6,  8,  8],
     [28,  3,  0,  7,  8,  8],
     [28,  6,  2,  6,  7,  8],
     [29,  1,  0,  8,  8,  8],
     [29,  3,  2,  6,  8,  8],
     [30,  1,  1,  7,  7,  7],
     [31,  1,  2,  7,  7,  7],
     [31,  3,  1,  7,  7,  8],
     [32,  3,  2,  7,  7,  8],
     [32,  3,  1,  7,  8,  8],
     [33,  1,  1,  8,  8,  8],
     [33,  3,  2,  7,  8,  8],
     [34,  1,  2,  8,  8,  8]],
    [[20,  1,  3,  3,  3,  3],
     [21,  4,  3,  3,  3,  4],
     [22,  4,  3,  3,  3,  5],
     [23,  6,  3,  3,  4,  4],
     [24, 12,  3,  3,  4,  5],
     [25,  6,  3,  3,  5,  5],
     [26,  4,  3,  4,  4,  4],
     [27, 12,  3,  4,  4,  5],
     [28, 12,  3,  4,  5,  5],
     [29,  4,  3,  5,  5,  5],
     [30,  1,  4,  4,  4,  4],
     [31,  4,  4,  4,  4,  5],
     [32,  6,  4,  4,  5,  5],
     [33,  4,  4,  5,  5,  5],
     [34,  1,  5,  5,  5,  5]],
    [[20,  1,  3,  3,  3,  6],
     [21,  1,  3,  3,  3,  7],
     [21,  3,  3,  3,  4,  6],
     [22,  1,  3,  3,  3,  8],
     [22,  3,  3,  3,  5,  6],
     [23,  3,  3,  4,  4,  6],
     [23,  3,  3,  3,  4,  7],
     [24,  3,  3,  3,  5,  7],
     [24,  3,  3,  3,  4,  8],
     [24,  6,  3,  4,  5,  6],
     [25,  3,  3,  5,  5,  6],
     [25,  3,  3,  3,  5,  8],
     [26,  1,  4,  4,  4,  6],
     [26,  3,  3,  4,  4,  7],
     [27,  3,  4,  4,  5,  6],
     [27,  3,  3,  4,  4,  8],
     [27,  6,  3,  4,  5,  7],
     [28,  3,  4,  5,  5,  6],
     [28,  3,  3,  5,  5,  7],
     [28,  6,  3,  4,  5,  8],
     [29,  1,  5,  5,  5,  6],
     [29,  3,  3,  5,  5,  8],
     [30,  1,  4,  4,  4,  7],
     [31,  1,  4,  4,  4,  8],
     [31,  3,  4,  4,  5,  7],
     [32,  3,  4,  5,  5,  7],
     [32,  3,  4,  4,  5,  8],
     [33,  1,  5,  5,  5,  7],
     [33,  3,  4,  5,  5,  8],
     [34,  1,  5,  5,  5,  8]],
    [[20,  1,  3,  3,  6,  6],
     [21,  2,  3,  4,  6,  6],
     [21,  2,  3,  3,  6,  7],
     [22,  2,  3,  5,  6,  6],
     [22,  2,  3,  3,  6,  8],
     [23,  1,  4,  4,  6,  6],
     [23,  1,  3,  3,  7,  7],
     [23,  4,  3,  4,  6,  7],
     [24,  2,  4,  5,  6,  6],
     [24,  2,  3,  3,  7,  8],
     [24,  4,  3,  5,  6,  7],
     [24,  4,  3,  4,  6,  8],
     [25,  1,  5,  5,  6,  6],
     [25,  1,  3,  3,  8,  8],
     [25,  4,  3,  5,  6,  8],
     [26,  2,  4,  4,  6,  7],
     [26,  2,  3,  4,  7,  7],
     [27,  2,  4,  4,  6,  8],
     [27,  2,  3,  5,  7,  7],
     [27,  4,  4,  5,  6,  7],
     [27,  4,  3,  4,  7,  8],
     [28,  2,  5,  5,  6,  7],
     [28,  2,  3,  4,  8,  8],
     [28,  4,  4,  5,  6,  8],
     [28,  4,  3,  5,  7,  8],
     [29,  2,  5,  5,  6,  8],
     [29,  2,  3,  5,  8,  8],
     [30,  1,  4,  4,  7,  7],
     [31,  2,  4,  5,  7,  7],
     [31,  2,  4,  4,  7,  8],
     [32,  1,  5,  5,  7,  7],
     [32,  1,  4,  4,  8,  8],
     [32,  4,  4,  5,  7,  8],
     [33,  2,  5,  5,  7,  8],
     [33,  2,  4,  5,  8,  8],
     [34,  1,  5,  5,  8,  8]],
    [[20,  1,  3,  6,  6,  6],
     [21,  1,  4,  6,  6,  6],
     [21,  3,  3,  6,  6,  7],
     [22,  1,  5,  6,  6,  6],
     [22,  3,  3,  6,  6,  8],
     [23,  3,  4,  6,  6,  7],
     [23,  3,  3,  6,  7,  7],
     [24,  3,  5,  6,  6,  7],
     [24,  3,  4,  6,  6,  8],
     [24,  6,  3,  6,  7,  8],
     [25,  3,  5,  6,  6,  8],
     [25,  3,  3,  6,  8,  8],
     [26,  1,  3,  7,  7,  7],
     [26,  3,  4,  6,  7,  7],
     [27,  3,  5,  6,  7,  7],
     [27,  3,  3,  7,  7,  8],
     [27,  6,  4,  6,  7,  8],
     [28,  3,  4,  6,  8,  8],
     [28,  3,  3,  7,  8,  8],
     [28,  6,  5,  6,  7,  8],
     [29,  1,  3,  8,  8,  8],
     [29,  3,  5,  6,  8,  8],
     [30,  1,  4,  7,  7,  7],
     [31,  1,  5,  7,  7,  7],
     [31,  3,  4,  7,  7,  8],
     [32,  3,  5,  7,  7,  8],
     [32,  3,  4,  7,  8,  8],
     [33,  1,  4,  8,  8,  8],
     [33,  3,  5,  7,  8,  8],
     [34,  1,  5,  8,  8,  8]],
    [[20,  1,  6,  6,  6,  6],
     [21,  4,  6,  6,  6,  7],
     [22,  4,  6,  6,  6,  8],
     [23,  6,  6,  6,  7,  7],
     [24, 12,  6,  6,  7,  8],
     [25,  6,  6,  6,  8,  8],
     [26,  4,  6,  7,  7,  7],
     [27, 12,  6,  7,  7,  8],
     [28, 12,  6,  7,  8,  8],
     [29,  4,  6,  8,  8,  8],
     [30,  1,  7,  7,  7,  7],
     [31,  4,  7,  7,  7,  8],
     [32,  6,  7,  7,  8,  8],
     [33,  4,  7,  8,  8,  8],
     [34,  1,  8,  8,  8,  8]],
]


def rotate_cartesian_moments(moments, rmat):
    '''Rotate cartesian moments

       **Arguments:**

       moments
            A row vector with a series of cartesian multipole moments. Items in
            this vector should follow the same order as defined by the function
            ``get_cartesian_powers``.

       rmat
            A (3,3) rotation matrix.
    '''
    ncart = moments.shape[0]
    result = np.zeros(ncart)
    for i in xrange(ncart):
        result[i] = rotate_moments_low(cartesian_transforms[i], rmat, moments)
    return result


def rotate_moments_low(rules, rmat, moments):
    '''Return rotated a multipole based on the given rules

       **Arguments:**

       moments
            A row vector with a series of cartesian multipole moments. Items in
            this vector should follow the same order as defined by the function
            ``get_cartesian_powers``.

       rules
            An item from the list cartesian_transforms.

       rmat
            A (3,3) rotation matrix.
    '''
    rcoeffs = rmat.ravel()
    result = 0
    for rule in rules:
        i = rule[0]
        factor = rule[1]
        for j in rule[2:]:
           factor *= rcoeffs[j]
        result += moments[i]*factor
    return result


def get_npure(l):
    '''The number of pure functions for a given angular momentum, l'''
    return 2*l+1


def get_npure_cumul(lmax):
    '''The number of pure functions up to a given angular momentum, lmax.'''
    return (lmax+1)**2
