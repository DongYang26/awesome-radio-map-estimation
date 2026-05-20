/**
 * data.ts — Load repo-root YAML data at build time.
 *
 * The data directory lives OUTSIDE site/ at ../../data relative to this file.
 * We use Node fs.readFileSync + js-yaml because the data directory is outside
 * the Astro project root and import.meta.glob cannot reach it.
 *
 * THIS MODULE IS BUILD-TIME ONLY (Astro SSG). Do not import on the client.
 */

import { readFileSync, readdirSync } from 'node:fs';
import { resolve, join, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'js-yaml';

// ---------------------------------------------------------------------------
// Path resolution — relative to THIS file (site/src/lib/data.ts)
// ---------------------------------------------------------------------------
const THIS_DIR = resolve(fileURLToPath(import.meta.url), '..');
const DATA_DIR = resolve(THIS_DIR, '../../../data');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function loadYaml<T>(filePath: string): T {
  const raw = readFileSync(filePath, 'utf-8');
  // js-yaml v4 `load()` is safe-by-default (equivalent to v3's `safeLoad`).
  return yaml.load(raw) as T;
}

/**
 * Return `url` only if it is an http(s) link, otherwise `undefined`.
 *
 * Paper/dataset link values are rendered into `<a href>` attributes. The data
 * schemas accept any URI, so a hostile `javascript:` / `data:` URL could become
 * a stored-XSS vector. Use this helper for every untrusted link `href`.
 */
export function safeHref(url?: string): string | undefined {
  if (!url) return undefined;
  try {
    const protocol = new URL(url).protocol;
    return protocol === 'http:' || protocol === 'https:' ? url : undefined;
  } catch {
    return undefined;
  }
}

// ---------------------------------------------------------------------------
// Papers
// ---------------------------------------------------------------------------
export interface Paper {
  id: string;
  title: string;
  authors: string[];
  year: number;
  venue?: string;
  abstract?: string;
  tldr?: string;
  links?: {
    arxiv?: string;
    pdf?: string;
    code?: string;
    project_page?: string;
    doi?: string;
  };
  subfield: 'REM' | 'spectrum-cartography' | 'pathloss-prediction' | 'CKM';
  method_family: 'interpolation' | 'model-based' | 'learning-based';
  method_detail?: string[];
  task: string[];
  input_modality: 'sparse-measurements' | 'environment-map' | 'both';
  environment: 'indoor' | 'outdoor' | 'both';
  dimensionality: '2D' | '3D';
  supervision: 'supervised' | 'self-supervised' | 'unsupervised' | 'semi-supervised' | 'n/a';
  datasets?: string[];
  citations?: number;
  is_milestone?: boolean;
  tags?: string[];
  added_date: string;
}

export function loadPapers(): Paper[] {
  const papersDir = join(DATA_DIR, 'papers');
  const files = readdirSync(papersDir)
    .filter((f) => extname(f) === '.yml' || extname(f) === '.yaml')
    .sort();
  const papers: Paper[] = files.map((f) => {
    const data = loadYaml<Paper>(join(papersDir, f));
    return data;
  });
  // Deterministic sort by id
  papers.sort((a, b) => a.id.localeCompare(b.id));
  return papers;
}

// ---------------------------------------------------------------------------
// Taxonomy
// ---------------------------------------------------------------------------
export interface TaxonomyNode {
  id: string;
  label: string;
  description?: string;
  children?: TaxonomyNode[];
}

export interface TaxonomyData {
  taxonomy: TaxonomyNode[];
}

export function loadTaxonomy(): TaxonomyData {
  return loadYaml<TaxonomyData>(join(DATA_DIR, 'taxonomy.yml'));
}

// ---------------------------------------------------------------------------
// Datasets
// ---------------------------------------------------------------------------
export interface BenchmarkRow {
  paper_id: string;
  metric: string;
  value: number;
}

export interface Dataset {
  id: string;
  name: string;
  description: string;
  link: string;
  papers_using?: string[];
  benchmark?: BenchmarkRow[];
}

export interface DatasetsData {
  datasets: Dataset[];
}

export function loadDatasets(): DatasetsData {
  return loadYaml<DatasetsData>(join(DATA_DIR, 'datasets.yml'));
}

// ---------------------------------------------------------------------------
// Reading path
// ---------------------------------------------------------------------------
export interface ReadingStep {
  order: number;
  paper_id: string;
  why: string;
}

export interface ReadingPathData {
  steps: ReadingStep[];
}

export function loadReadingPath(): ReadingPathData {
  return loadYaml<ReadingPathData>(join(DATA_DIR, 'reading-path.yml'));
}

// ---------------------------------------------------------------------------
// Convenience re-exports (pre-loaded singletons for use in .astro files)
// ---------------------------------------------------------------------------
export const papers: Paper[] = loadPapers();
export const taxonomy: TaxonomyData = loadTaxonomy();
export const datasets: DatasetsData = loadDatasets();
export const readingPath: ReadingPathData = loadReadingPath();
