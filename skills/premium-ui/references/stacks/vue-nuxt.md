# Stack: Vue / Nuxt (and Inertia + Vue)

Read this only when the project is Vue. Generic rules live in `SKILL.md`,
`panel-patterns.md` and `pitfalls.md`.

Detect: `package.json` with `vue` / `nuxt`; Inertia if `@inertiajs/vue3`
(often inside a Laravel app — then also read `laravel-livewire.md` §3 for
language files). Component library: Nuxt UI, PrimeVue, Vuetify, shadcn-vue.

## 1. Theming the component library centrally

Find where the library takes its tokens and change them there:

- **Nuxt UI**: semantic colours in `app.config.ts` (`ui.colors.primary`,
  `neutral`) and CSS variables / `@theme` in the main stylesheet.
- **PrimeVue**: a preset (`definePreset(Aura, {...})`) passed to the plugin
  config — override `semantic.primary`, surfaces and `borderRadius` there.
- **shadcn-vue**: same CSS variables as shadcn/ui (`--primary`, `--radius`…),
  see `react-next.md` §1.
- **Vuetify**: `createVuetify({ theme: { themes: { light, dark } } })` and
  global `defaults` for rounded/variant.

Check the installed major version first; these APIs change between majors.

## 2. Motion in Vue

- `<Transition>` / `<TransitionGroup>` for enter/leave and list staggers
  (stagger via a `--i` style binding + `transition-delay`).
- Page enter: Nuxt `pageTransition` in `nuxt.config` / `definePageMeta`;
  Inertia: wrap the page slot in `<Transition appear>` in the layout.
- Reveal/observer logic in a composable (`useReveal(el)`) that sets up in
  `onMounted` and disconnects in `onBeforeUnmount`. Add `armed` on mount, so
  SSR output stays visible.
- If `@vueuse/core` is present, use `useIntersectionObserver`,
  `usePreferredReducedMotion`, `useElementBounding`. Don't add it just for this.
- Hydration: same rule as React — stable first render for count-ups,
  greetings and dates; adjust after mount (`<ClientOnly>` if needed).

## 3. Pitfalls seen in Vue projects

| Symptom | Cause | Fix |
| --- | --- | --- |
| Hydration mismatch warnings on the dashboard | Time/locale text rendered on the server | Stable first render, update in `onMounted` |
| Observers keep firing after navigation | No cleanup in `onBeforeUnmount` | Disconnect in the composable |
| `<Transition>` doesn't animate | Child has no single root element / no `key` change | One root, `:key` on the swapped element |
