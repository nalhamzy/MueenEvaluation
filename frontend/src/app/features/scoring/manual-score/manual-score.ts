import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { JsonPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Article, ScoreBreakdown } from '../../../core/models/interfaces';

@Component({
  selector: 'app-manual-score',
  imports: [
    FormsModule, MatCardModule, MatFormFieldModule,
    MatInputModule, MatSelectModule, MatButtonModule,
    MatIconModule, MatProgressSpinnerModule, JsonPipe,
  ],
  templateUrl: './manual-score.html',
  styleUrl: './manual-score.scss',
})
export class ManualScore implements OnInit {
  articles = signal<Article[]>([]);
  selectedArticleId = '';
  selectedTask = 'ner';
  rawOutput = '';
  scoring = signal(false);
  result = signal<ScoreBreakdown | null>(null);
  error = signal<string | null>(null);

  tasks = [
    { value: 'ner', label: 'NER (Named Entity Recognition)' },
    { value: 'summary', label: 'Abstractive Summary' },
    { value: 'nli', label: 'NLI (Fact Verification)' },
    { value: 'coref', label: 'Entity Coreference Resolution' },
    { value: 'translation', label: 'Translation (Eng→Arabic)' },
  ];

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getArticles().subscribe({
      next: (arts) => this.articles.set(arts),
    });
  }

  getScoreClass(score: number): string {
    if (score >= 7) return 'score-high';
    if (score >= 4) return 'score-mid';
    return 'score-low';
  }

  score() {
    if (!this.selectedArticleId || !this.rawOutput.trim()) return;

    this.scoring.set(true);
    this.result.set(null);
    this.error.set(null);

    this.api.scoreManual(this.selectedArticleId, this.selectedTask, this.rawOutput).subscribe({
      next: (res) => {
        this.result.set(res);
        this.scoring.set(false);
      },
      error: (err) => {
        this.error.set(err.error?.detail || err.message || 'Scoring failed');
        this.scoring.set(false);
      },
    });
  }
}
