# ProcessDoctor — Accessibility Checklist

**Owner:** Adetutu (Tutu) Adenusi, UX Coordinator
**Standard:** WCAG 2.1 Level AA
**Why this matters:** IBM is an accessibility leader through Carbon and the IBM Accessibility Lab. Judges from IBM will test for keyboard navigation, screen reader support, and color contrast. Failing this hurts our judging score on UX/Design (Criterion 3). It also signals to judges that we don't understand the IBM ecosystem.

This is a pre-submission checklist. Run through every item before we present.

---

## 1. Keyboard Navigation

- [ ] Every interactive element is reachable via Tab.
- [ ] Tab order follows visual reading order (left to right, top to bottom).
- [ ] Focus is never trapped (modals can be closed with Escape).
- [ ] Focus returns to the triggering element when modals close.
- [ ] Skip-to-main-content link is present and functional (already in App.tsx).
- [ ] No keyboard-inaccessible custom controls. If a button is a `<div>`, it has `role="button"`, `tabindex="0"`, AND key handlers for Enter and Space.

**How to test:** unplug your mouse. Tab through the entire app. Every action you can do with a click must be doable with the keyboard.

---

## 2. Focus Visibility

- [ ] All focusable elements have a visible focus ring.
- [ ] Focus ring meets 3:1 contrast against adjacent colors (WCAG 2.4.7).
- [ ] Focus ring uses our token: `--pd-focus-ring-color` (#0F62FE).
- [ ] Carbon components inherit focus styling automatically — do not override.
- [ ] Custom buttons use `:focus-visible` not `:focus` (preserves mouse-click experience).

**How to test:** Tab through the app. You should see a clear blue outline on every focused element.

---

## 3. Color and Contrast

- [ ] Body text contrast ratio is at least 4.5:1.
- [ ] Large text (18pt+) contrast ratio is at least 3:1.
- [ ] UI component borders / focus rings meet 3:1 against background.
- [ ] No information is conveyed by color alone.
  - Bottlenecks: red border + warning icon + "Bottleneck" label
  - Success states: green + checkmark icon + "Optimized" label
  - Error states: red + error icon + descriptive text

**How to test:** use webaim.org/resources/contrastchecker. Open in grayscale mode (devtools rendering tab) and confirm everything still makes sense.

---

## 4. Semantic HTML

- [ ] One `<h1>` per page (the brand title in DashboardHeader).
- [ ] Heading hierarchy is logical: `<h1>` → `<h2>` → `<h3>` (no skipping).
- [ ] `<main>`, `<header>`, `<section>`, `<article>`, `<nav>` used appropriately.
- [ ] Lists are real `<ul>` or `<ol>`, not styled `<div>`s.
- [ ] Buttons are `<button>`, not `<div onClick>`.
- [ ] Links are `<a href>`, not buttons used for navigation.

**How to test:** open devtools accessibility tree. The structure should make sense without any styling.

---

## 5. ARIA Labels and Roles

- [ ] Every form input has a `<label>` (Carbon's `labelText` prop handles this).
- [ ] Buttons that contain only icons have `aria-label`.
- [ ] Decorative images and icons have `aria-hidden="true"`.
- [ ] Meaningful images have descriptive `alt` text.
- [ ] Workflow graph has `role="img"` and `aria-label` describing its content.
- [ ] Stage indicator uses `aria-current="step"` on the active phase.
- [ ] Reasoning panel uses `aria-live="polite"` so new steps are announced without interrupting.
- [ ] Status tags include screen-reader text: e.g., `<span class="pd-sr-only">Severity: </span>critical`.

**How to test:** turn on VoiceOver (Mac: Cmd+F5) or NVDA (Windows: free download). Navigate the app. Every piece of information should be announced clearly.

---

## 6. Forms

- [ ] Every input has a visible, persistent label.
- [ ] Helper text and error messages are associated with their input via `aria-describedby` (Carbon does this automatically).
- [ ] Required fields are marked both visually and with `required` / `aria-required="true"`.
- [ ] Validation errors are announced to screen readers via Carbon's built-in error states.
- [ ] Placeholder text never replaces a label (placeholders disappear on focus).

---

## 7. Motion and Animation

- [ ] Honor `prefers-reduced-motion`. Our global stylesheet handles this — animations reduce to 0.01ms when the user has the OS setting enabled.
- [ ] No flashing or strobing content (3+ flashes per second is a seizure risk).
- [ ] Auto-advancing content (carousels, etc.) — we don't have any. Don't add.

**How to test:** OS settings → Accessibility → Reduce Motion. Re-test the app. Transitions should be effectively instant.

---

## 8. Zoom and Reflow

- [ ] App is usable at 200% zoom without horizontal scrolling.
- [ ] No fixed-width containers that break at small sizes.
- [ ] Text is real text, not an image of text.
- [ ] Layout reflows gracefully on mobile viewport (test at 375px width).

**How to test:** Cmd/Ctrl + Plus to zoom to 200%. Resize browser to phone width. Everything should still be readable and functional.

---

## 9. Specific to ProcessDoctor

- [ ] **Workflow graph:** every node is reachable by keyboard if interactive. Bottleneck status is communicated by icon + label, not just red.
- [ ] **Reasoning panel:** `aria-live="polite"` so screen reader users hear new reasoning steps as Bob "thinks."
- [ ] **Phase tabs:** Carbon Tabs handle keyboard navigation (arrow keys to move between tabs). Don't override.
- [ ] **Modal (approval gate):** focus traps inside the modal while open, returns to the trigger button on close. Escape key closes. Carbon's Modal handles all of this.
- [ ] **Code snippet (generated YAML):** Carbon's CodeSnippet is keyboard-accessible. Copy button is keyboard-reachable.
- [ ] **Success state:** the green checkmark icon has appropriate text alongside it. Not relying on color alone.

---

## 10. Pre-Demo Smoke Test

Run this exact sequence before the demo:

1. Load the app with screen reader on. Navigate from the skip link through every section.
2. Tab through every interactive element on every phase. Verify focus order makes sense.
3. Test every action with keyboard only.
4. Zoom to 200%. Confirm everything still renders.
5. Toggle prefers-reduced-motion on. Confirm animations are effectively gone.
6. Run an automated audit:
   - Chrome DevTools → Lighthouse → Accessibility audit. Aim for 95+ score.
   - Or install axe DevTools (free Chrome extension) and run on every phase.

If any of these fail, fix before submission.

---

## Why this is a competitive advantage, not just compliance

Most hackathon teams skip accessibility. We won't. Three reasons:

1. **IBM is an accessibility leader.** Carbon ships with WCAG AA built in because IBM's customers (banks, governments, healthcare) require it. Judges from IBM will notice if we honor that.
2. **It's effectively free with Carbon.** Most of this checklist is already handled by using Carbon components correctly. We just have to not break it.
3. **It signals enterprise-readiness.** A product that's accessible looks like a product ready for real customers, not a hackathon prototype.

If we hit every box on this list, we get judging points other teams won't.
