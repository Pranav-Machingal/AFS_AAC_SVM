import os, io, random
import string
import numpy as np

import panel as pn
# import panel.widgets as pnw
pn.extension()

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Plot, Grid, Range1d
from bokeh.models.glyphs import Text, Rect
from bokeh.layouts import gridplot
from bokeh.colors import RGB

def _get_color(attr):
  # clip values to prevent CSS errors (Values should be from [-1,1])
  attr = max(-1, min(1, attr))
  r=0
  g=0
  b=0
  a=1
  if attr > 0:
    g = 255
    a = attr
  elif attr<0:
    r = 255
    a = -attr
  return RGB(r,g,b,a)

# def _get_color(attr):
#   # clip values to prevent CSS errors (Values should be from [-1,1])
#   attr = max(-1, min(1, attr))
#   r=0.001
#   g=0.001
#   b=0
#   a=1
#   fill = np.ceil(np.abs(attr)*255).astype(int)
#   if attr > 0:
#     g =c
#     # a = 255
#   if attr<0:
#     r = r+fill
#     # a = 255
#   return RGB(r,g,b,a)

def get_colors(seqs, attrs):
  """make colors for bases in sequence"""
  AAs = [i for s in list(seqs) for i in s]
  attrs = [i for s in attrs for i in s]
  colors = []
  j=0
  for AA in AAs:
    # if AA=='-':
    #   colors.append('white')
    #   continue
    colors.append(_get_color(attrs[j]))
    j=j+1
  return colors

def view_alignment(seqs, attrs, fontsize="9pt", plot_width=800, max_val=1.0, ids=None):
  """Bokeh sequence alignment view"""
  # attrs = (max_val-np.array(attrs))/max_val
  #make sequence and id lists from the aln object
  if ids==None:
    ids = ['sequence'+str(i) for i in range(1,len(seqs)+1)]    
  text = [i for s in list(seqs) for i in s]
  colors = get_colors(seqs, attrs)    
  N = len(seqs[0])
  S = len(seqs)    
  width = .4

  x = np.arange(1,N+1)
  y = np.arange(0,S,1)
  #creates a 2D grid of coords from the 1D arrays
  xx, yy = np.meshgrid(x, y)
  #flattens the arrays
  gx = xx.ravel()
  gy = yy.flatten()
  #use recty for rect coords with an offset
  recty = gy+.5
  h= 1/S
  #now we can create the ColumnDataSource with all the arrays
  source = ColumnDataSource(dict(x=gx, y=gy, recty=recty, text=text, colors=colors))
  plot_height = len(seqs)*15+50
  x_range = Range1d(0,N+1, bounds='auto')
  if N>600:
    viewlen=600
  else:
    viewlen=N
  #view_range is for the close up view
  view_range = (0,viewlen)
  tools="xpan, xwheel_zoom, reset, save"

  #entire sequence view (no text, with zoom)
  p = figure(title=None, width= plot_width, height=50,
             x_range=x_range, y_range=(0,S), tools=tools,
             min_border=0, toolbar_location='below')
  rects = Rect(x="x", y="recty",  width=1, height=1, fill_color="colors",
               line_color=None, fill_alpha=0.6)
  p.add_glyph(source, rects)
  p.yaxis.visible = False
  p.grid.visible = False  

  #sequence text view with ability to scroll along x axis
  p1 = figure(title=None, width=plot_width, height=plot_height,
              x_range=view_range, y_range=ids, tools="xpan,reset",
              min_border=0, toolbar_location='below')#, lod_factor=1)          
  glyph = Text(x="x", y="y", text="text", text_align='center',text_color="black",
              text_font="monospace",text_font_size=fontsize)
  rects = Rect(x="x", y="recty",  width=1, height=1, fill_color="colors",
              line_color=None, fill_alpha=0.4)
  p1.add_glyph(source, glyph)
  p1.add_glyph(source, rects)

  p1.grid.visible = False
  p1.xaxis.major_label_text_font_style = "bold"
  p1.yaxis.minor_tick_line_width = 0
  p1.yaxis.major_tick_line_width = 0

  p = gridplot([[p],[p1]], toolbar_location='below')
  return p