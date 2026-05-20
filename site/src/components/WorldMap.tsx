import { useMemo } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

interface PaperLite {
  id: string;
  title: string;
  year: number;
  subfield: string;
  authors: string[];
}

interface InstitutionWithPapers {
  id: string;
  name: string;
  country: string;
  lat: number;
  lon: number;
  count: number;
  papers: PaperLite[];
}

interface Props {
  institutions: InstitutionWithPapers[];
  basePath: string;
}

// Color by the dominant subfield among an institution's papers.
const subfieldColor: Record<string, string> = {
  REM: '#3b82f6',                    // blue
  'spectrum-cartography': '#f59e0b', // amber
  'pathloss-prediction': '#10b981',  // green
  CKM: '#a855f7',                    // purple
};

function dominantSubfield(papers: PaperLite[]): string {
  const tally: Record<string, number> = {};
  for (const p of papers) tally[p.subfield] = (tally[p.subfield] ?? 0) + 1;
  let best = papers[0]?.subfield ?? 'REM';
  let max = 0;
  for (const [k, v] of Object.entries(tally)) {
    if (v > max) {
      best = k;
      max = v;
    }
  }
  return best;
}

// Marker radius: log-scale on count, between 6 and 22 px.
function radiusFor(count: number): number {
  return Math.min(22, 6 + Math.log2(count + 1) * 4);
}

export default function WorldMap({ institutions, basePath }: Props) {
  const markers = useMemo(
    () =>
      institutions.map((inst) => ({
        ...inst,
        color: subfieldColor[dominantSubfield(inst.papers)] ?? '#6b7280',
        radius: radiusFor(inst.count),
      })),
    [institutions],
  );

  return (
    <div
      style={{
        height: 540,
        width: '100%',
        borderRadius: 8,
        overflow: 'hidden',
        border: '1px solid #d1d5db',
      }}
    >
      <MapContainer
        center={[25, 10]}
        zoom={2}
        minZoom={2}
        scrollWheelZoom={false}
        worldCopyJump
        style={{ height: '100%', width: '100%' }}
        aria-label="World map of paper first-author institutions"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {markers.map((m) => (
          <CircleMarker
            key={m.id}
            center={[m.lat, m.lon]}
            radius={m.radius}
            pathOptions={{
              color: m.color,
              fillColor: m.color,
              fillOpacity: 0.55,
              weight: 1.5,
            }}
          >
            <Tooltip direction="top" offset={[0, -2]} opacity={1}>
              <strong>{m.name}</strong> — {m.count} paper{m.count === 1 ? '' : 's'}
            </Tooltip>
            <Popup maxWidth={360}>
              <div style={{ fontSize: 13, lineHeight: 1.4 }}>
                <div style={{ fontWeight: 600, marginBottom: 4 }}>{m.name}</div>
                <div style={{ color: '#6b7280', marginBottom: 6 }}>
                  {m.country} · {m.count} paper{m.count === 1 ? '' : 's'}
                </div>
                <ul
                  style={{
                    paddingLeft: 18,
                    margin: 0,
                    maxHeight: 240,
                    overflowY: 'auto',
                  }}
                >
                  {m.papers.map((p) => (
                    <li key={p.id} style={{ marginBottom: 4 }}>
                      <a
                        href={`${basePath}/matrix#${encodeURIComponent(p.id)}`}
                        style={{ color: '#2563eb' }}
                      >
                        {p.title}
                      </a>{' '}
                      <span style={{ color: '#6b7280' }}>
                        · {p.year} · {p.subfield}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
