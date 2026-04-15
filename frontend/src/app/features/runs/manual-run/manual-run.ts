import { Component, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatStepperModule } from '@angular/material/stepper';
import { MatExpansionModule } from '@angular/material/expansion';
import { ApiService } from '../../../core/services/api.service';
import { DatasetItem } from '../../../core/models/interfaces';

@Component({
  selector: 'app-manual-run',
  imports: [
    FormsModule, RouterLink,
    MatCardModule, MatButtonModule, MatIconModule,
    MatFormFieldModule, MatInputModule, MatChipsModule,
    MatSnackBarModule, MatProgressBarModule,
    MatStepperModule, MatExpansionModule,
  ],
  templateUrl: './manual-run.html',
  styleUrl: './manual-run.scss',
})
export class ManualRun implements OnInit {
  datasetItems = signal<DatasetItem[]>([]);
  loading = signal(false);
  busy = signal(false);

  // Step 1: pick articles
  selectedIds = signal<Set<string>>(new Set());

  // Step 2: brief
  briefText = signal<string>('');

  // Step 3: upload outputs
  modelName = '';
  uploadedJson: any = null;
  uploadError = signal<string | null>(null);

  // Step 4: result
  resultRunId = signal<string | null>(null);
  resultMissing = signal<string[]>([]);
  resultErrors = signal<string[]>([]);
  resultScored = signal<number>(0);

  constructor(
    private api: ApiService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.loadDataset();
  }

  loadDataset() {
    this.loading.set(true);
    this.api.getDatasetItems(0, 1000).subscribe({
      next: (items) => {
        // Only items that have been generated
        this.datasetItems.set(items.filter(i => i.generated_at));
        this.loading.set(false);
      },
      error: () => this.loading.set(false),
    });
  }

  toggleArticle(id: string) {
    const next = new Set(this.selectedIds());
    if (next.has(id)) next.delete(id);
    else next.add(id);
    this.selectedIds.set(next);
  }

  selectAll() {
    const all = new Set(this.datasetItems().map(i => i.article_id));
    this.selectedIds.set(all);
  }

  selectFirstN(n: number) {
    const ids = this.datasetItems().slice(0, n).map(i => i.article_id);
    this.selectedIds.set(new Set(ids));
  }

  clearSelection() {
    this.selectedIds.set(new Set());
  }

  generateBrief() {
    const ids = Array.from(this.selectedIds());
    if (ids.length === 0) {
      this.snackBar.open('Select at least one article', 'Close', { duration: 3000 });
      return;
    }
    this.busy.set(true);
    this.api.manualBrief(ids).subscribe({
      next: (brief: string) => {
        this.briefText.set(brief);
        this.busy.set(false);
        this.snackBar.open(`Brief generated for ${ids.length} articles`, 'Close', { duration: 3000 });
      },
      error: (err) => {
        this.busy.set(false);
        this.snackBar.open('Brief failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  copyBrief() {
    navigator.clipboard.writeText(this.briefText()).then(() => {
      this.snackBar.open('Brief copied to clipboard', 'Close', { duration: 2000 });
    });
  }

  downloadBrief() {
    const blob = new Blob([this.briefText()], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'manual_evaluation_brief.md';
    a.click();
    URL.revokeObjectURL(url);
  }

  onFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    this.uploadError.set(null);

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        const parsed = JSON.parse(text);
        if (!parsed.outputs || !Array.isArray(parsed.outputs)) {
          throw new Error('JSON must have an "outputs" array');
        }
        this.uploadedJson = parsed;
        if (parsed.model_name && !this.modelName) {
          this.modelName = parsed.model_name;
        }
        this.snackBar.open(`Loaded ${parsed.outputs.length} outputs`, 'Close', { duration: 3000 });
      } catch (err: any) {
        this.uploadError.set('Invalid JSON: ' + err.message);
      }
    };
    reader.readAsText(file);
    input.value = '';
  }

  pasteJson(text: string) {
    this.uploadError.set(null);
    try {
      const parsed = JSON.parse(text);
      if (!parsed.outputs || !Array.isArray(parsed.outputs)) {
        throw new Error('JSON must have an "outputs" array');
      }
      this.uploadedJson = parsed;
      if (parsed.model_name && !this.modelName) {
        this.modelName = parsed.model_name;
      }
    } catch (err: any) {
      this.uploadError.set('Invalid JSON: ' + err.message);
    }
  }

  submitOutputs() {
    if (!this.uploadedJson) {
      this.snackBar.open('Upload or paste outputs JSON first', 'Close', { duration: 3000 });
      return;
    }
    if (!this.modelName.trim()) {
      this.snackBar.open('Enter a model name', 'Close', { duration: 3000 });
      return;
    }

    this.busy.set(true);
    this.api.manualUpload(this.modelName, this.uploadedJson.outputs).subscribe({
      next: (res) => {
        this.busy.set(false);
        this.resultRunId.set(res.run_id);
        this.resultScored.set(res.scored_count);
        this.resultMissing.set(res.missing || []);
        this.resultErrors.set(res.errors || []);
        this.snackBar.open(
          `Created run with ${res.scored_count} scored outputs`,
          'View Run',
          { duration: 5000 },
        ).onAction().subscribe(() => {
          this.router.navigate(['/runs', res.run_id]);
        });
      },
      error: (err) => {
        this.busy.set(false);
        this.snackBar.open('Upload failed: ' + (err.error?.detail || err.message), 'Close', { duration: 5000 });
      },
    });
  }

  goToRun() {
    const id = this.resultRunId();
    if (id) this.router.navigate(['/runs', id]);
  }
}
