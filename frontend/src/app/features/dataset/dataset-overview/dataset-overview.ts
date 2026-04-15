import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatExpansionModule } from '@angular/material/expansion';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { DatasetItem, DatasetStats } from '../../../core/models/interfaces';

@Component({
  selector: 'app-dataset-overview',
  imports: [
    MatCardModule, MatButtonModule, MatIconModule,
    MatTableModule, MatChipsModule, MatSnackBarModule,
    MatProgressBarModule, MatFormFieldModule, MatInputModule,
    MatExpansionModule, FormsModule, DatePipe,
  ],
  templateUrl: './dataset-overview.html',
  styleUrl: './dataset-overview.scss',
})
export class DatasetOverview implements OnInit, OnDestroy {
  stats = signal<DatasetStats | null>(null);
  items = signal<DatasetItem[]>([]);
  loading = signal(false);
  generating = signal(false);
  limit = 3;
  selectedItem = signal<DatasetItem | null>(null);

  displayedColumns = ['article_id', 'teacher_model', 'generated_at', 'has_ner', 'has_summary', 'has_nli', 'has_translation'];

  private pollTimer: any = null;

  constructor(
    private api: ApiService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.loadData();
  }

  ngOnDestroy() {
    this.stopPolling();
  }

  loadData() {
    this.loading.set(true);
    this.api.getDatasetStats().subscribe({
      next: (s) => this.stats.set(s),
    });
    this.api.getDatasetItems().subscribe({
      next: (items) => {
        this.items.set(items);
        this.loading.set(false);
      },
      error: () => this.loading.set(false),
    });
  }

  generate() {
    this.generating.set(true);
    this.api.generateDataset(this.limit).subscribe({
      next: (res) => {
        this.snackBar.open(res.message, 'Close', { duration: 5000 });
        this.startPolling();
      },
      error: (err) => {
        this.generating.set(false);
        this.snackBar.open('Generation failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  startPolling() {
    this.stopPolling();
    this.pollTimer = setInterval(() => {
      this.api.getDatasetStats().subscribe({
        next: (s) => {
          this.stats.set(s);
          if (s.pending === 0) {
            this.generating.set(false);
            this.stopPolling();
            this.loadData();
            this.snackBar.open('Dataset generation complete!', 'Close', { duration: 3000 });
          }
        },
      });
      this.api.getDatasetItems().subscribe({
        next: (items) => this.items.set(items),
      });
    }, 5000);
  }

  stopPolling() {
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
  }

  onRowClick(item: DatasetItem) {
    this.selectedItem.set(this.selectedItem()?.id === item.id ? null : item);
  }

  viewDetail(item: DatasetItem) {
    this.router.navigate(['/articles', item.article_id]);
  }

  completionPercent(): number {
    const s = this.stats();
    if (!s || s.total_items === 0) return 0;
    return Math.round((s.completed / s.total_items) * 100);
  }
}
