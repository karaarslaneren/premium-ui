# Pitfalls (each one happened at least once)

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
| Wrong greeting ("İyi geceler" at 9:00) | App timezone UTC | Convert to the user's timezone for display |
| "Sync running" shown with nothing connected | Status pill unconditional | Show live/status claims only when the data supports them |
| Dates/English strings in a Turkish UI | `APP_LOCALE=en`, starter-kit strings untranslated, `#[Title]` not translated | See panel-patterns §5 |
| Inline `transform` on `<em>` does nothing | Transforms don't apply to inline elements | `inline-block` |
| Function from another block undefined | Helper declared inside an `if` block of a different feature | Keep helpers top-level in the script or inline them |
| Counters/odometers jump from 0 on every change | count-up always starts at 0 | Start from the previous value |
| Livewire method name fatal (white screen) | Component method clashes with `Livewire\Component` methods (`pull`, `reset`, `only`…) | Use specific names (`pullCatalogue`) |
