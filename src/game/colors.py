from hsluv import hsluv_to_rgb

_RGB = tuple[float, float, float]

# bg colors
C_WARN: _RGB = hsluv_to_rgb([0, 0, 25])
C_DEFAULT: _RGB = hsluv_to_rgb([0, 0, 30])

# text colors
C_T_WARN: _RGB = hsluv_to_rgb([12.7, 100, 55.5])
