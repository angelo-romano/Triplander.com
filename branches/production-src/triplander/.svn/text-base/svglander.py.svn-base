import cairo
import rsvg
from os.path import exists
 
class svglander:
    def __init__(self):
        self.path = None
        self.svg = None
        self.cr = None
    
    def open(self,path):
        if not exists(path): return False
        self.path = path
        self.svg = rsvg.Handle (file = path)
        

    def drawRectangle(self,x0,y0,x1,y1):
        surface = cairo.ImageSurface (cairo.FORMAT_ARGB32,256,256)
        cr = cairo.Context (surface)
        if (cr is None): return None
        cr.rectangle(x0,y0,x1,y1)
        
    def convert(self,width=None,height=None):
        output = None
        if (self.path is None): return None
        if (self.svg is None): return None
        
        path = self.path
        
        '''Output filename generation'''
        if path[-4:] == ".svg":
            path = path[:-4]
        output = "%s.png" % path
        base = "%s%d.png"
        #i = 1
        #while exists (output):
        #    output = base % (path, i)
        #    i += 1
     
        if width is None and height is None:
            width = self.svg.props.width
            height = self.svg.props.height
        elif width is not None:
            ratio = float (width) / self.svg.props.width
            height = int (ratio * self.svg.props.height)
        elif height is not None:
            ratio = float (height) / self.svg.props.height
            width = int (ratio * self.svg.props.width)
     
        surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context (surface)
        
        wscale = float (width) / self.svg.props.width
        hscale = float (height) / self.svg.props.height
     
        cr.scale (wscale, hscale)
     
        self.svg.render_cairo (cr)
     
        surface.write_to_png (output)
        
        return output