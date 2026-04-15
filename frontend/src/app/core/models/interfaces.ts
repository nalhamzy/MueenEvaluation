export interface Article {
  id: string;
  title: string;
  body: string;
  source: string | null;
  date: string | null;
  status: 'PENDING' | 'GENERATING' | 'READY' | 'ERROR';
  created_at: string;
}

export interface UploadResponse {
  total: number;
  inserted: number;
  skipped: number;
  errors: string[];
}

export interface DatasetItem {
  id: string;
  article_id: string;
  ner_input: string | null;
  ner_reference: NerReference | null;
  summary_input: string | null;
  summary_reference: string | null;
  nli_input: string | null;
  nli_claims: NliClaim[] | null;
  translation_input: string | null;
  translation_reference: string | null;
  generated_at: string | null;
  teacher_model: string | null;
}

export interface NerReference {
  PERSON: string[];
  LOCATION: string[];
  ORGANIZATION: string[];
  MISC: string[];
  [key: string]: string[];
}

export interface NliClaim {
  claim: string;
  label: 'SUPPORTED' | 'REFUTED' | 'NOT_ENOUGH_INFO';
}

export interface DatasetStats {
  total_items: number;
  completed: number;
  pending: number;
}

export interface EvaluationRun {
  id: string;
  model_name: string;
  status: 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  started_at: string;
  completed_at: string | null;
  total_articles: number;
  processed_count: number;
  error_message: string | null;
}

export interface ModelOutput {
  id: string;
  run_id: string;
  dataset_item_id: string;
  article_id: string;
  ner_output: NerReference | null;
  summary_output: string | null;
  nli_output: NliClaim[] | null;
  translation_output: string | null;
  ner_score: number | null;
  summary_score: number | null;
  nli_score: number | null;
  translation_score: number | null;
  overall_score: number | null;
  judge_summary_rubric: any | null;
  judge_translation_rubric: any | null;
  status: string;
  error_message: string | null;
}

export interface ScoreBreakdown {
  task: string;
  score: number;
  details: any;
}

export interface ModelEntry {
  id: string;
  display_name: string;
  model_id: string;
  provider: string;
  provider_name: string;
  category: string;
  base_url: string | null;
  has_api_key: boolean;
}

export interface AppConfig {
  teacher_model: string;
  judge_model: string;
  student_models: string;
  openai_base_url: string | null;
  teacher_api_key: string;
  student_api_key: string;
  judge_api_key: string;
}
