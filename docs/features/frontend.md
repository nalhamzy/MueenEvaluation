# Frontend — Angular Application

## Overview

The frontend is an Angular 20 application using standalone components and Angular Material for UI. It provides pages for article management, dataset overview, manual scoring, and configuration.

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Angular | 20 | Application framework |
| Angular Material | Latest | UI component library |
| TypeScript | 5.x | Type-safe development |
| SCSS | - | Component styling |
| Noto Naskh Arabic | Google Fonts | Arabic text rendering |

## Application Structure

```
frontend/src/app/
├── app.ts / app.html / app.scss     — Shell with toolbar + router outlet
├── app.config.ts                     — Providers (HTTP, router, animations)
├── app.routes.ts                     — Lazy-loaded routes
├── core/
│   ├── models/interfaces.ts          — TypeScript interfaces matching backend schemas
│   └── services/api.service.ts       — HTTP client for all backend endpoints
└── features/
    ├── articles/
    │   ├── article-list/             — Upload CSV/JSON, table of articles with status
    │   └── article-detail/           — Full article + DatasetItem side by side (tabs)
    ├── dataset/
    │   └── dataset-overview/         — Stats cards, generate button, items table
    ├── scoring/
    │   └── manual-score/             — Paste-and-score panel
    └── config/
        └── config-page               — Model settings, masked API keys
```

## Routing

| Path | Component | Description |
|------|-----------|-------------|
| `/` | Redirect → `/articles` | Default route |
| `/articles` | `ArticleList` | Upload + article table |
| `/articles/:id` | `ArticleDetail` | Article + dataset side-by-side |
| `/dataset` | `DatasetOverview` | Generation stats + items table |
| `/scoring` | `ManualScore` | Paste-and-score panel |
| `/config` | `ConfigPage` | LLM model configuration |

All components are **lazy-loaded** via `loadComponent()` for optimal bundle size.

## API Service

`core/services/api.service.ts` wraps all backend HTTP calls:

```typescript
// Articles
uploadArticles(file: File): Observable<UploadResponse>
getArticles(skip?, limit?): Observable<Article[]>
getArticle(id): Observable<Article>

// Dataset
generateDataset(limit?): Observable<any>
getDatasetItems(): Observable<DatasetItem[]>
getDatasetStats(): Observable<DatasetStats>

// Scoring
scoreManual(articleId, task, modelOutput): Observable<ScoreBreakdown>

// Config
getConfig(): Observable<AppConfig>
updateConfig(config): Observable<any>
```

Base URL: `http://localhost:8000/api` (hardcoded for development).

## Arabic Text Handling

- All Arabic text uses `dir="rtl"` attribute
- Font: `Noto Naskh Arabic` from Google Fonts (loaded in `index.html`)
- CSS class `.arabic-body` applies the font, `line-height: 2`, and `white-space: pre-wrap`
- NLI claims display with colored chips for label types

## Key Design Decisions

1. **Standalone components**: No `NgModule`s — Angular 20 defaults. Each component declares its own imports.

2. **Signals**: State managed via Angular signals (`signal<T>()`) for reactive UI updates.

3. **Lazy loading**: All feature pages are lazy-loaded via `loadComponent()` in routes.

4. **Material Design**: Angular Material components throughout — tables, cards, chips, form fields, toolbar, tabs, snackbars.

5. **No state management library**: Simple enough to use component-level signals + service calls. No need for NgRx.

## Running

```bash
cd frontend
npm install
npx ng serve --port 4200
```

Open `http://localhost:4200`. Backend must be running on port 8000.

## Building

```bash
npx ng build
# Output: frontend/dist/frontend/
```
