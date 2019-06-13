# Water-Vapour-Unit-Conversion
💧Converts units of a vertical profile of water vapour

## Metadata
| Metadata       |             |
|---------------:|-------------|
| Author         | Eden Au     |
| Version        | py1.0 stable|
| Last Updated   | 13 June 2019|
| Lib dependency | numpy       |

## Files
- [convert_h2o.py](convert_h2o.py) is the main code.
- [test_convert_h2o_py1.0.ipynb](test_convert_h2o_py1.0.ipynb) is the testing notebook for version py1.0-stable.

## Usage
```
from convert_h2o import convert_h2o
wout = convert_h2o(p,t,winp,unitinp,unitout)
```

1. p       - Pressure profile in hPa
2. t       - Temperature profile in K
3. winp    - Water vapour concentration in:
4. unitinp - Input units
5. unitout - Output units

where unitinp,unitout, character:
-                          'M' Mass Mixing Ratio (g/Kg)
-                          'V' Volume Mixing Ratio (ppv)
-                          'H' Relative Umidity (%)
-                          'S' Specific Humidity
-                          'D' Dew Point (K)
-                          'P' Partial Pressure (hPa)
-                          'N' Number Density (cm-3)
-                          'R' Mass Density (kg/m3)
-                          'C' Colummnar conntent (mm) (output only)

## Version py1.0
Currently, only 'M', 'H', 'N', and 'C' are supported.
