#!/usr/bin/python3
# -*- coding: utf8 -*-
# paperboxmaker.py
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Author: Niels Kjøller Hansen <niels.k.h@gmail.com>
"""A script for making foldable, glueless boxes.

Depends on svgwrite
"""

import svgwrite
import sys


# Dimensions are inner dimensions
BOX_WIDTH = 59.5 + 2
BOX_HEIGHT = 90 + 2
BOX_DEPTH = 36.0*0.5
PAPER_THICKNESS = 0.2
LID_DEPTH_PERCENTAGE = 50.0 # Currently not used
FILENAME = 'test.svg'

PAPER_WIDTH = 210
PAPER_HEIGHT = 297
MIN_MARGIN_TOP_BOTTOM = 13
MIN_MARGIN_LEFT_RIGHT = 6

# Conversion factors
PX_TO_MM = 25.4/90
MM_TO_PX = 90/25.4

# Derived
# TODO: Make variable names make more sense

USABLE_WIDTH = PAPER_WIDTH - 2 * MIN_MARGIN_LEFT_RIGHT
USABLE_HEIGHT = PAPER_HEIGHT - 2 * MIN_MARGIN_TOP_BOTTOM

PAPER_THICKNESS_PX = PAPER_THICKNESS * MM_TO_PX
BOX_WIDTH_PX = BOX_WIDTH * MM_TO_PX
BOX_HEIGHT_PX = BOX_HEIGHT * MM_TO_PX
BOX_DEPTH_PX = BOX_DEPTH * MM_TO_PX
BOX_WIDTH_PX_OUTER = BOX_WIDTH_PX + 2 * PAPER_THICKNESS_PX
BOX_HEIGHT_PX_OUTER = BOX_HEIGHT_PX + 2 * PAPER_THICKNESS_PX
BOX_DEPTH_PX_OUTER = BOX_DEPTH_PX + 2 * PAPER_THICKNESS_PX

LID_WIDTH_PX = BOX_WIDTH_PX + 4 * PAPER_THICKNESS_PX
LID_HEIGHT_PX = BOX_HEIGHT_PX + 4 * PAPER_THICKNESS_PX
LID_DEPTH_PX = BOX_DEPTH_PX * LID_DEPTH_PERCENTAGE
LID_DEPTH_PX_OUTER = LID_DEPTH_PX + 2 * PAPER_THICKNESS_PX

BOX_TOTAL_HEIGHT = 4.5 * BOX_DEPTH_PX_OUTER + 2 * BOX_HEIGHT_PX_OUTER
BOX_TOTAL_WIDTH = 5 * BOX_DEPTH_PX_OUTER + BOX_WIDTH_PX_OUTER

BOX_CENTER_X = PAPER_WIDTH / 2 * MM_TO_PX
BOX_CENTER_Y = MIN_MARGIN_TOP_BOTTOM * MM_TO_PX + 2.5 * BOX_DEPTH_PX_OUTER + BOX_HEIGHT_PX_OUTER/2

START_X = BOX_CENTER_X - BOX_WIDTH_PX_OUTER / 2
START_Y = BOX_CENTER_Y - BOX_HEIGHT_PX_OUTER / 2 - BOX_DEPTH_PX_OUTER


def make_box(origin, depth, width, height, stroke_width="1",
                                           stroke="black",
                                           fill="rgb(255,255,255)",
                                           fill_opacity=1):
    group = svgwrite.container.Group()
    path = svgwrite.path.Path(d="M%f,%f" % origin,
                              stroke_width=stroke_width,
                              stroke=stroke,
                              fill=fill,
                              fill_opacity=fill_opacity)
    path.push("v-%f" % depth)
    path.push("l%f,-%f" % (depth/2, depth/2))
    path.push("h%f" % (width - depth))
    path.push("l%f,%f" % (depth/2, depth/2))
    path.push("v%f" % depth)
    path.push("a%f,%f,0,0,1,%f,%f" % (depth,depth,depth,depth))

    path.push("h%f" % depth)
    path.push("l%f,%f" % (depth/2, depth/2))
    path.push("v%f" % (height - depth))
    path.push("l-%f,%f" % (depth/2, depth/2))
    path.push("h-%f" % depth)
    path.push("a%f,%f,0,0,1,-%f,%f" % (depth,depth,depth,depth))

    path.push("v%f" % (depth+height))
    path.push("h-%f" % width)
    path.push("v-%f" % (depth+height))
    path.push("a%f,%f,0,0,1,-%f,-%f" % (depth,depth,depth,depth))

    path.push("h-%f" % depth)
    path.push("l-%f,-%f" % (depth/2, depth/2))
    path.push("v-%f" % (height - depth))
    path.push("l%f,-%f" % (depth/2, depth/2))
    path.push("h%f" % depth)
    path.push("a%f,%f,0,0,1,%f,-%f" % (depth,depth,depth,depth))

    path.push("z")
    group.add(path)

    # Add the folding lines in the corners
    group.add(svgwrite.path.Path(d="M%f,%f l-%f,-%f" % (origin[0],origin[1]+depth,depth/1.4142, depth/1.4142),stroke=stroke,stroke_width=stroke_width, stroke_dasharray="2,1" ,fill=fill, fill_opacity=fill_opacity))
    group.add(svgwrite.path.Path(d="M%f,%f l-%f,%f" % (origin[0],origin[1]+depth+height,depth/1.4142, depth/1.4142),stroke=stroke,stroke_width=stroke_width, stroke_dasharray="2,1" ,fill=fill, fill_opacity=fill_opacity))
    group.add(svgwrite.path.Path(d="M%f,%f l%f,-%f" % (origin[0]+width,origin[1]+depth,depth/1.4142, depth/1.4142),stroke=stroke,stroke_width=stroke_width, stroke_dasharray="2,1" ,fill=fill, fill_opacity=fill_opacity))
    group.add(svgwrite.path.Path(d="M%f,%f l%f,%f" % (origin[0]+width,origin[1]+depth+height,depth/1.4142, depth/1.4142),stroke=stroke,stroke_width=stroke_width, stroke_dasharray="2,1" ,fill=fill, fill_opacity=fill_opacity))

    group.add(svgwrite.path.Path(d="M%f,%f h-%f" % (origin[0],origin[1]+3*depth+height,depth/2),stroke=stroke,stroke_width=stroke_width, stroke_dasharray="2,1" ,fill=fill, fill_opacity=fill_opacity))
    group.add(svgwrite.path.Path(d="M%f,%f h%f" % (origin[0]+width,origin[1]+3*depth+height,depth/2),stroke=stroke,stroke_width=stroke_width, stroke_dasharray="2,1" ,fill=fill, fill_opacity=fill_opacity))

    return group

# Check if drawing will fit on paper
if BOX_TOTAL_HEIGHT > USABLE_HEIGHT*MM_TO_PX or BOX_TOTAL_WIDTH > USABLE_WIDTH*MM_TO_PX:
    print(BOX_TOTAL_HEIGHT, " ", USABLE_HEIGHT*MM_TO_PX)
    print(BOX_TOTAL_WIDTH, " ", USABLE_WIDTH*MM_TO_PX)
    print("Det passer ikke på papiret")
    #sys.exit(0)

svg_document = svgwrite.Drawing(filename=FILENAME,
                                size= ("210mm", "297mm"))

svg_document.add(make_box((START_X,START_Y),BOX_DEPTH_PX_OUTER,BOX_WIDTH_PX_OUTER,BOX_HEIGHT_PX_OUTER))
svg_document.save()
