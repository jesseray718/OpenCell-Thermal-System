# Passive Solar Loop: Volumetric Blackbody Solar Absorber

**Principal Investigator:** Jesse McMillen  
**Date Created:** 2026-06-07  
**Status:** Active Development

## Summary
A passive solar–subsurface thermal loop using volumetric blackbody absorbers
and porous subterranean thermal mass to create self-powered convective air
movement and harvest large latent heat from shallow ground water/ice.

## Repository Structure
- `0_data/raw/` — Unprocessed sensor logs and CSVs
- `0_data/processed/` — Cleaned data, analysis results
- `1_code/src/` — Python scripts, Flask bridge, tools
- `1_code/arduino/` — ESP32/Arduino sensor sketches
- `2_pipeline/automation/` — Cron jobs, diagnostics, system scripts
- `docs/manuscript/` — Grant applications, peer-review drafts
- `docs/specifications/` — Technical specs, calculations
- `docs/sessions/` — Conversation notes, planning logs
- `inputs/` — Reference papers, external documents
- `env/` — Dependency lists, environment configs

## Quick Start
1. Install Termux dependencies: `pkg install python git`
2. Run data collector: `python 1_code/src/data_collector.py`
3. View sensor status: `bash 2_pipeline/automation/device_info.sh`

## Key Innovation: Open-Cell Aerocement
Formulation: xantham gum (15g) in rubbing alcohol slurry + 1/4 cup Dawn Ultra
in water → gel with near-zero slump. Mixed 1:2 ratio with cement. Stirring
incorporates microscopic air sphere bubbles. At critical volume, closed-cell
transitions to open-cell. Adding activated carbon creates blackbody structure.

## Contact
Project owner: Jesse McMillen
