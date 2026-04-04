import { Component, OnInit, signal, computed } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { NgClass } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../../core/services/api.service';
import { ModelOutput, DatasetItem, NerReference, NliClaim, CorefSpan } from '../../../core/models/interfaces';

interface EntityComparison {
  entity: string;
  category: string;
  status: 'match' | 'predicted-only' | 'reference-only';
}

interface ClaimComparison {
  claim: string;
  referenceLabel: string;
  predictedLabel: string;
  correct: boolean;
}

@Component({
  selector: 'app-output-detail',
  imports: [
    NgClass, RouterLink,
    MatCardModule, MatTabsModule, MatTableModule, MatChipsModule,
    MatIconModule, MatButtonModule, MatProgressBarModule, MatSnackBarModule,
  ],
  templateUrl: './output-detail.html',
  styleUrl: './output-detail.scss',
})
export class OutputDetail implements OnInit {
  output = signal<ModelOutput | null>(null);
  datasetItem = signal<DatasetItem | null>(null);
  loading = signal(true);

  private runId = '';
  private articleId = '';

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.runId = this.route.snapshot.paramMap.get('runId')!;
    this.articleId = this.route.snapshot.paramMap.get('articleId')!;
    this.loadData();
  }

  private loadData() {
    this.loading.set(true);
    this.api.getOutput(this.runId, this.articleId).subscribe({
      next: (data) => {
        this.output.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.snackBar.open('Failed to load model output', 'Close', { duration: 3000 });
      },
    });
    this.api.getDatasetItem(this.articleId).subscribe({
      next: (data) => this.datasetItem.set(data),
      error: () => this.snackBar.open('Failed to load dataset item', 'Close', { duration: 3000 }),
    });
  }

  // --- NER comparison ---
  nerEntities = computed((): EntityComparison[] => {
    const ref = this.datasetItem()?.ner_reference;
    const pred = this.output()?.ner_output;
    if (!ref && !pred) return [];
    const result: EntityComparison[] = [];
    const allCategories = new Set<string>([
      ...Object.keys(ref || {}),
      ...Object.keys(pred || {}),
    ]);
    for (const cat of allCategories) {
      const refEntities = new Set<string>((ref as any)?.[cat] || []);
      const predEntities = new Set<string>((pred as any)?.[cat] || []);
      for (const e of refEntities) {
        if (predEntities.has(e)) {
          result.push({ entity: e, category: cat, status: 'match' });
        } else {
          result.push({ entity: e, category: cat, status: 'reference-only' });
        }
      }
      for (const e of predEntities) {
        if (!refEntities.has(e)) {
          result.push({ entity: e, category: cat, status: 'predicted-only' });
        }
      }
    }
    return result;
  });

  // --- NLI comparison ---
  nliComparison = computed((): ClaimComparison[] => {
    const refClaims = this.datasetItem()?.nli_claims || [];
    const predClaims = this.output()?.nli_output || [];
    return refClaims.map((rc, i) => {
      const pc = predClaims[i];
      return {
        claim: rc.claim,
        referenceLabel: rc.label,
        predictedLabel: pc?.label || '—',
        correct: pc ? rc.label === pc.label : false,
      };
    });
  });

  // --- Coref ---
  refCoref = computed((): CorefSpan[] => this.datasetItem()?.coref_reference || []);
  predCoref = computed((): CorefSpan[] => this.output()?.coref_output || []);

  formatScore(value: number | null): string {
    return value !== null ? value.toFixed(2) : '—';
  }
}
