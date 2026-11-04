# Pitfalls (each one happened at least once)

Stack-agnostic ones. Framework-specific pitfalls are at the end of each
`stacks/*.md` file.

| Symptom | Cause | Fix |
| --- | --- | --- |
| User says "yine çok benzer" after a redesign | Kept the reference's visual language (shapes, mono type, grid, palette), only recoloured it | Start from the product's truths and a new direction; take only motion *quality* from the reference |
| Range slider "won't update" / drag selects page text | Input styled `height: 4px`; only the 4px line receives pointer events, the 22px thumb overflow does not | Input height = thumb height, transparent background; draw the line on `::-webkit-slider-runnable-track` / `::-moz-range-track` (+ `::-moz-range-progress`); thumb `margin-top: -(thumb - track)/2` |
| "Sayılar tutmuyor" on a recommender | Explanation showed the plan's limits (10/20) instead of why the user's numbers (3/9) needed it | Explain with the crossed limit of the plan below: "Profesyonel en fazla 6 hesap içeriyor; Kurumsal 10 mağaza ve 20 hesaba kadar yetiyor" |
| Pinned section content overflows to the right | Flex track inside a grid column; grid item `min-width: auto` grows to the track's width | `min-width: 0` on that column |
| Sticky section doesn't stick | An ancestor has `overflow: hidden` | Move overflow clipping inside the sticky element |
| Header CTA overflows on mobile | A component class with `display:inline-flex` in an unlayered `<style>` beats Tailwind's `hidden` utility | Wrap it: `<span class="hidden sm:inline"><span class="tag">…</span></span>` |
| Blank page when JS fails | Elements hidden by default for reveal | Hide only under a class JS adds (`.armed`) |
| Reduced-motion users get a CPU spike | Loop `await wait(0)` when reduced | Loop waits use a real timeout regardless |
| Screenshots look faded/blurred | Taken mid-reveal/page-enter | Wait for transitions or force `.in` before judging |
| "Fixed" code not visible in browser | Navigating to the same URL with only a hash change does not reload | `location.reload()` or add a query string |
| Test passes, real drag fails | Test set `input.value` via JS | Verify interactions with real pointer events too |
| Wrong greeting ("İyi geceler" at 9:00) | Server/app timezone (UTC) used for display | Convert to the user's timezone for display |
| "Sync running" shown with nothing connected | Status pill unconditional | Show live/status claims only when the data supports them |
| Dates/English strings in a localized UI | Framework locale not set, starter-kit strings untranslated | panel-patterns §5 + the stack file |
| Inline `transform` on `<em>` does nothing | Transforms don't apply to inline elements | `inline-block` |
| Function from another block undefined | Helper declared inside an `if` block of a different feature | Keep helpers top-level in the script or inline them |
| Counters/odometers jump from 0 on every change | count-up always starts at 0 | Start from the previous value |
| Report says "only transform/opacity" but the story section stutters | Step bodies expanded with `grid-template-rows: 0fr → 1fr` / `max-height`; progress bar or slider thumb animates `width` | Fade bodies with opacity/transform at full height; bars use `scaleX`; grep before claiming |
| Without JS only step 1 of "how it works" is readable | Inactive steps hidden by server CSS (`opacity: 0`, `hidden` on mobile), not under `.armed` | Put every JS-driven hidden state under `.armed`; no-JS shows the steps stacked |
| Animations dead after an in-app navigation | Init ran once on page load; SPA navigation swapped the DOM | Re-init on the router's navigation event, idempotently |
| Ghost / outline button invisible on a coloured hero (1.0–1.2:1) | Button text uses the hero's own brand colour (`color: var(--accent)` on an accent background) | Ghost buttons on coloured surfaces use the surface's *ink* colour; scope per-direction `.btn` colour overrides with `:not(.ghost)`; run `verify.js` on every direction, not only the light one |
| Phone / screen mock-up empty in screenshots and with reduced motion | Signature animation starts from an empty scene and fills it over time | Start the loop from the finished scene (or give frame 0 content); check a still screenshot, see `visual-critique.md` |
| `verify.js` reports low contrast on muted text | `--muted` picked by eye on one background | Check muted text on *both* background and raised surface, light and dark |
