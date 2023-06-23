import hexoid from "hexoid";

const generateId = hexoid();

export function randomId(): string {
  return generateId();
}

// Le min et le max sont inclus
// https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Math/random#obtenir_un_entier_al%C3%A9atoire_dans_un_intervalle_ferm%C3%A9
export function getRandomIntBetween(min: number, max: number): number {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
