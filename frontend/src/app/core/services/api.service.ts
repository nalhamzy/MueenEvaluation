import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Article, UploadResponse, DatasetItem, DatasetStats,
  EvaluationRun, ModelOutput, ScoreBreakdown, AppConfig, ModelEntry
} from '../models/interfaces';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private baseUrl = 'http://localhost:8111/api';

  constructor(private http: HttpClient) {}

  // --- Articles ---
  uploadArticles(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<UploadResponse>(`${this.baseUrl}/articles/upload`, formData);
  }

  getArticles(skip = 0, limit = 100): Observable<Article[]> {
    const params = new HttpParams().set('skip', skip).set('limit', limit);
    return this.http.get<Article[]>(`${this.baseUrl}/articles`, { params });
  }

  getArticle(id: string): Observable<Article> {
    return this.http.get<Article>(`${this.baseUrl}/articles/${id}`);
  }

  getArticleCount(): Observable<{ total: number; by_status: Record<string, number> }> {
    return this.http.get<any>(`${this.baseUrl}/articles/count`);
  }

  deleteArticle(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/articles/${id}`);
  }

  deleteAllArticles(): Observable<any> {
    return this.http.delete(`${this.baseUrl}/articles`, { params: { confirm: true } });
  }

  resetErrorArticles(): Observable<any> {
    return this.http.post(`${this.baseUrl}/articles/reset-status`, null);
  }

  // --- Dataset ---
  generateDataset(limit?: number): Observable<any> {
    const params = limit ? new HttpParams().set('limit', limit) : undefined;
    return this.http.post(`${this.baseUrl}/dataset/generate`, null, { params });
  }

  getDatasetItems(skip = 0, limit = 100): Observable<DatasetItem[]> {
    const params = new HttpParams().set('skip', skip).set('limit', limit);
    return this.http.get<DatasetItem[]>(`${this.baseUrl}/dataset`, { params });
  }

  getDatasetStats(): Observable<DatasetStats> {
    return this.http.get<DatasetStats>(`${this.baseUrl}/dataset/stats`);
  }

  getDatasetItem(articleId: string): Observable<DatasetItem> {
    return this.http.get<DatasetItem>(`${this.baseUrl}/dataset/${articleId}`);
  }

  // --- Runs ---
  createRun(modelName: string, apiKey?: string, baseUrl?: string, limit?: number | null): Observable<EvaluationRun> {
    return this.http.post<EvaluationRun>(`${this.baseUrl}/runs`, {
      model_name: modelName, api_key: apiKey, base_url: baseUrl, limit: limit || undefined
    });
  }

  getRuns(): Observable<EvaluationRun[]> {
    return this.http.get<EvaluationRun[]>(`${this.baseUrl}/runs`);
  }

  getRun(id: string): Observable<EvaluationRun> {
    return this.http.get<EvaluationRun>(`${this.baseUrl}/runs/${id}`);
  }

  cancelRun(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/runs/${id}`);
  }

  getRunOutputs(runId: string): Observable<ModelOutput[]> {
    return this.http.get<ModelOutput[]>(`${this.baseUrl}/runs/${runId}/outputs`);
  }

  getRunScores(runId: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/runs/${runId}/scores`);
  }

  // --- Manual evaluation (no API key) ---
  manualBrief(articleIds: string[]): Observable<string> {
    return this.http.post(`${this.baseUrl}/runs/manual/brief`,
      { article_ids: articleIds },
      { responseType: 'text' as 'json' }
    ) as unknown as Observable<string>;
  }

  manualUpload(modelName: string, outputs: any[]): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/runs/manual/upload`, {
      model_name: modelName,
      outputs,
    });
  }

  // --- Outputs ---
  getOutputs(runId: string): Observable<ModelOutput[]> {
    return this.http.get<ModelOutput[]>(`${this.baseUrl}/outputs/${runId}`);
  }

  getOutput(runId: string, articleId: string): Observable<ModelOutput> {
    return this.http.get<ModelOutput>(`${this.baseUrl}/outputs/${runId}/${articleId}`);
  }

  // --- Scoring ---
  scoreManual(articleId: string, task: string, modelOutput: string): Observable<ScoreBreakdown> {
    return this.http.post<ScoreBreakdown>(`${this.baseUrl}/scoring/score-manual`, {
      article_id: articleId, task, model_output: modelOutput
    });
  }

  judgeRun(runId: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/scoring/judge-run/${runId}`, null);
  }

  // --- Reports ---
  getReportSummary(runId: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/reports/summary/${runId}`);
  }

  generateReport(runId: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/reports/generate/${runId}`, null);
  }

  getComparison(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/reports/comparison`);
  }

  exportReport(runId: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/reports/export/${runId}`);
  }

  // --- Config ---
  getConfig(): Observable<AppConfig> {
    return this.http.get<AppConfig>(`${this.baseUrl}/config`);
  }

  updateConfig(config: Partial<AppConfig>): Observable<any> {
    return this.http.put(`${this.baseUrl}/config`, config);
  }

  // --- Model Registry ---
  getModels(): Observable<{ models: ModelEntry[] }> {
    return this.http.get<{ models: ModelEntry[] }>(`${this.baseUrl}/config/models`);
  }

  testModel(modelId: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/config/models/${modelId}/test`, null);
  }
}
