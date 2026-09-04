// Aperçu d'un fichier CSV : on ne lit que le début du fichier (les sources
// peuvent peser des dizaines de Mo) et on en montre les premières lignes.
// Fonction pure, testée sans réseau.

export type CsvPreview = {
  readonly delimiter: string;
  readonly header: ReadonlyArray<string>;
  readonly rows: ReadonlyArray<ReadonlyArray<string>>;
  readonly truncated: boolean;
};

const CANDIDATES = [";", ",", "\t", "|"] as const;

function splitLine(line: string, delimiter: string): string[] {
  const cells: string[] = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const char = line[i] ?? "";
    if (char === '"') {
      if (quoted && line[i + 1] === '"') {
        cell += '"';
        i += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === delimiter && !quoted) {
      cells.push(cell);
      cell = "";
    } else {
      cell += char;
    }
  }
  cells.push(cell);
  return cells;
}

export function detectDelimiter(sample: string): string {
  const firstLines = sample.split(/\r?\n/, 5).filter((line) => line.length > 0);
  let best = ",";
  let bestScore = 0;
  for (const candidate of CANDIDATES) {
    const counts = firstLines.map((line) => splitLine(line, candidate).length);
    const min = Math.min(...counts);
    // Un bon délimiteur découpe chaque ligne en plusieurs colonnes, de façon
    // stable d'une ligne à l'autre.
    const score = min > 1 && counts.every((count) => count === min) ? min : 0;
    if (score > bestScore) {
      bestScore = score;
      best = candidate;
    }
  }
  return best;
}

export function previewCsv(
  sample: string,
  args: { maxRows: number; complete: boolean },
): CsvPreview {
  const lines = sample.split(/\r?\n/).filter((line) => line.length > 0);
  // Si l'échantillon est coupé, la dernière ligne est probablement partielle.
  const usable = args.complete ? lines : lines.slice(0, -1);
  const delimiter = detectDelimiter(usable.slice(0, 5).join("\n"));
  const [headerLine, ...rest] = usable;
  const header = headerLine === undefined ? [] : splitLine(headerLine, delimiter);
  const rows = rest.slice(0, args.maxRows).map((line) => splitLine(line, delimiter));
  return {
    delimiter,
    header,
    rows,
    truncated: !args.complete || rest.length > args.maxRows,
  };
}
