import colorsys

def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def get_color(x):
    x %= 50
    r, g, b = hsv2rgb(x / 50, 0.3, 0.9)
    return rgb2hex(r, g, b)