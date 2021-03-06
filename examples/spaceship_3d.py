"""
    examples/spaceship_3d.py
    
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


import random
import struct
import time
import sys
import os

sys.path.insert(0, os.path.abspath('./..'))

import glm

import pyglet.window.key as key

from jupylet.label import Label
from jupylet.app import App, State
from jupylet.model import load_blender_gltf


if __name__ == '__main__':
    mode = 'window'
else:
    mode = 'hidden'

app = App(768, 512, mode=mode)

scene = load_blender_gltf('./scenes/moon/alien-moon.gltf')

scene.add_cubemap('./scenes/moon/nebula/nebula*.png', 2.)

camera = scene.cameras['Camera']
camera.zfar = 10000

moon = scene.meshes['Moon']


state = State(
    
    capslock = False,
    shift = False,
    alt = False,
    
    up = False,
    down = False,
    right = False,
    left = False,
    
    key_w = False,
    key_s = False,
    key_a = False,
    key_d = False,
    
    lv = glm.vec3(0),
    av = glm.vec3(0),
)


@app.event
def on_key_press(symbol, modifiers):
    on_key(symbol, modifiers, True)


@app.event
def on_key_release(symbol, modifiers):
    on_key(symbol, modifiers, False)
    

def on_key(symbol, modifiers, value):
    
    if symbol == key.CAPSLOCK and value:
        state.capslock = not state.capslock
        
    if symbol == key.LALT:
        state.alt = value
        
    if symbol == key.LSHIFT:
        state.shift = value
        
    if symbol == key.UP:
        state.up = value
        
    if symbol == key.DOWN:
        state.down = value
        
    if symbol == key.LEFT:
        state.left = value
        
    if symbol == key.RIGHT:
        state.right = value
        
    if symbol == key.W:
        state.key_w = value
        
    if symbol == key.S:
        state.key_s = value    
        
    if symbol == key.A:
        state.key_a = value
        
    if symbol == key.D:
        state.key_d = value


obj = moon if state.capslock else camera

linear_acceleration = 1 / 2
angular_acceleration = 1 / 24

@app.run_me_again_and_again(1/48)
def move_object(dt):
        
    global obj
    
    obj = moon if state.capslock else camera
    sign = -1 if obj is camera else 1
    
    if state.right and state.shift:
        state.av.z += angular_acceleration * sign
            
    if state.right and not state.shift:
        state.av.y -= angular_acceleration
        
    if state.left and state.shift:
        state.av.z -= angular_acceleration * sign
            
    if state.left and not state.shift:
        state.av.y += angular_acceleration
            
    if state.up:
        state.av.x -= angular_acceleration
        
    if state.down:
        state.av.x += angular_acceleration
        
    if state.key_w and state.alt:
        state.lv.y += linear_acceleration
                
    if state.key_w and not state.alt:
        state.lv.z += linear_acceleration * sign
                
    if state.key_s and state.alt:
        state.lv.y -= linear_acceleration
        
    if state.key_s and not state.alt:
        state.lv.z -= linear_acceleration * sign
        
    if state.key_a:
        state.lv.x += linear_acceleration * sign
        
    if state.key_d:
        state.lv.x -= linear_acceleration * sign
        
    state.lv = glm.clamp(state.lv, -64, 64)
    state.av = glm.clamp(state.av, -64, 64)
    
    obj.move_local(dt * state.lv)
    
    obj.rotate_local(dt * state.av.x, (1, 0, 0))
    obj.rotate_local(dt * state.av.y, (0, 1, 0))
    obj.rotate_local(dt * state.av.z, (0, 0, 1))
    
    state.lv *= 0.67 ** dt
    state.av *= 0.67 ** dt


label0 = Label('Hello World!', color='white', font_size=12, x=10, y=74)
label1 = Label('Hello World!', color='white', font_size=12, x=10, y=52)
label2 = Label('Hello World!', color='white', font_size=12, x=10, y=30)
label3 = Label('Hello World!', color='white', font_size=12, x=10, y=8)

hello_world = Label('Hello World 3D!', color='cyan', font_size=16, x=600, y=10)


dtl = [0]

@app.event
def on_draw():
        
    app.window.clear()
    app.set3d()    
    
    t0 = time.time()
    
    scene.draw()
    
    dtl.append(0.98 * dtl[-1] + 0.02 * (time.time() - t0))
    dtl[:] = dtl[-256:]
    
    app.set2d()
            
    label0.text = 'time to draw - %.2f ms' % (1000 * dtl[-1])
    label1.text = 'up - %r' % obj.up
    label2.text = 'front - %r' % obj.front
    label3.text = 'position - %r' % obj.position
    
    label0.draw()
    label1.draw()  
    label2.draw()  
    label3.draw()  

    hello_world.draw()


@app.schedule_interval(1/30)
def spin(dt):
    scene.meshes['Alien'].rotate_local(-0.5 * dt, (0, 0, 1))


scene.shadows = True


if __name__ == '__main__':
    app.run()

