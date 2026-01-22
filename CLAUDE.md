# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
npm run dev      # Start development server with HMR
npm run build    # TypeScript type check + Vite production build
npm run lint     # Run ESLint
npm run preview  # Preview production build locally
```

## Project Overview

This is a React + TypeScript + Vite application designed for Figma-to-code conversion workflows. The main sample application is a Japanese medication record management interface (お薬手帳).

## Architecture

**Stack:** React 19, TypeScript, Vite, Tailwind CSS 4

**Entry Flow:**
- `src/main.tsx` → React DOM mount
- `src/App.tsx` → Root component
- `src/MedicationRecordApp.tsx` → Main feature component with medication cards

**Styling:** Tailwind CSS utility classes. Mobile-first design (564px target width). Global styles in `src/index.css`.

## Figma-to-Code Skill

Located in `.claude/skills/`:
- `figma-to-html.md` - Instructions for converting Figma designs to React + Tailwind CSS or HTML + CSS
- `scripts/figma_to_html.py` - Python utility for parsing Figma JSON and generating HTML/CSS

The skill supports multi-page Figma designs and uses Figma API image URLs for assets.

## TypeScript Configuration

Strict mode enabled with `noUnusedLocals` and `noUnusedParameters`. JSX uses react-jsx transform (no React import needed in components).
