import { Component, OnInit, OnDestroy, signal, computed } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { JsonPipe } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, Chart, RadarController, RadialLinearScale, PointElement, LineElement, Filler, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import { ApiService } from '../../../core/services/api.service';
import { EvaluationRun, ModelOutput } from '../../../core/models/interfaces';

Chart.register(RadarController, RadialLinearScale, PointElement, LineElement, Filler, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

@Component({
  selector: 'app-run-detail',
  imports: [
    DatePipe,
    RouterLink,
    MatTableModule, MatButtonModule, MatIconModule,
    MatChipsModule, MatCardModule, MatSnackBarModule,
    MatProgressBarModule, MatTooltipModule,
    JsonPipe, BaseChartDirective,
  ],
  templateUrl: './run-detail.html',
  styleUrl: './run-detail.scss',
})
export class RunDetail implements OnInit, OnDestroy {
  run = signal<EvaluationRun | null>(null);
  outputs = signal<ModelOutput[]>([]);
  scores = signal<any>(null);
  loading = signal(false);
  judging = signal(false);
  generatingReport = signal(false);

  progressPercent = computed(() => {
    const r = this.run();
    if (!r || !r.total_articles) return 0;
    return Math.round((r.processed_count / r.total_articles) * 100);
  });

  avgScores = computed(() => {
    const items = this.outputs();
    if (items.length === 0) return null;
    const scored = items.filter(o => o.overall_score !== null);
    if (scored.length === 0) return null;
    const avg = (field: keyof ModelOutput) => {
      const vals = scored.map(o => o[field] as number | null).filter((v): v is number => v !== null);
      return vals.length ? +(vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(2) : null;
    };
    return {
      ner: avg('ner_score'),
      nli: avg('nli_score'),
      summary: avg('summary_score'),
      translation: avg('translation_score'),
      overall: avg('overall_score'),
    };
  });

  radarChartConfig = computed((): ChartConfiguration<'radar'> | null => {
    const s = this.avgScores();
    if (!s) return null;
    return {
      type: 'radar',
      data: {
        labels: ['NER', 'NLI', 'Summary', 'Translation'],
        datasets: [{
          label: this.run()?.model_name || 'Model',
          data: [s.ner ?? 0, s.nli ?? 0, s.summary ?? 0, s.translation ?? 0],
          backgroundColor: 'rgba(25, 118, 210, 0.2)',
          borderColor: '#1976d2',
          pointBackgroundColor: '#1976d2',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#1976d2',
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            beginAtZero: true,
            max: 10,
            ticks: { stepSize: 2 },
          },
        },
        plugins: { legend: { display: false } },
      },
    };
  });

  scoreDistributionConfig = computed((): ChartConfiguration<'bar'> | null => {
    const items = this.outputs();
    if (items.length === 0) return null;
    const bins = [0, 0, 0, 0, 0]; // 0-3, 3-5, 5-7, 7-9, 9-10
    for (const o of items) {
      const score = o.overall_score;
      if (score == null) continue;
      if (score < 3) bins[0]++;
      else if (score < 5) bins[1]++;
      else if (score < 7) bins[2]++;
      else if (score < 9) bins[3]++;
      else bins[4]++;
    }
    return {
      type: 'bar',
      data: {
        labels: ['0-3', '3-5', '5-7', '7-9', '9-10'],
        datasets: [{
          label: 'Articles',
          data: bins,
          backgroundColor: ['#ef5350', '#ff9800', '#ffca28', '#66bb6a', '#43a047'],
          borderRadius: 4,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (ctx) => `${ctx.parsed.y} articles` } },
        },
        scales: {
          x: { title: { display: true, text: 'Score Range' } },
          y: { beginAtZero: true, title: { display: true, text: 'Count' }, ticks: { stepSize: 1 } },
        },
      },
    };
  });

  displayedColumns = ['article_id', 'ner_score', 'nli_score', 'summary_score', 'translation_score', 'overall_score', 'status', 'actions'];
  expandedOutput = signal<ModelOutput | null>(null);

  toggleExpand(output: ModelOutput) {
    this.expandedOutput.set(this.expandedOutput()?.id === output.id ? null : output);
  }

  private runId = '';
  private pollTimer: ReturnType<typeof setInterval> | null = null;

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.runId = this.route.snapshot.paramMap.get('id')!;
    this.loadRun();
    this.loadOutputs();
    this.startPolling();
  }

  ngOnDestroy() {
    this.stopPolling();
  }

  private startPolling() {
    this.pollTimer = setInterval(() => {
      const r = this.run();
      if (r && (r.status === 'RUNNING' || r.status === 'QUEUED')) {
        this.loadRun();
        this.loadOutputs();
      }
    }, 3000);
  }

  private stopPolling() {
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
  }

  loadRun() {
    this.api.getRun(this.runId).subscribe({
      next: (data) => this.run.set(data),
      error: () => this.snackBar.open('Failed to load run', 'Close', { duration: 3000 }),
    });
  }

  loadOutputs() {
    this.api.getRunOutputs(this.runId).subscribe({
      next: (data) => this.outputs.set(data),
    });
  }

  judgeRun() {
    this.judging.set(true);
    this.api.judgeRun(this.runId).subscribe({
      next: () => {
        this.judging.set(false);
        this.snackBar.open('LLM Judge started', 'Close', { duration: 3000 });
        this.loadOutputs();
      },
      error: (err) => {
        this.judging.set(false);
        this.snackBar.open('Judge failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  generateReport() {
    this.generatingReport.set(true);
    this.api.generateReport(this.runId).subscribe({
      next: () => {
        this.generatingReport.set(false);
        this.snackBar.open('Report generated', 'Close', { duration: 3000 });
      },
      error: (err) => {
        this.generatingReport.set(false);
        this.snackBar.open('Report generation failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  formatScore(value: number | null): string {
    return value !== null ? value.toFixed(2) : '—';
  }
}
