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

# Previous version
#def render(fin, fout):
#    view = pyrr.matrix44.create_look_at(eye=[40, 100, 10], target=[0, 0, 0], up=[0, 0, 1])
#   # projection = pyrr.matrix44.create_orthogonal_projection(left=-10, right=10, bottom=-10, top=10, near=1, far=200)
#    projection = pyrr.matrix44.create_perspective_projection(fovy=25, aspect=1, near=1, far=200)
#    camera = svg3d.Camera(view, projection)
#
#    shapes = get_shapes(fin)
#    meshes = []
#    for shape in shapes[0:7]:
#        style = dict(
#            fill="white", fill_opacity="1",
#            stoke="none", stoke_linejoin="round", stoke_width="0.00")
#
#        if shape.appearance != None:
#            diffuse_color = shape.appearance.material.diffuseColor
#            transparency = shape.appearance.material.transparency
#            style = dict(fill=rgb(*diffuse_color), stroke="none", stroke_width="0.000", stroke_linejoin="round")
#
#        if shape.geometry != None:
#            triangles = np.int32(shape.geometry.coordIndex)
#            verts = np.float32(shape.geometry.coord.point)
#            
#            mesh = svg3d.Mesh(15*verts[triangles], style=style)
#            meshes += [mesh]
#
#    view = svg3d.View(camera, svg3d.Scene(meshes))
#    svg3d.Engine([view]).render(fout)

def render(fin, fout):
    shapes = get_shapes(fin)

    # test with one first
    shape = shapes[-1]
    triangles = np.int32(shape.geometry.coordIndex)
    verts = np.float32(shape.geometry.coord.point)
    faces = verts[triangles]

    # model matrix
    model = pyrr.Matrix44.identity()
    # view matrix
    view = pyrr.matrix44.create_look_at(eye=[0, 10, 0], target=[0, 0, 0], up=[0, 0, 1])
    # projection matrix
    projection = pyrr.matrix44.create_orthogonal_projection(left=-10, right=10, bottom=-10, top=10, near=1, far=100)

    # create svg drawing
    drawing = svgwrite.Drawing(fout, (512, 512), viewBox="-0.5 -0.5 1.0 1.0")
    precision = 5
    group = drawing.g()
    for face in faces:
        face = np.around(face[:, :2], precision)
        group.add(drawing.polygon(face, fill="red"))
    drawing.add(g)
    drawing.save()
