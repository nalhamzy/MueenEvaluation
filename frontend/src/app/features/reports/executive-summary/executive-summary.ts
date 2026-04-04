import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { JsonPipe } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-executive-summary',
  imports: [
    JsonPipe,
    MatButtonModule, MatIconModule, MatCardModule,
    MatSnackBarModule, MatProgressBarModule,
  ],
  templateUrl: './executive-summary.html',
  styleUrl: './executive-summary.scss',
})
export class ExecutiveSummary implements OnInit {
  report = signal<any>(null);
  loading = signal(false);
  regenerating = signal(false);
  exporting = signal(false);

  private runId = '';

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.runId = this.route.snapshot.paramMap.get('id')!;
    this.loadReport();
  }

  loadReport() {
    this.loading.set(true);
    this.api.getReportSummary(this.runId).subscribe({
      next: (data) => {
        this.report.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.snackBar.open('Failed to load report', 'Close', { duration: 3000 });
      },
    });
  }

  regenerate() {
    this.regenerating.set(true);
    this.api.generateReport(this.runId).subscribe({
      next: () => {
        this.regenerating.set(false);
        this.snackBar.open('Report regenerated', 'Close', { duration: 3000 });
        this.loadReport();
      },
      error: (err) => {
        this.regenerating.set(false);
        this.snackBar.open('Regeneration failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  exportJson() {
    this.exporting.set(true);
    this.api.exportReport(this.runId).subscribe({
      next: (data) => {
        this.exporting.set(false);
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `report-${this.runId}.json`;
        a.click();
        URL.revokeObjectURL(url);
        this.snackBar.open('Report exported', 'Close', { duration: 3000 });
      },
      error: (err) => {
        this.exporting.set(false);
        this.snackBar.open('Export failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  renderMarkdown(text: string): string {
    if (!text) return '';
    return text
      .split('\n\n')
      .map(paragraph => `<p>${paragraph.replace(/\n/g, '<br>')}</p>`)
      .join('');
  }
}
