import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'articles', pathMatch: 'full' },
  {
    path: 'articles',
    loadComponent: () => import('./features/articles/article-list/article-list').then(m => m.ArticleList),
  },
  {
    path: 'articles/:id',
    loadComponent: () => import('./features/articles/article-detail/article-detail').then(m => m.ArticleDetail),
  },
  {
    path: 'dataset',
    loadComponent: () => import('./features/dataset/dataset-overview/dataset-overview').then(m => m.DatasetOverview),
  },
  {
    path: 'scoring',
    loadComponent: () => import('./features/scoring/manual-score/manual-score').then(m => m.ManualScore),
  },
  {
    path: 'config',
    loadComponent: () => import('./features/config/config-page').then(m => m.ConfigPage),
  },
  {
    path: 'runs',
    loadComponent: () => import('./features/runs/run-list/run-list').then(m => m.RunList),
  },
  {
    path: 'runs/manual',
    loadComponent: () => import('./features/runs/manual-run/manual-run').then(m => m.ManualRun),
  },
  {
    path: 'runs/:id',
    loadComponent: () => import('./features/runs/run-detail/run-detail').then(m => m.RunDetail),
  },
  {
    path: 'comparison',
    loadComponent: () => import('./features/evaluation/model-comparison/model-comparison').then(m => m.ModelComparison),
  },
  {
    path: 'outputs/:runId/:articleId',
    loadComponent: () => import('./features/evaluation/output-detail/output-detail').then(m => m.OutputDetail),
  },
  {
    path: 'reports/:id',
    loadComponent: () => import('./features/reports/executive-summary/executive-summary').then(m => m.ExecutiveSummary),
  },
];
