# Demo Scenarios: Flame in Freefall

Benchmark scenarios for testing microgravity combustion predictions and data integrity.

## Scenario 1: Solid Fuel Flammability in BASS-II
- **Investigation**: BASS-II (PSI-25)
- **Parameters**: 
  - Fuel: Acrylic (PMMA) / Cotton
  - Oxygen Concentration: 21% - 30%
  - Airflow Velocity: 0 to 10 cm/s
- **Expected Outcome**: Flame propagation speed increases exponentially with oxygen concentration (>25%) even in zero forced flow.
- **Verification Rule**: Compare local predictions with BASS-II raw dataset (`data/raw-BASS-II/`).

## Scenario 2: Extinction & Droplet Limits in FLEX
- **Investigation**: FLEX (PSI-69) / FLEX-2 (PSI-68)
- **Parameters**:
  - Fuel: Heptane / Methanol droplets
  - Ambient Pressure: 1 atm
- **Expected Outcome**: Radiative extinction observed at critical droplet diameter prior to complete fuel burnout.
- **Verification Rule**: Cross-reference output with FLEX sample metadata (`data/raw-FLEX/`).

## Scenario 3: Incipient Spacecraft Fire in Saffire
- **Investigation**: Saffire-I (PSI-98)
- **Parameters**:
  - Fuel: Cotton-fiberglass blend (large scale)
  - Microgravity duration: Extended (Cygnus re-entry phase)
- **Expected Outcome**: Low-flow flame propagation exhibits slow pyrolysis front with distinct smoke signature.
- **Verification Rule**: Metadata traced back to NASA NTRS records (`data/papers.json`).