import { browser } from "$app/environment";
import type { ServicesOptions } from "$lib/types";
import type { Schema, Shape } from "$lib/validation/schema-utils";
import { tick } from "svelte";
import { writable } from "svelte/store";

export type ValidationContext = {
  onBlur: (evt: any) => Promise<void>;
  onChange: (evt: any) => Promise<void>;
};
export const contextValidationKey = {};

export const formErrors: any = writable({});

let currentErrors;
formErrors.subscribe((value) => {
  currentErrors = value;
});

export const currentSchema = writable<Schema | undefined>();
export const currentFormData = writable<object | undefined>();

function addError(fieldName, msg) {
  formErrors.update((previousErrors) => {
    previousErrors[fieldName] = previousErrors[fieldName]?.length
      ? [...previousErrors[fieldName], msg]
      : [msg];
    return previousErrors;
  });
}

function clearError(fieldName) {
  formErrors.update((previousErrors) => {
    delete previousErrors[fieldName];
    return previousErrors;
  });
}

export function isRequired<T>(shape: Shape<T>, data: any) {
  if (shape.required == null) {
    return false;
  }
  if (typeof shape.required === "boolean") {
    return shape.required;
  }
  return shape.required(data);
}

function validateField(
  fieldName: string,
  shape: Shape<any>,
  data,
  servicesOptions: ServicesOptions | undefined,
  schema,
  checkRequired = true
) {
  const originalValue = data[fieldName];

  let value = originalValue;
  if ((!checkRequired || !isRequired(shape, data)) && value == null) {
    // Ignore null values for fields that are not required
    return { value, valid: true };
  }

  if (shape.pre && value) {
    for (const preprocess of shape.pre) {
      value = preprocess(value);
    }
  }

  if (
    checkRequired &&
    isRequired(shape, data) &&
    ((Array.isArray(value) && !value.length) ||
      (!Array.isArray(value) && (value == null || value === "")))
  ) {
    return { originalValue, valid: false, msg: "Information requise" };
  }

  for (const rule of shape.rules) {
    const result = rule(`${fieldName}`, value, data, servicesOptions, schema);

    if (!result.valid) {
      return { originalValue, valid: false, msg: result.msg };
    }
  }

  if (shape.post) {
    for (const postprocess of shape.post) {
      value = postprocess(value);
    }
  }

  return { value, valid: true };
}

async function scrollToField(fieldName) {
  await tick();
  if (browser) {
    const elt = document.getElementById(fieldName);
    elt?.scrollIntoView({ behavior: "smooth", block: "start" });
    if (!elt) {
      console.error("Impossible de scroller sur ", fieldName);
    }
  }
}

export function validate(
  data,
  schema,
  {
    noScroll = false,
    // lors de la saisie du formulaire, la validation est faite champ par champ
    // mais dans certains cas on veut pouvoir valider un champ dépendant du premier
    // en même temps. Pour cela on peut donc passer ici le schema complet du formulaire.
    fullFormSchema = undefined,
    showErrors = true,
    servicesOptions = undefined,
    checkRequired = true,
  }: {
    noScroll?: boolean;
    fullFormSchema?: any;
    showErrors?: boolean;
    servicesOptions?: ServicesOptions;
    checkRequired?: boolean;
  } = {}
) {
  let validatedData = {};
  let isValid = true;
  let doneOnce = false;
  const errorFields: string[] = [];

  if (showErrors) {
    Object.keys(schema).forEach((fieldName) => delete currentErrors[fieldName]);
    formErrors.set(currentErrors);
  }

  Object.entries(schema).forEach(([fieldName, shape]: [string, Shape<any>]) => {
    const { value, valid, msg } = validateField(
      fieldName,
      shape,
      data,
      servicesOptions,
      schema,
      checkRequired
    );

    isValid = isValid && valid;
    validatedData[fieldName] = value;

    if (!valid) {
      errorFields.push(shape.label);
    }

    if (showErrors) {
      clearError(fieldName);

      if (!valid) {
        addError(fieldName, msg);
      }

      if (!noScroll && !doneOnce && !valid) {
        scrollToField(fieldName);
        doneOnce = true;
      }
    }

    // Vérification des dépendances
    if (shape.dependents?.length && fullFormSchema) {
      shape.dependents.forEach((depName) => {
        const {
          value: depValue,
          valid: depValid,
          msg: depMsg,
        } = validateField(
          depName,
          fullFormSchema[depName],
          data,
          servicesOptions,
          schema,
          checkRequired
        );

        isValid = isValid && depValid;
        validatedData[depName] = depValue;
        if (!depValid) {
          errorFields.push(fullFormSchema[depName].name);
        }

        if (showErrors) {
          clearError(depName);
          if (!depValid) {
            clearError(depName);
            addError(depName, depMsg);
          }
          if (!noScroll && !doneOnce && !depValid) {
            scrollToField(depName);
            doneOnce = true;
          }
        }
      });
    }
  });

  // Ensure we pass the fields that are not in the validation schema untouched
  // Those are mostly the hidden fields
  validatedData = { ...data, ...validatedData };

  return { validatedData, valid: isValid, errorFields };
}

function parseServerError(error) {
  // https://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
  // We need to differenciate ValidationErrors from the rest of them
  if (error.detail) {
    // Other error
    return { nonFieldErrors: [{ ...error.detail }] };
  }
  // Validation error
  return error;
}

export function injectAPIErrors(err, serverErrorsTranslation) {
  let doneOnce = false;
  const parsedErrors = parseServerError(err);

  Object.entries(parsedErrors).forEach(
    ([key, errors]: [string, { code: string; message: string }[]]) => {
      const fieldName = key;
      errors.forEach((value) => {
        const errorCode = value.code;
        const errorMsg =
          (serverErrorsTranslation[fieldName] &&
            serverErrorsTranslation[fieldName][errorCode]) ||
          (serverErrorsTranslation._default &&
            serverErrorsTranslation._default[errorCode]) ||
          value.message;

        addError(fieldName, errorMsg);

        if (!doneOnce) {
          scrollToField(fieldName);
          doneOnce = true;
        }
      });
    }
  );
}
