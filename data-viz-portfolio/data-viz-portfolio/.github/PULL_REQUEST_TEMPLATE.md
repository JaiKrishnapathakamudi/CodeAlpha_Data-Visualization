## Summary
Brief description of what this PR does.

## Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New chart / feature
- [ ] 🎨 Visual / style improvement
- [ ] 📝 Documentation update
- [ ] ♻️  Refactor (no functional change)
- [ ] 🧪 Test improvement

## Charts Affected
List any chart files added or modified:
- `src/visualizations/chart_XX_name.py`

## Checklist
- [ ] `python src/build_all.py` runs without errors
- [ ] `pytest tests/ -v` passes (8/8 or better)
- [ ] Chart calls `apply_theme()` and `add_watermark(fig)`
- [ ] Uses only palette tokens from `style.py` (no hard-coded colours)
- [ ] `render(save=False)` returns a `plt.Figure` object
- [ ] `README.md` updated with new chart entry (if applicable)
- [ ] `CHANGELOG.md` updated under `[Unreleased]`

## Screenshots
Attach before/after PNG screenshots for any visual changes.
