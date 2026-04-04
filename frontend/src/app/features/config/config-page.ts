import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../core/services/api.service';
import { AppConfig } from '../../core/models/interfaces';

@Component({
  selector: 'app-config-page',
  imports: [
    FormsModule, MatCardModule, MatFormFieldModule,
    MatInputModule, MatButtonModule, MatIconModule,
    MatSnackBarModule,
  ],
  templateUrl: './config-page.html',
  styleUrl: './config-page.scss',
})
export class ConfigPage implements OnInit {
  config = signal<AppConfig | null>(null);
  loading = signal(true);

  // Editable fields
  teacherModel = '';
  judgeModel = '';
  studentModels = '';
  baseUrl = '';

  constructor(
    private api: ApiService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.api.getConfig().subscribe({
      next: (cfg) => {
        this.config.set(cfg);
        this.teacherModel = cfg.teacher_model;
        this.judgeModel = cfg.judge_model;
        this.studentModels = cfg.student_models;
        this.baseUrl = cfg.openai_base_url || '';
        this.loading.set(false);
      },
      error: () => this.loading.set(false),
    });
  }

  save() {
    this.api.updateConfig({
      teacher_model: this.teacherModel,
      judge_model: this.judgeModel,
      student_models: this.studentModels,
      openai_base_url: this.baseUrl || undefined,
    } as any).subscribe({
      next: () => this.snackBar.open('Config saved', 'Close', { duration: 3000 }),
      error: () => this.snackBar.open('Failed to save config', 'Close', { duration: 3000 }),
    });
  }
}
