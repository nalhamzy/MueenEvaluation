import { Component, OnInit, signal } from '@angular/core';
import { Router } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatMenuModule } from '@angular/material/menu';
import { MatBadgeModule } from '@angular/material/badge';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ApiService } from '../../../core/services/api.service';
import { Article, UploadResponse } from '../../../core/models/interfaces';

@Component({
  selector: 'app-article-list',
  imports: [
    MatTableModule, MatButtonModule, MatIconModule,
    MatChipsModule, MatCardModule, MatSnackBarModule,
    MatProgressBarModule, MatMenuModule, MatBadgeModule,
    MatTooltipModule, MatDialogModule,
  ],
  templateUrl: './article-list.html',
  styleUrl: './article-list.scss',
})
export class ArticleList implements OnInit {
  articles = signal<Article[]>([]);
  loading = signal(false);
  uploading = signal(false);
  uploadResult = signal<UploadResponse | null>(null);
  counts = signal<{ total: number; by_status: Record<string, number> } | null>(null);

  displayedColumns = ['id', 'title', 'source', 'date', 'status', 'actions'];

  constructor(
    private api: ApiService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.loadArticles();
    this.loadCounts();
  }

  loadArticles() {
    this.loading.set(true);
    this.api.getArticles().subscribe({
      next: (data) => {
        this.articles.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.snackBar.open('Failed to load articles', 'Close', { duration: 3000 });
      },
    });
  }

  loadCounts() {
    this.api.getArticleCount().subscribe({
      next: (c) => this.counts.set(c),
    });
  }

  refresh() {
    this.loadArticles();
    this.loadCounts();
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    this.uploading.set(true);
    this.api.uploadArticles(file).subscribe({
      next: (result) => {
        this.uploadResult.set(result);
        this.uploading.set(false);
        this.snackBar.open(
          `Uploaded: ${result.inserted} inserted, ${result.skipped} skipped`,
          'Close',
          { duration: 5000 }
        );
        this.refresh();
      },
      error: (err) => {
        this.uploading.set(false);
        this.snackBar.open('Upload failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });

    input.value = '';
  }

  onRowClick(article: Article) {
    this.router.navigate(['/articles', article.id]);
  }

  deleteArticle(event: Event, article: Article) {
    event.stopPropagation();
    if (!confirm(`Delete article ${article.id}?`)) return;

    this.api.deleteArticle(article.id).subscribe({
      next: () => {
        this.snackBar.open(`Deleted ${article.id}`, 'Close', { duration: 3000 });
        this.refresh();
      },
      error: () => this.snackBar.open('Delete failed', 'Close', { duration: 3000 }),
    });
  }

  deleteAll() {
    if (!confirm('Delete ALL articles and their dataset items? This cannot be undone.')) return;

    this.api.deleteAllArticles().subscribe({
      next: () => {
        this.snackBar.open('All articles deleted', 'Close', { duration: 3000 });
        this.uploadResult.set(null);
        this.refresh();
      },
      error: () => this.snackBar.open('Delete failed', 'Close', { duration: 3000 }),
    });
  }

  resetErrors() {
    this.api.resetErrorArticles().subscribe({
      next: (res) => {
        this.snackBar.open(res.message, 'Close', { duration: 3000 });
        this.refresh();
      },
    });
  }

  triggerGeneration() {
    this.api.generateDataset(3).subscribe({
      next: (res) => this.snackBar.open(res.message, 'Close', { duration: 5000 }),
      error: (err) => this.snackBar.open(err.error?.detail || 'Failed', 'Close', { duration: 5000 }),
    });
  }
}
