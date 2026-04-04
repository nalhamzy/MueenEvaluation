import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { Router } from '@angular/router';
import { DatePipe, UpperCasePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';
import { ApiService } from '../../../core/services/api.service';
import { EvaluationRun, ModelEntry } from '../../../core/models/interfaces';

@Component({
  selector: 'app-run-list',
  imports: [
    DatePipe, UpperCasePipe, FormsModule,
    MatTableModule, MatButtonModule, MatIconModule,
    MatChipsModule, MatCardModule, MatSnackBarModule,
    MatProgressBarModule, MatFormFieldModule, MatInputModule,
    MatSelectModule, MatTooltipModule,
  ],
  templateUrl: './run-list.html',
  styleUrl: './run-list.scss',
})
export class RunList implements OnInit, OnDestroy {
  runs = signal<EvaluationRun[]>([]);
  models = signal<ModelEntry[]>([]);
  loading = signal(false);
  showForm = signal(false);
  creating = signal(false);
  testing = signal<string | null>(null);

  selectedModelId = '';
  customModelName = '';
  apiKey = '';
  baseUrl = '';
  articleLimit: number | null = 3;
  useCustom = false;

  displayedColumns = ['model_name', 'status', 'progress', 'started_at', 'completed_at', 'actions'];

  private pollTimer: ReturnType<typeof setInterval> | null = null;

  constructor(
    private api: ApiService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.loadRuns();
    this.loadModels();
    this.pollTimer = setInterval(() => this.loadRuns(), 5000);
  }

  ngOnDestroy() {
    if (this.pollTimer) clearInterval(this.pollTimer);
  }

  loadRuns() {
    this.loading.set(true);
    this.api.getRuns().subscribe({
      next: (data) => {
        this.runs.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.snackBar.open('Failed to load runs', 'Close', { duration: 3000 });
      },
    });
  }

  loadModels() {
    this.api.getModels().subscribe({
      next: (data) => this.models.set(data.models),
    });
  }

  toggleForm() {
    this.showForm.update(v => !v);
  }

  get modelCategories(): string[] {
    const cats = new Set(this.models().map(m => m.category));
    return [...cats];
  }

  modelsInCategory(category: string): ModelEntry[] {
    return this.models().filter(m => m.category === category);
  }

  testModel(modelId: string) {
    this.testing.set(modelId);
    this.api.testModel(modelId).subscribe({
      next: (res) => {
        this.testing.set(null);
        if (res.status === 'ok') {
          this.snackBar.open(`${res.message}`, 'Close', { duration: 3000 });
        } else if (res.status === 'no_key') {
          this.snackBar.open(`No API key: ${res.message}`, 'Close', { duration: 5000 });
        } else {
          this.snackBar.open(`Error: ${res.message}`, 'Close', { duration: 5000 });
        }
      },
      error: (err) => {
        this.testing.set(null);
        this.snackBar.open('Test failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  createRun() {
    const modelName = this.useCustom ? this.customModelName.trim() : this.selectedModelId;
    if (!modelName) return;

    this.creating.set(true);
    this.api.createRun(
      modelName,
      this.apiKey.trim() || undefined,
      this.baseUrl.trim() || undefined,
      this.articleLimit,
    ).subscribe({
      next: (run) => {
        this.creating.set(false);
        this.showForm.set(false);
        this.selectedModelId = '';
        this.customModelName = '';
        this.apiKey = '';
        this.baseUrl = '';
        this.snackBar.open(`Run started: ${run.model_name}`, 'Close', { duration: 3000 });
        this.loadRuns();
      },
      error: (err) => {
        this.creating.set(false);
        this.snackBar.open('Failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  cancelRun(event: Event, run: EvaluationRun) {
    event.stopPropagation();
    if (!confirm(`Cancel run ${run.id}?`)) return;
    this.api.cancelRun(run.id).subscribe({
      next: () => {
        this.snackBar.open('Run cancelled', 'Close', { duration: 3000 });
        this.loadRuns();
      },
      error: () => this.snackBar.open('Cancel failed', 'Close', { duration: 3000 }),
    });
  }

  onRowClick(run: EvaluationRun) {
    this.router.navigate(['/runs', run.id]);
  }

  progressPercent(run: EvaluationRun): number {
    if (!run.total_articles) return 0;
    return Math.round((run.processed_count / run.total_articles) * 100);
  }
}
