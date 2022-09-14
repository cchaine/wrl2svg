#           __        _
#  ________/ /  ___ _(_)__  ___
# / __/ __/ _ \/ _ `/ / _ \/ -_)
# \__/\__/_//_/\_,_/_/_//_/\__/
# 
# Copyright (C) Clément Chaine
# This file is part of wrl2svg <https://github.com/cchaine/wrl2svg>
# 
# wrl2svg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# wrl2svg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with wrl2svg.  If not, see <http://www.gnu.org/licenses/>.

import sys
import svg3d, pyrr, math
from wrlparser import parse_file, Shape
import numpy as np
import svgwrite

def get_shapes(model):
    scene = parse_file(model)
    shapes = []
    for node in scene.nodes:
        if type(node) == Shape:
            shapes += [node]
    return shapes

def rgb(r, g, b):
    r = max(0.0, min(r, 1.0))
    g = max(0.0, min(g, 1.0))
    b = max(0.0, min(b, 1.0))
    return svgwrite.utils.rgb(r * 255, g * 255, b * 255)

def render(fin, fout):
    view = pyrr.matrix44.create_look_at(eye=[40, 100, 10], target=[0, 0, 0], up=[0, 0, 1])
   # projection = pyrr.matrix44.create_orthogonal_projection(left=-10, right=10, bottom=-10, top=10, near=1, far=200)
    projection = pyrr.matrix44.create_perspective_projection(fovy=25, aspect=1, near=1, far=200)
    camera = svg3d.Camera(view, projection)

    shapes = get_shapes(fin)
    meshes = []
    for shape in shapes:
        style = dict(
            fill="white", fill_opacity="1",
            stoke="none", stoke_linejoin="round", stoke_width="0.005")
        if shape.appearance != None:
            diffuse_color = shape.appearance.material.diffuseColor
            transparency = shape.appearance.material.transparency
            style = dict(fill=rgb(*diffuse_color), stroke="none", stroke_width="0.001", stroke_linejoin="round")
        if shape.geometry != None:
            triangles = np.int32(shape.geometry.coordIndex)
            verts = np.float32(shape.geometry.coord.point)
            mesh = svg3d.Mesh(15*verts[triangles], style=style)
            meshes += [mesh]

    view = svg3d.View(camera, svg3d.Scene(meshes))
    svg3d.Engine([view]).render(fout)
