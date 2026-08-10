# Model panel

The frozen panel uses four lower-cost full-matrix backbones and two frontier diagnostic models through OpenRouter. Exact model slugs and providers are in `configs/model_panel_v1.yaml`.

OpenRouter routing is configured with provider order, fallbacks disabled, required-parameter enforcement, and provider data collection denied. Provider compatibility must pass preflight. Silent provider substitution is prohibited.

The frontier diagnostic subset is pre-specified at six tasks, one per domain to control cost. It is reported separately from the full-matrix backbone analysis.
