from numpy import binary_repr
from Modulus.utils import color_gradient

e_path = None

color_range = []

data = {
    'calType': None,
    'parameters': [],
    'coff': [],
    'timeInterval': 1,
    'totalTime': 10,
    'resume': 0,
    'resumeFrom': 0
}

other_coff = {
    'Ag': 0,
    'Hg': 0
}

alloys = None
selected_temperature = None
selected_alloy = None
temp_selected_coff = None

# Position of mouse in the mesh
mouse_position = {
    'x': 0,
    'y': 0,
    'z': 0
}


# Mouse in the main window was clicked
is_position_selected = False

# Main window slider position
slider_position = None


grid_size_3d = {
    'x': 32,
    'y': 32,
    'z': 32
}


current_time = 0

# Default oof2 parameters
oof2_param = {
    'image_path': None,
    'image_name': None,
    'output_path': None,
    'coordinate': {
        'x': '0',
        'y': '0'
    },
    'elastic_constants': {
        'phase_1': {
            'C11': '208',
            'C12': '148',
            'C44': '96',
        },
        'phase_2': {
            'C11': '207',
            'C12': '149',
            'C44': '101',
        },
    },
    'boundary_conditions': {
        'bc1': {
            'boundary': 'left',
            'value': '-10'
        },
        'bc2': {
            'boundary': 'right',
            'value': '10'
        }
    },
    'mesh': {
        'x_elements': '10',
        'y_elements': '10',
        'element_type':'TriSkeleton'
    }
}

# For slecting plot colors
plot_colors = {
    'c_a_plot': {
        'options': {
            'colors': ['red', 'blue', 'green']
        },
        'selected': {
            'color': 'red',
            'thickness': 1
        }
    },
    'm_plot': {
        'options': {
            'continuous': ['binary', 'OrRd', 'BuPu', 'GnBu'],
            'discrete': ['blue-yellow', 'green-red'],
        },
        'selected': {
            'color_type': 'continuous',
            'color_value': 'OrRd',
            'plot_type': 'surface'
        }
    }
}
