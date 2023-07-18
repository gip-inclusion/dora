import { formatPhoneNumber } from "./misc";

// prettier-ignore
export function renderPrescriberAcceptMessage(data: Record<string, string | undefined>) {
  let result = `Bonjour,

Nous avons le plaisir de vous informer que votre demande d’orientation a été acceptée ! 🎉

Votre demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} à été validée par la structure « ${data.serviceStructureName} ».

Si vous avez des questions supplémentaires ou si vous souhaitez obtenir plus d’informations, n’hésitez pas à nous contacter.

Cordialement,`;

  if(data.serviceContactName) {
    result += `\n${data.serviceContactName}`;
  }
  if(data.serviceContactEmail) {
    result += `\n${data.serviceContactEmail}`;
  }
  if(data.serviceContactPhone) {
    result += `\n${data.serviceContactPhone}`;
  }
  if(data.serviceStructureName) {
    result += `\n${data.serviceStructureName}`;
  }

  return result;
}

// prettier-ignore
export function renderBeneficiaryAcceptMessage(data: Record<string, string | undefined>) {
let result = `Bonjour,

Nous avons le plaisir de vous informer que la structure « ${data.serviceStructureName} » a validé la demande réalisée par ${data.referentFirstName} ${data.referentLastName} concernant votre positionnement sur « ${data.serviceName} ».

Pour toute information supplémentaire, n’hésitez pas à contacter votre référent${ data.structurePhone ? ` ou la structure directement au ${formatPhoneNumber(data.structurePhone)}`: ""}.

Nous vous souhaitons une bonne continuation.

Bien à vous,`;

  if(data.serviceContactName) {
    result += `\n${data.serviceContactName}`;
  }
  if(data.serviceContactEmail) {
    result += `\n${data.serviceContactEmail}`;
  }
  if(data.serviceContactPhone) {
    result += `\n${data.serviceContactPhone}`;
  }
  if(data.serviceStructureName) {
    result += `\n${data.serviceStructureName}`;
  }

  return result;
}

// prettier-ignore
export function renderRejectMessage(
  reasons: string[],
  reasonsChoices: { value: string; label: string }[],
  data: Record<string, string | undefined>
): string {
  if (reasons.length === 0) {
    return "";
  }

  const textStart = `Bonjour ${data.referentFirstName} ${data.referentLastName},`;
  let textEnd = `Bien à vous,`;

  if(data.serviceContactName) {
    textEnd += `\n${data.serviceContactName}`;
  }
  if(data.serviceContactEmail) {
    textEnd += `\n${data.serviceContactEmail}`;
  }
  if(data.serviceContactPhone) {
    textEnd += `\n${data.serviceContactPhone}`;
  }
  if(data.serviceStructureName) {
    textEnd += `\n${data.serviceStructureName}`;
  }

  if (reasons.length > 1) {
    return textStart + `

Nous vous remercions d’avoir soumis la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Après avoir examiné attentivement la situation, nous regrettons de vous informer que nous ne pouvons pas donner suite à cette demande pour le moment. Plusieurs raisons spécifiques ont été identifiées, notamment :

${reasons.map((reason) => `- ${reasonsChoices.find((choice) => choice.value === reason)?.label}`).join("\n")}

Ces facteurs combinés ont conduit à notre décision de ne pas donner suite à la demande actuelle.

Si vous avez des questions supplémentaires ou si vous souhaitez discuter plus en détail des raisons du refus, n’hésitez pas à nous contacter.

`+ textEnd;
  }

  if (reasons[0] === "bénéficiaire-non-joignable") {
    return textStart + `

Après avoir effectué plusieurs tentatives pour contacter ${data.beneficiaryFirstName} ${data.beneficiaryLastName}, nous n’avons pas réussi à le ou la joindre. Malgré nos efforts répétés, nous n’avons pas pu recueillir les informations nécessaires pour donner une réponse positive à la demande.

Nous tenions à vous remercier pour avoir positionné ${data.beneficiaryFirstName} ${data.beneficiaryLastName} sur le service « ${data.serviceName} » , et nous regrettons sincèrement de ne pas pouvoir donner suite à cette demande.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;
  } else if (reasons[0] === "bénéficiaire-absent") {
    return textStart + `

Nous vous contactons aujourd’hui pour vous informer qu’à la suite de notre entretien prévu avec ${data.beneficiaryFirstName} ${data.beneficiaryLastName}, celui-ci/celle-ci n’a malheureusement pas honoré le rendez-vous convenu.

Sans l’opportunité d’échanger avec ${data.beneficiaryFirstName} ${data.beneficiaryLastName} et de recueillir les informations nécessaires, nous ne sommes pas en mesure de donner une réponse favorable à sa demande.

Nous tenions à vous remercier pour avoir positionné ${data.beneficiaryFirstName} ${data.beneficiaryLastName} sur le service « ${data.serviceName} », et nous regrettons sincèrement de ne pas pouvoir donner suite à cette demande.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "bénéficiaire-en-emploi") {
    return textStart + `

Nous tenons à vous informer que nous avons examiné attentivement la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Malheureusement, nous ne sommes pas en mesure de donner une suite favorable à cette demande pour le moment.

Nous avons été informé que ${data.beneficiaryFirstName} ${data.beneficiaryLastName} est actuellement en emploi et indisponible pour bénéficier de notre service à l’heure actuelle.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "bénéficiaire-en-formation") {
    return textStart + `

Nous tenons à vous informer que nous avons examiné attentivement la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Malheureusement, nous ne sommes pas en mesure de donner une suite favorable à cette demande pour le moment.

Nous avons été informé que ${data.beneficiaryFirstName} ${data.beneficiaryLastName} est actuellement en formation et indisponible pour bénéficier de notre service à l’heure actuelle.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "bénéficiaire-non-éligible") {
    return textStart + `

Nous vous remercions d’avoir soumis la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Après l’avoir étudiée attentivement, nous regrettons de vous informer que nous ne pouvons pas donner suite à cette demande pour le moment.

Après avoir évalué les critères et les prérequis nécessaires, nous constatons que ${data.beneficiaryFirstName} ${data.beneficiaryLastName} ne remplit pas les conditions d’éligibilité requises pour bénéficier de ce service.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "bénéficiaire-non-mobile") {
    return textStart + `

Nous tenons à vous informer que nous avons examiné attentivement la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Malheureusement, nous ne sommes pas en mesure de donner une suite favorable à cette demande pour le moment.

Après avoir pris en compte divers éléments, nous avons constaté que ${data.beneficiaryFirstName} ${data.beneficiaryLastName} ne remplit pas les critères requis pour bénéficier de ce service pour des raisons de mobilité.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "bénéficiaire-non-intéressé") {
    return textStart + `

Nous tenons à vous informer que nous avons examiné attentivement la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Malheureusement, nous ne sommes pas en mesure de donner une suite favorable à cette demande pour le moment.

Nous avons constaté que ${data.beneficiaryFirstName} ${data.beneficiaryLastName} ne manifeste pas d’intérêt particulier ou de motivation suffisante pour bénéficier de ce service.

Nous vous encourageons à discuter davantage avec ${data.beneficiaryFirstName} ${data.beneficiaryLastName} afin de comprendre ses besoins et ses aspirations, et d’explorer d’autres alternatives qui pourraient mieux correspondre à ses attentes.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "freins-périphériques") {
    return textStart + `

Nous tenons à vous informer que nous avons examiné attentivement la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Malheureusement, nous ne sommes pas en mesure de donner une suite favorable à cette demande pour le moment.

Nous avons constaté que ${data.beneficiaryFirstName} ${data.beneficiaryLastName} fait face à des freins périphériques qui l’empêchent actuellement de poursuivre ce service. Ces freins rendent difficile la participation et l’engagement nécessaires.

Nous vous encourageons à explorer d’autres options qui pourraient mieux correspondre à la situation actuelle de ${data.beneficiaryFirstName} ${data.beneficiaryLastName}. Il existe peut-être d’autres programmes ou ressources qui sont mieux équipés pour relever les défis spécifiques auxquels ${data.beneficiaryFirstName} ${data.beneficiaryLastName} est confronté.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "session-complète") {
    return textStart + `

Nous tenons à vous informer que nous avons examiné attentivement la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Malheureusement, nous ne sommes pas en mesure de donner une suite favorable à cette demande pour le moment.

En raison d’une forte demande et d’une capacité limitée, toutes les places disponibles pour cette session ont été entièrement attribuées. Malheureusement, nous ne sommes plus en mesure d’accueillir de nouvelles personnes à ce stade.

Nous vous encourageons néanmoins à rester à l’écoute de nos prochaines sessions ou à explorer d’autres programmes similaires qui pourraient répondre aux besoins de ${data.beneficiaryFirstName} ${data.beneficiaryLastName}.

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;

  } else if (reasons[0] === "orientation-en-doublon") {
    return textStart + `

Nous vous remercions d’avoir soumis une nouvelle demande pour ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ».

Cependant, après avoir examiné attentivement les informations fournies, nous constatons qu’une orientation pour ${data.beneficiaryFirstName} ${data.beneficiaryLastName} a déjà été reçue précédemment.

Nous tenons à vous assurer que nos équipes reviendront rapidement vers vous avec une réponse, si cela n’a pas déjà été fait. Il n’est donc pas nécessaire de soumettre une nouvelle demande à ce stade. Nous vous remercions de votre compréhension.

N’hésitez pas à nous contacter si vous avez des questions supplémentaires ou si vous souhaitez fournir des mises à jour pertinentes concernant la situation de ${data.beneficiaryFirstName} ${data.beneficiaryLastName}.

`+ textEnd;


  } else if (reasons[0] === "autre") {
    return textStart + `

Nous tenons à vous informer que nous avons examiné attentivement la demande concernant ${data.beneficiaryFirstName} ${data.beneficiaryLastName} pour le service « ${data.serviceName} ». Malheureusement, nous ne sommes pas en mesure de donner une suite favorable à cette demande pour le moment.

[MERCI DE RENSEIGNER VOS DETAILS ICI]

Si vous avez des questions supplémentaires, n’hésitez pas à nous contacter.

`+ textEnd;
  }

  return "";
}
