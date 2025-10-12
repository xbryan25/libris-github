# 🎨 Libris Color System

This document defines the **Libris UI Color System**, which unifies design and code through reusable theme tokens.  
It ensures consistent color behavior in both **light** and **dark** modes — powered by **Nuxt Color Mode** and **Tailwind**.

---

## 🌗 Overview

The color system is built on **CSS custom properties** (variables) that adapt automatically when the color mode changes.

| Token                   | Description               | Light       | Dark        |
| ----------------------- | ------------------------- | ----------- | ----------- |
| `--color-background`    | Page background           | `zinc-100`  | `zinc-900`  |
| `--color-surface`       | Cards, navbar, containers | `white`     | `zinc-950`  |
| `--color-surface-hover` | Hover backgrounds         | `zinc-200`  | `zinc-800`  |
| `--color-base`          | Borders & dividers        | `zinc-300`  | `zinc-700`  |
| `--color-text`          | Default text              | `zinc-800`  | `zinc-100`  |
| `--color-accent`        | Brand color (interactive) | `green-700` | `green-500` |

---
## 📋 Design Guidelines

### When to Use Each Token

- **`--color-background`**: Main app background, page canvas
- **`--color-surface`**: Elevated elements (cards, modals, navigation)
- **`--color-surface-hover`**: Interactive surface states (buttons, list items)
- **`--color-base`**: Visual separators, input borders, dividing lines
- **`--color-text`**: Primary content, headings, body text
- **`--color-text-muted`**: Supporting text, captions, labels
- **`--color-accent`**: CTAs, links, brand elements, focus states
- **`--color-accent-active`**: Pressed buttons, active selections

## Visual Reference

The visualization below demonstrates all tokens applied in a realistic UI context:

![Sample](https://color-palette-ui.tiiny.site/color-palette-ui.svg)

