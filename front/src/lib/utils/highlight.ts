export type HighlightSegment = { text: string; match: boolean };

// Découpe le texte en segments, `match` indiquant ceux qui correspondent à l'un
// des motifs ; une seule regex pour tous, afin qu'ils ne se chevauchent pas, avec
// les plus longs d'abord pour que « par » n'empêche pas de surligner « paris ».
// Les motifs ne doivent pas contenir de groupe capturant, qui décalerait les
// segments renvoyés par `split`
export function splitHighlight(
  text: string,
  patterns: string[]
): HighlightSegment[] {
  if (!patterns.length) {
    return [{ text, match: false }];
  }
  const alternatives = [...patterns].sort((a, b) => b.length - a.length);
  return text
    .split(new RegExp(`(${alternatives.join("|")})`, "iu"))
    .map((part, index) => ({ text: part, match: index % 2 === 1 }))
    .filter((segment) => segment.text);
}
