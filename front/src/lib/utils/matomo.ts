declare global {
  const Matomo: any;
  const Piwik: any;
  interface Window {
    matomoAbTestingAsyncInit: any;
  }
}

interface MatomoTarget {
  attribute: string;
  inverted: string;
  type: string;
  value: string;
}

interface MatomoVariation {
  name: string;
  activate: (event: unknown) => void;
}

interface MatomoExperiment {
  name: string;
  includedTargets: MatomoTarget[];
  excludedTargets: MatomoTarget[];
  variations: MatomoVariation[];
}

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
