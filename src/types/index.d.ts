export {};

declare global {
  interface Window {
    // eslint-disable-next-line no-unused-vars
    plausible: (name: string, props: object) => void;
  }
}
