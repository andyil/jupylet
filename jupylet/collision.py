"""
    jupylet/collision.py
    
    Copyright (c) 2020, Nir Aides - nir@winpdb.org

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import functools
import scipy
import math

import PIL.Image

import numpy as np


def affine(a=0, s=1, ax=0, ay=0, dx=0, dy=0):
    
    r = math.radians(a)
    a = math.cos(r) * s
    b = math.sin(r) * s
    
    return np.array([
        [a, b, -a*ax - b*ay + dx],
        [-b, a, b*ax - a*ay + dy],
        [0, 0, 1]
    ])


@functools.lru_cache(1024)
def trbl(width, height, anchor_x=0, anchor_y=0, angle=0, scale=1):
    
    bb0 = np.array([[width, height, 1], [width, 0, 1], [0, 0, 1], [0, height, 1]])
    bb1 = affine(angle, scale, anchor_x, anchor_y).dot(bb0.T).T
    bb2 = bb1.tolist()
    
    x = [v[0] for v in bb2]
    y = [v[1] for v in bb2]
    
    t, r, b, l = max(y), max(x), min(y), min(x)
    
    return t, r, b, l


def hitmap_and_outline_from_alpha(a):

    if isinstance(a, PIL.Image.Image):
        a = np.array(a)[...,3]

    k0 = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    
    a2 = (a > 128).astype('uint8')[::-1]
    a3 = scipy.signal.convolve2d(a2, k0, 'same') != 4
    a4 = a2 * a3
    a5 = np.stack(a4.nonzero()[::-1], -1)
    a6 = np.concatenate([a5, a5[:,:1] * 0 + 1], -1)
    
    h1, w1 = a2.shape
    xx = max(a2.shape) + 2

    a7 = np.pad(a2, ((1, xx - h1 - 1), (1, xx - w1 - 1)))

    return a7, a6


def collisions_from_hitmap_and_outline(a0, a1):
    a1 = np.core.umath.clip(a1, 0, a0.shape[0]-1)
    a2 = a0[a1[:,1], a1[:,0]]
    a3 = a1[a2.nonzero()]
    return a3

