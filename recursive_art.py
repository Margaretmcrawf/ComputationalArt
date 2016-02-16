""" Function creates art based on randomly generated functions. Takes about 20 seconds to run. """

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
        (see assignment writeup for details on the representation of
        these functions)
    """

    #randomly selects the first block to go into the function, from a string of building block functions
    blocks = ['prod', 'avg', 'cos_pi', 'sin_pi', 'x', 'y', 'cube', 'atan']
    function = [random.choice(blocks)]
    
    #basic situation for when there are lots of recursions left and we don't have to worry about end cases
    if min_depth > 1:
        min_depth = min_depth - 1
        max_depth = max_depth - 1
        if function in [['x'], ['y'], ['avg'], ['prod']]: #function requires two inputs
            function = function + [build_random_function(min_depth, max_depth)] + [build_random_function(min_depth, max_depth)]
        else: #only one input
            function = function + [build_random_function(min_depth, max_depth)]
        return function

    #once max_depth gets to 1, the next element must be either x or y.
    if max_depth == 1:
        list1 = ['x', 'y']
        function = [random.choice(list1)]
        return function

    #once the function gets past the threshold of min_depth, it can end if the random function is either x or y
    if min_depth == 1:
        
        if function == ['x'] or function == ['y']:
            return function
        else:
            max_depth = max_depth - 1

            if function == ['avg'] or function == ['prod']:
                function = function + [build_random_function(min_depth, max_depth)] + [build_random_function(min_depth, max_depth)]
            else:
                function = function + [build_random_function(min_depth, max_depth)]
            return function

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate, will be a list of strings
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(['x'],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(['y'],0.1,0.02)
        0.02
        >>> evaluate_random_function(['sin_pi', ['y']], 0.9, 0.5)
        1.0
    """

    #define all lambda functions for the building blocks
    prod = lambda a, b: a*b
    avg = lambda a, b: 0.5*(a+b)
    cos_pi = lambda a: math.cos(math.pi*a)
    sin_pi = lambda a: math.sin(math.pi*a)
    fx = lambda a, b: a
    fy = lambda a, b: b
    atan = lambda a: math.atan(a)*4/math.pi
    cube = lambda a: a**3

    #in the last recursion, a = x and b = y
    blocks = [['prod'], ['avg'], ['cos_pi'], ['sin_pi'], ['x'], ['y'], ['cube'], ['atan']]
    if f in blocks:
        a = x
        b = y
    else:
    #recursively defines the inputs for the outermost function
        a = evaluate_random_function(f[1], x, y)
        if f[0] in ['x', 'y', 'avg', 'prod']:
            b = evaluate_random_function(f[2], x, y)

    if f[0] == 'prod':
        return prod(a, b)
    if f[0] == 'avg':
        return avg(a, b)
    if f[0] == 'cos_pi':
        return cos_pi(a)
    if f[0] == 'sin_pi':
        return sin_pi(a)
    if f[0] == 'x':
        return fx(a, b)
    if f[0] == 'y':
        return fy(a, b)
    if f[0] == 'cube':
        return cube(a)
    if f[0] == 'atan':
        return cube(a)

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    fraction = float(val - input_interval_start) / (input_interval_end - input_interval_start) #the value between 0 and 1 that val translates to
    return fraction*(output_interval_end - output_interval_start) + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """

    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("example7.png")

    # Test that PIL is installed correctly
    #test_image("noise.png")