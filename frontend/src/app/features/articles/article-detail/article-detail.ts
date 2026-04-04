import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatTabsModule } from '@angular/material/tabs';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { JsonPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Article, DatasetItem } from '../../../core/models/interfaces';

@Component({
  selector: 'app-article-detail',
  imports: [
    MatCardModule, MatChipsModule, MatTabsModule,
    MatProgressSpinnerModule, JsonPipe,
  ],
  templateUrl: './article-detail.html',
  styleUrl: './article-detail.scss',
})
export class ArticleDetail implements OnInit {
  article = signal<Article | null>(null);
  datasetItem = signal<DatasetItem | null>(null);
  loading = signal(true);

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.api.getArticle(id).subscribe({
      next: (a) => {
        this.article.set(a);
        this.loading.set(false);
      },
    });
    this.api.getDatasetItem(id).subscribe({
      next: (item) => this.datasetItem.set(item),
      error: () => {},
    });
  }
}
