declare global {
  const Matomo: any;
  const Piwik: any;
  interface Window {
    matomoAbTestingAsyncInit: any;
    _paq?: any[][];
  }
}

type MatomoTarget = {
  attribute: string;
  inverted: string;
  type: string;
  value: string;
};

type MatomoVariation = {
  name: string;
  activate: (event: unknown) => void;
};

type MatomoExperiment = {
  name: string;
  includedTargets: MatomoTarget[];
  excludedTargets: MatomoTarget[];
  variations: MatomoVariation[];
};

export function registerMatomoExperiment(experiment: MatomoExperiment) {
  function createExperiment() {
    const Experiment = Matomo.AbTesting.Experiment;

    const myExperiment = new Experiment(experiment);

    myExperiment.getActivatedVariationName();
  }

  if ("object" === typeof Piwik && "object" === typeof Matomo.AbTesting) {
    // if matomo.js was embedded before this code
    createExperiment();
  } else {
    // if matomo.js is loaded after this code
    window.matomoAbTestingAsyncInit = createExperiment;
  }
}

export function trackMatomoEvent(
  category: string,
  action: string,
  name?: string,
  value?: number
): void {
  if (typeof window === "undefined" || !(window as any)._paq) {
    return;
  }

  const args: any[] = ["trackEvent", category, action];
  if (name !== undefined) {
    args.push(name);
  }
  if (value !== undefined) {
    args.push(value);
  }

  (window as any)._paq.push(args);
}
