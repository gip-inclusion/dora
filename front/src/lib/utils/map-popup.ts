// Construit le contenu d'une popup de carte sans interpréter de HTML
export function createPopupContent(
  title: string,
  description?: string | null
): HTMLElement {
  const container = document.createElement("div");
  const strong = document.createElement("strong");
  strong.textContent = title;
  container.append(strong, document.createElement("br"), description ?? "");
  return container;
}
