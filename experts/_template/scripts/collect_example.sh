#!/usr/bin/env bash
# Deterministic data collector for the gather-example skill.
#
# This is the determinism boundary of the expert: it prints a stable, structured
# set of key=value lines so callers (the skill, a playbook's confirm step, a
# test) get the same shape every run. Replace the placeholder values with real,
# reproducible data collection for your domain.
set -euo pipefail

echo "collector=collect_example"
echo "expert=_template"
echo "status=ok"
echo "items_found=0"
