/**
 * LandscapeMatrix.tsx — Interactive landscape-matrix React island.
 *
 * View 3 of the research map. Receives the full `papers` array as a prop and
 * renders a sortable, filterable, fuzzy-searchable table.
 *
 * Stack:
 *  - TanStack Table v8 (@tanstack/react-table) — headless multi-column sort.
 *  - Fuse.js — fuzzy global search over title + authors + tldr.
 *
 * This is the ONLY component on the site that ships client JS; it is mounted
 * with `client:load` on matrix.astro and is otherwise fully isolated.
 */

import { useMemo, useState } from 'react';
import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type ColumnDef,
  type SortingState,
} from '@tanstack/react-table';
import Fuse from 'fuse.js';

// ---------------------------------------------------------------------------
// Types — mirrors the `Paper` shape exported by site/src/lib/data.ts.
// Kept local so the island stays self-contained (data.ts is build-time only).
// ---------------------------------------------------------------------------
interface Paper {
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
  subfield: string;
  method_family: string;
  method_detail?: string[];
  task: string[];
  input_modality: string;
  environment: string;
  dimensionality: string;
  supervision: string;
  datasets?: string[];
  citations?: number;
  is_milestone?: boolean;
  tags?: string[];
  added_date: string;
}

interface LandscapeMatrixProps {
  papers: Paper[];
}

// ---------------------------------------------------------------------------
// Facet configuration — the 8 classification enum fields from paper.schema.json.
// `array: true` marks fields whose value is a string[] (match if ANY value hits).
// ---------------------------------------------------------------------------
interface FacetConfig {
  key: keyof Paper;
  label: string;
  array: boolean;
}

const FACETS: FacetConfig[] = [
  { key: 'subfield', label: 'Subfield', array: false },
  { key: 'method_family', label: 'Method family', array: false },
  { key: 'method_detail', label: 'Method detail', array: true },
  { key: 'task', label: 'Task', array: true },
  { key: 'input_modality', label: 'Input modality', array: false },
  { key: 'environment', label: 'Environment', array: false },
  { key: 'dimensionality', label: 'Dimensionality', array: false },
  { key: 'supervision', label: 'Supervision', array: false },
];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Return `url` only if it is an http(s) link, otherwise `undefined`.
 *
 * Link values come from untrusted paper data; a hostile `javascript:` /
 * `data:` URL must never reach an `<a href>`. Kept local because this island
 * is fully self-contained (data.ts is build-time only).
 */
function safeHref(url?: string): string | undefined {
  if (!url) return undefined;
  try {
    const protocol = new URL(url).protocol;
    return protocol === 'http:' || protocol === 'https:' ? url : undefined;
  } catch {
    return undefined;
  }
}

/** Pick the best external link for a paper, in priority order. */
function bestLink(paper: Paper): string | undefined {
  const l = paper.links;
  if (!l) return undefined;
  const candidate =
    l.arxiv ?? l.project_page ?? l.pdf ?? l.code ?? (l.doi ? `https://doi.org/${l.doi}` : undefined);
  return safeHref(candidate);
}

/** Compact author display: first author + "et al." when there are more. */
function compactAuthors(authors: string[]): string {
  if (authors.length === 0) return '—';
  if (authors.length === 1) return authors[0];
  return `${authors[0]} et al.`;
}

/** Collect the sorted set of distinct values present for a facet field. */
function distinctValues(papers: Paper[], facet: FacetConfig): string[] {
  const set = new Set<string>();
  for (const p of papers) {
    const raw = p[facet.key];
    if (facet.array && Array.isArray(raw)) {
      for (const v of raw) set.add(String(v));
    } else if (raw != null && raw !== '') {
      set.add(String(raw));
    }
  }
  return [...set].sort((a, b) => a.localeCompare(b));
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
export default function LandscapeMatrix({ papers }: LandscapeMatrixProps) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [search, setSearch] = useState('');
  // Per-facet selected values. Empty Set => facet imposes no filter.
  const [facetSelections, setFacetSelections] = useState<Record<string, Set<string>>>(
    () => Object.fromEntries(FACETS.map((f) => [f.key as string, new Set<string>()])),
  );

  // Distinct enum values per facet — computed once from the full corpus.
  const facetOptions = useMemo(
    () => Object.fromEntries(FACETS.map((f) => [f.key as string, distinctValues(papers, f)])),
    [papers],
  );

  // Fuse index over title + authors + tldr — rebuilt only if the corpus changes.
  const fuse = useMemo(
    () =>
      new Fuse(papers, {
        keys: ['title', 'authors', 'tldr'],
        threshold: 0.4,
        ignoreLocation: true,
        minMatchCharLength: 2,
      }),
    [papers],
  );

  // Apply fuzzy search, then every active facet filter.
  const filteredPapers = useMemo(() => {
    const query = search.trim();
    const base = query ? fuse.search(query).map((r) => r.item) : papers;

    return base.filter((paper) => {
      for (const facet of FACETS) {
        const selected = facetSelections[facet.key as string];
        if (!selected || selected.size === 0) continue;
        const raw = paper[facet.key];
        if (facet.array && Array.isArray(raw)) {
          // Array field matches if ANY of its values is selected.
          if (!raw.some((v) => selected.has(String(v)))) return false;
        } else {
          if (!selected.has(String(raw))) return false;
        }
      }
      return true;
    });
  }, [papers, fuse, search, facetSelections]);

  // Column definitions for TanStack Table.
  const columns = useMemo<ColumnDef<Paper>[]>(
    () => [
      {
        accessorKey: 'title',
        header: 'Title',
        cell: ({ row }) => {
          const paper = row.original;
          const href = bestLink(paper);
          return href ? (
            <a href={href} target="_blank" rel="noopener noreferrer" className="lm-title-link">
              {paper.title}
            </a>
          ) : (
            <span>{paper.title}</span>
          );
        },
      },
      {
        id: 'authors',
        accessorFn: (p) => compactAuthors(p.authors),
        header: 'Authors',
        cell: ({ getValue }) => <span className="lm-authors">{getValue<string>()}</span>,
      },
      { accessorKey: 'year', header: 'Year' },
      { accessorKey: 'subfield', header: 'Subfield' },
      { accessorKey: 'method_family', header: 'Method family' },
      {
        id: 'method_detail',
        accessorFn: (p) => (p.method_detail ?? []).join(', '),
        header: 'Method detail',
        // Sort by the joined string for a stable order.
        sortingFn: 'alphanumeric',
      },
      {
        id: 'task',
        accessorFn: (p) => p.task.join(', '),
        header: 'Task',
        sortingFn: 'alphanumeric',
      },
      { accessorKey: 'environment', header: 'Environment' },
      { accessorKey: 'dimensionality', header: 'Dimensionality' },
    ],
    [],
  );

  const table = useReactTable({
    data: filteredPapers,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    enableMultiSort: true,
    isMultiSortEvent: () => true, // every header click adds to the sort stack
  });

  // Whether any filter (search or facet) is currently active.
  const anyFilterActive =
    search.trim().length > 0 ||
    Object.values(facetSelections).some((s) => s.size > 0);

  function clearFacet(facetKey: string) {
    setFacetSelections((prev) => ({ ...prev, [facetKey]: new Set<string>() }));
  }

  function clearFilters() {
    setSearch('');
    setFacetSelections(Object.fromEntries(FACETS.map((f) => [f.key as string, new Set<string>()])));
    setSorting([]);
  }

  return (
    <div className="lm-root">
      {/* ---- Controls -------------------------------------------------- */}
      <div className="lm-controls">
        <div className="lm-search">
          <label htmlFor="lm-search-input">Search papers</label>
          <input
            id="lm-search-input"
            type="search"
            placeholder="Search title, authors, or summary…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            autoComplete="off"
          />
        </div>

        <fieldset className="lm-facets">
          <legend>Filter by classification</legend>
          <div className="lm-facets-grid">
            {FACETS.map((facet) => {
              const facetKey = facet.key as string;
              const options = facetOptions[facetKey] ?? [];
              const selected = facetSelections[facetKey] ?? new Set<string>();
              const selectId = `lm-facet-${facetKey}`;
              return (
                <div className="lm-facet" key={facetKey}>
                  <label htmlFor={selectId}>
                    {facet.label}
                    {selected.size > 0 && (
                      <span className="lm-facet-count" aria-hidden="true">
                        {' '}
                        ({selected.size})
                      </span>
                    )}
                  </label>
                  <select
                    id={selectId}
                    multiple
                    size={Math.min(Math.max(options.length, 2), 5)}
                    value={[...selected]}
                    onChange={(e) => {
                      const picked = new Set(
                        Array.from(e.target.selectedOptions, (o) => o.value),
                      );
                      setFacetSelections((prev) => ({ ...prev, [facetKey]: picked }));
                    }}
                    aria-describedby={`${selectId}-hint`}
                  >
                    {options.map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>
                  <p id={`${selectId}-hint`} className="lm-facet-hint">
                    {selected.size > 0 ? (
                      <button
                        type="button"
                        className="lm-clear-facet"
                        onClick={() => clearFacet(facetKey)}
                      >
                        Clear {facet.label}
                      </button>
                    ) : (
                      <span className="sr-only">No {facet.label} filter active</span>
                    )}
                  </p>
                </div>
              );
            })}
          </div>
        </fieldset>

        <div className="lm-status">
          <p className="lm-count" role="status" aria-live="polite">
            Showing <strong>{filteredPapers.length}</strong> of{' '}
            <strong>{papers.length}</strong> papers
          </p>
          <button
            type="button"
            className="lm-clear-all"
            onClick={clearFilters}
            disabled={!anyFilterActive && sorting.length === 0}
          >
            Clear filters
          </button>
        </div>
      </div>

      {/* ---- Table ----------------------------------------------------- */}
      <div className="lm-table-wrapper" role="region" aria-label="Papers table" tabIndex={0}>
        <table className="lm-table">
          <caption className="sr-only">
            Radio map estimation papers. Click a column header to sort; click
            again to reverse, and additional headers to sort by multiple
            columns.
          </caption>
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  const sortDir = header.column.getIsSorted();
                  const sortIndex = header.column.getSortIndex();
                  const ariaSort =
                    sortDir === 'asc'
                      ? 'ascending'
                      : sortDir === 'desc'
                        ? 'descending'
                        : 'none';
                  return (
                    <th key={header.id} scope="col" aria-sort={ariaSort}>
                      {header.isPlaceholder ? null : (
                        <button
                          type="button"
                          className="lm-sort-btn"
                          onClick={header.column.getToggleSortingHandler()}
                          title="Sort by this column"
                        >
                          <span>
                            {flexRender(
                              header.column.columnDef.header,
                              header.getContext(),
                            )}
                          </span>
                          <span className="lm-sort-icon" aria-hidden="true">
                            {sortDir === 'asc' ? '▲' : sortDir === 'desc' ? '▼' : '↕'}
                            {sortDir && table.getState().sorting.length > 1 ? (
                              <sup className="lm-sort-rank">{sortIndex + 1}</sup>
                            ) : null}
                          </span>
                        </button>
                      )}
                    </th>
                  );
                })}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="lm-empty">
                  No papers match the current filters.{' '}
                  <button type="button" className="lm-clear-all" onClick={clearFilters}>
                    Clear filters
                  </button>
                </td>
              </tr>
            ) : (
              table.getRowModel().rows.map((row) => (
                <tr key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* ---- Scoped styles --------------------------------------------- */}
      <style>{`
        .lm-root {
          margin-top: 1.5rem;
        }
        .lm-controls {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          margin-bottom: 1.25rem;
        }
        .lm-search {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          max-width: 28rem;
        }
        .lm-search label {
          font-weight: 600;
          font-size: 0.9rem;
        }
        .lm-search input {
          padding: 0.5rem 0.75rem;
          font-size: 0.95rem;
          font-family: inherit;
          color: var(--color-text);
          background: var(--color-bg);
          border: 1px solid var(--color-border);
          border-radius: var(--radius);
        }
        .lm-facets {
          border: 1px solid var(--color-border);
          border-radius: var(--radius);
          padding: 0.75rem 1rem 1rem;
        }
        .lm-facets legend {
          font-weight: 600;
          font-size: 0.9rem;
          padding: 0 0.4rem;
        }
        .lm-facets-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
          gap: 0.85rem;
        }
        .lm-facet {
          display: flex;
          flex-direction: column;
          gap: 0.3rem;
        }
        .lm-facet label {
          font-weight: 600;
          font-size: 0.82rem;
        }
        .lm-facet-count {
          color: var(--color-primary);
          font-weight: 700;
        }
        .lm-facet select {
          font-family: inherit;
          font-size: 0.82rem;
          color: var(--color-text);
          background: var(--color-bg);
          border: 1px solid var(--color-border);
          border-radius: var(--radius);
          padding: 0.2rem;
        }
        .lm-facet select option {
          padding: 0.15rem 0.3rem;
        }
        .lm-facet-hint {
          margin: 0;
          min-height: 1.2rem;
        }
        .lm-clear-facet,
        .lm-clear-all {
          font-family: inherit;
          font-size: 0.78rem;
          color: var(--color-primary);
          background: transparent;
          border: 1px solid var(--color-border);
          border-radius: var(--radius);
          padding: 0.2rem 0.55rem;
          cursor: pointer;
        }
        .lm-clear-facet:hover,
        .lm-clear-all:hover {
          background: var(--color-surface);
          color: var(--color-primary-hover);
        }
        .lm-clear-all {
          font-size: 0.85rem;
          padding: 0.35rem 0.8rem;
        }
        .lm-clear-all:disabled {
          opacity: 0.45;
          cursor: not-allowed;
        }
        .lm-clear-facet:focus-visible,
        .lm-clear-all:focus-visible,
        .lm-sort-btn:focus-visible,
        .lm-search input:focus-visible,
        .lm-facet select:focus-visible,
        .lm-table-wrapper:focus-visible {
          outline: 2px solid var(--color-focus);
          outline-offset: 2px;
        }
        .lm-status {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 1rem;
          flex-wrap: wrap;
        }
        .lm-count {
          margin: 0;
          font-size: 0.95rem;
        }
        .lm-table-wrapper {
          overflow-x: auto;
          border: 1px solid var(--color-border);
          border-radius: var(--radius);
        }
        .lm-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 0.88rem;
        }
        .lm-table thead tr {
          background: var(--color-surface);
          border-bottom: 2px solid var(--color-border);
        }
        .lm-table th {
          padding: 0;
          text-align: left;
          white-space: nowrap;
        }
        .lm-sort-btn {
          display: flex;
          align-items: center;
          gap: 0.4rem;
          width: 100%;
          padding: 0.55rem 0.75rem;
          font-family: inherit;
          font-size: 0.85rem;
          font-weight: 600;
          color: var(--color-text);
          background: transparent;
          border: none;
          cursor: pointer;
          text-align: left;
        }
        .lm-sort-btn:hover {
          color: var(--color-primary);
        }
        .lm-sort-icon {
          font-size: 0.7rem;
          color: var(--color-text-muted);
        }
        .lm-sort-rank {
          font-size: 0.6rem;
          color: var(--color-primary);
          font-weight: 700;
        }
        .lm-table td {
          padding: 0.5rem 0.75rem;
          border-bottom: 1px solid var(--color-border);
          vertical-align: top;
        }
        .lm-table tbody tr:last-child td {
          border-bottom: none;
        }
        .lm-table tbody tr:hover {
          background: var(--color-surface);
        }
        .lm-title-link {
          font-weight: 600;
        }
        .lm-authors {
          color: var(--color-text-muted);
          white-space: nowrap;
        }
        .lm-empty {
          padding: 1.5rem 0.75rem;
          text-align: center;
          color: var(--color-text-muted);
        }
        @media (max-width: 640px) {
          .lm-facets-grid {
            grid-template-columns: 1fr 1fr;
          }
        }
        @media (max-width: 420px) {
          .lm-facets-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}
