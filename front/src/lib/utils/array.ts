export function shuffleArray(array: Array<any>): Array<any> {
  return array
    .map((value) => ({ value, sortWeight: Math.random() }))
    .sort((a, b) => a.sortWeight - b.sortWeight)
    .map(({ value }) => value);
}
