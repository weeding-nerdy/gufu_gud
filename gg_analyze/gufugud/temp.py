import numpy as np
import scipy.interpolate as interp

# Materials reference tables
MATERIAL_REF = {
    'tcr': {
        #         'ss316l': 879*10**-6  # delta_r/r per degree Celsius  # From Steam Engine calculator
        'ss316l': 920*10**-6,  # delta_r/r per degree Celsius
    },
    'tfr': {
        # list(tuple()) with form [(t1, rr1), (t2, rr2), ...] with:
        #      t = temperature in Celsius
        #     rr = resistance ratio of measured_resistance / reference_resistance
        'ss316l': [  # From Arctic Fox/Steam Engine
            (-40, 0.93474),
            (20, 1.00000),
            (50, 1.03000),
            (100, 1.08000),
            (150, 1.12600),
            (200, 1.16800),
            (250, 1.20700),
            (300, 1.24600),
            (425, 1.33700),
        ],
    },
}

ESCC_COLD_RES_TCR_REF = {
    'escc_v1': [
        # list(tuple()) with form [(tcr1, r1), (tcr2, r2), ...] with:
        #     tcr = Temperature Coefficent of Resistance * 10^5 (unitless)
        #       r = Cold resistance in Ohms
        # Data from: https://www.reddit.com/r/AdvancedVapeSupply/comments/iszh2f/escc_tcr_chart_and_update_about_the_escc/
        (200, 0.40),
        (185, 0.45),
        (170, 0.50),
        (155, 0.55),
        (145, 0.60),
        (138, 0.65),
        (130, 0.70),
        (120, 0.75),
        (110, 0.80),
        (100, 0.85),
        (85, 0.90),
        (70, 0.95),
        (50, 1.00),
        (25, 1.05),
        (5, 1.10),
    ],
}


def resratio_to_temp(t_cold=None, material='ss316l', method='tfr'):
    """ Converts resistance ratio into temperature for a material with a known TCR or TFR.

    Args:
        t_cold (float): The cold coil reference temperature, in Celsius. Only used for TCR and is 20 C if None. Optional.
        material (float, list, or str): Material TCR float in delta_r/r per degree Celsius,
                                        material TFG list of tuples of temp in Celsius and resistance ratio,
                                        or str of material for TCR and TFR to look up.
        method (str): Method to use for conversion, must be one of ['tcr', 'tfr']. Optional.

    Returns:
        Function object:
            Args:
                rr (array-like): Resistance ratio(s) to convert to a temperature
            Returns:
                np.ndarray to temperatures in Celsius
    """
    if method not in ['tcr', 'tfr']:
        raise NotImplementedError(f'Unimplemented method: {method}')

    if (t_cold is not None) and (method != 'tcr'):
        raise ValueError(f't_cold is only useable for tcr method')

    if isinstance(material, str):
        # Look up material properties from string
        material = MATERIAL_REF[method][material]

    if method == 'tcr':
        # Temperature Coefficient of Resistance method
        t_cold = 20.0 if t_cold is None else t_cold  # Default t_cold is 20 C
        def temp_func(rr, t_cold=t_cold, material=material): return np.asarray(
            t_cold + ((np.asarray(rr) - 1.0) / material))
    elif method == 'tfr':
        # Temperature Function of Resistance method, cubic spline interpolation
        temp, rr = tuple(zip(*material))
        temp_func = interp.CubicSpline(rr, temp, bc_type='natural')
    else:
        raise RuntimeError('The matrix is glitching again')

    return temp_func


def coldres_to_tcr(material='escc_v1'):
    """ Converts cold resistance into temperature for a material with a known TCR or TFR.

    Args:
        material (float, list, or str): Material TCR list of tuples of TCR (unitless) and cold resistance in Ohms,
                                        or str of material name to look up.

    Returns:
        Function object:
            Args:
                r_cold (array-like): Reference cold resistance to convert to a TCR
            Returns:
                np.ndarray to TCR (unitless)
    """
    if isinstance(material, str):
        # Look up material properties from string
        material = ESCC_COLD_RES_TCR_REF[material]

    # Temperature Function of Resistance method, cubic spline interpolation
    temp, rr = tuple(zip(*material))
    temp_func = interp.CubicSpline(rr, temp, bc_type='natural')

    return temp_func


def calculate_temp(df, resistance, material, method):
    t_func = resratio_to_temp(material=material, method=method)
    df['temp'] = t_func(df.r / resistance)
    df['temp'] = df.temp.fillna(0).clip(0.0, 300.0)

    return df
