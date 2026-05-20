/**
 * TrendCharts.tsx — React island for the Trends page.
 *
 * Renders three recharts charts from the build-time `stats.json` aggregate:
 *   1. Papers per year            — bar chart
 *   2. Method family by year      — stacked bar chart
 *   3. Subfield distribution      — bar chart
 *
 * recharts is React-only, so this component is hosted in `trends.astro` as an
 * island (`client:load`). The Astro page reads `stats.json` at build time and
 * passes the parsed object in as props — this component does no I/O.
 */

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

// ---------------------------------------------------------------------------
// Shape of site/src/data/stats.json (subset this component consumes).
// ---------------------------------------------------------------------------
export interface Stats {
  papers_per_year: Record<string, number>;
  method_family_by_year: Record<string, Record<string, number>>;
  subfield_distribution: Record<string, number>;
  method_family_distribution: Record<string, number>;
  totals: { papers: number; milestones: number; subfields: number };
}

interface Props {
  stats: Stats;
}

// Color palette — chosen for WCAG-AA contrast on light and dark surfaces.
const FAMILY_COLORS: Record<string, string> = {
  interpolation: '#0969da',
  'model-based': '#8250df',
  'learning-based': '#1a7f37',
};
const SUBFIELD_COLORS = ['#0969da', '#bc4c00', '#8250df', '#1a7f37'];
const FALLBACK_COLOR = '#57606a';

const AXIS_STYLE = { fontSize: 12 };
const GRID_COLOR = '#d0d7de';

export default function TrendCharts({ stats }: Props) {
  // --- Chart 1: papers per year -------------------------------------------
  const perYear = Object.keys(stats.papers_per_year)
    .sort()
    .map((year) => ({ year, papers: stats.papers_per_year[year] }));

  // --- Chart 2: method family by year (stacked) ---------------------------
  const families = Array.from(
    new Set(
      Object.values(stats.method_family_by_year).flatMap((m) => Object.keys(m)),
    ),
  ).sort();

  const familyByYear = Object.keys(stats.method_family_by_year)
    .sort()
    .map((year) => {
      const row: Record<string, string | number> = { year };
      const counts = stats.method_family_by_year[year];
      for (const fam of families) {
        row[fam] = counts[fam] ?? 0;
      }
      return row;
    });

  // --- Chart 3: subfield distribution -------------------------------------
  const subfieldData = Object.keys(stats.subfield_distribution)
    .sort()
    .map((subfield) => ({
      subfield,
      papers: stats.subfield_distribution[subfield],
    }));

  return (
    <div className="trend-charts">
      <figure className="chart-card">
        <figcaption className="chart-card__title">Papers per year</figcaption>
        <p className="chart-card__desc">
          Annual count of radio map estimation papers in the corpus.
        </p>
        <div className="chart-card__plot">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={perYear} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
              <CartesianGrid stroke={GRID_COLOR} strokeDasharray="3 3" />
              <XAxis dataKey="year" tick={AXIS_STYLE} />
              <YAxis allowDecimals={false} tick={AXIS_STYLE} />
              <Tooltip />
              <Bar dataKey="papers" name="Papers" fill="#0969da" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </figure>

      <figure className="chart-card">
        <figcaption className="chart-card__title">Method family by year</figcaption>
        <p className="chart-card__desc">
          How the mix of interpolation, model-based, and learning-based methods has shifted
          over time.
        </p>
        <div className="chart-card__plot">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={familyByYear} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
              <CartesianGrid stroke={GRID_COLOR} strokeDasharray="3 3" />
              <XAxis dataKey="year" tick={AXIS_STYLE} />
              <YAxis allowDecimals={false} tick={AXIS_STYLE} />
              <Tooltip />
              <Legend />
              {families.map((fam) => (
                <Bar
                  key={fam}
                  dataKey={fam}
                  name={fam}
                  stackId="family"
                  fill={FAMILY_COLORS[fam] ?? FALLBACK_COLOR}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
      </figure>

      <figure className="chart-card">
        <figcaption className="chart-card__title">Subfield distribution</figcaption>
        <p className="chart-card__desc">
          Number of papers in each of the four radio map estimation subfields.
        </p>
        <div className="chart-card__plot">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={subfieldData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
              <CartesianGrid stroke={GRID_COLOR} strokeDasharray="3 3" />
              <XAxis dataKey="subfield" tick={AXIS_STYLE} />
              <YAxis allowDecimals={false} tick={AXIS_STYLE} />
              <Tooltip />
              <Bar dataKey="papers" name="Papers" radius={[3, 3, 0, 0]}>
                {subfieldData.map((entry, i) => (
                  <Cell key={entry.subfield} fill={SUBFIELD_COLORS[i % SUBFIELD_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </figure>
    </div>
  );
}
