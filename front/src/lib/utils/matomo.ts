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

type MatomoEvent = {
  category: string;
  action: string;
  name?: string;
  value?: number;
};

export function registerMatomoExperiment(experiment: MatomoExperiment) {
  // Matomo n'est disponible que côté navigateur : on ne fait rien lors du
  // rendu serveur, sans quoi l'accès à `window` provoque une erreur.
  if (typeof window === "undefined") {
    return;
  }

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
export function registerRechercheTextuelleExperiment(onActivate) {
  registerMatomoExperiment({
    name: "rechercheTextuelle",
    includedTargets: [
      {
        attribute: "path",
        inverted: "0",
        type: "equals_simple",
        value: "/",
      },
    ],
    excludedTargets: [],
    variations: [
      {
        name: "original",
        activate: () => {},
      },
      {
        name: "Variation1",
        activate: onActivate,
      },
    ],
  });
}

export function trackMatomoEvent({
  category,
  action,
  name,
  value,
}: MatomoEvent): void {
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
