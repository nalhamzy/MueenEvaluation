import { Component, OnInit, signal, computed } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import { ApiService } from '../../../core/services/api.service';

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const MODEL_COLORS = [
  '#1976d2', '#e53935', '#43a047', '#fb8c00', '#8e24aa',
  '#00897b', '#d81b60', '#5e35b1', '#3949ab', '#00acc1',
];

@Component({
  selector: 'app-model-comparison',
  imports: [
    MatTableModule, MatButtonModule, MatIconModule,
    MatCardModule, MatSnackBarModule, MatProgressBarModule,
    BaseChartDirective,
  ],
  templateUrl: './model-comparison.html',
  styleUrl: './model-comparison.scss',
})
export class ModelComparison implements OnInit {
  comparison = signal<any[]>([]);
  loading = signal(false);

  groupedBarConfig = computed((): ChartConfiguration<'bar'> | null => {
    const data = this.comparison();
    if (data.length === 0) return null;
    const tasks = ['NER', 'NLI', 'Summary', 'Translation'];
    const taskKeys = ['ner_score', 'nli_score', 'summary_score', 'translation_score'];
    const datasets = data.map((row, i) => ({
      label: row.model_name,
      data: taskKeys.map(k => row[k] ?? 0),
      backgroundColor: MODEL_COLORS[i % MODEL_COLORS.length],
      borderRadius: 4,
    }));
    return {
      type: 'bar',
      data: { labels: tasks, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${(ctx.parsed.y as number).toFixed(2)}` } },
        },
        scales: {
          x: { title: { display: true, text: 'Task' } },
          y: { beginAtZero: true, max: 10, title: { display: true, text: 'Score' } },
        },
      },
    };
  });

  displayedColumns = ['model_name', 'ner_score', 'nli_score', 'summary_score', 'translation_score', 'overall_score'];

  constructor(
    private api: ApiService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.loadComparison();
  }

  loadComparison() {
    this.loading.set(true);
    this.api.getComparison().subscribe({
      next: (data) => {
        this.comparison.set(Array.isArray(data) ? data : data.runs || []);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.snackBar.open('Failed to load comparison data', 'Close', { duration: 3000 });
      },
    });
  }

  formatScore(value: number | null | undefined): string {
    return value != null ? value.toFixed(2) : '—';
  }

  barWidth(value: number | null | undefined): number {
    if (value == null) return 0;
    return Math.min(Math.max(value * 100, 0), 100);
  }
}
