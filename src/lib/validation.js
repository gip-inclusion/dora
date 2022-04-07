import { writable } from "svelte/store";
export const contextValidationKey = {};
export const formErrors = writable({});

let currentErrors;
formErrors.subscribe((value) => {
  currentErrors = value;
});

function addError(fieldname, msg) {
  formErrors.update((previousErrors) => {
    previousErrors[fieldname] = previousErrors[fieldname]?.length
      ? [...previousErrors[fieldname], msg]
      : [msg];
    return previousErrors;
  });
}

function clearError(fieldname) {
  formErrors.update((previousErrors) => {
    delete previousErrors[fieldname];
    return previousErrors;
  });
}

function validateField(fieldname, shape, data) {
  clearError(fieldname);
  const originalValue = data[fieldname];

  let value = originalValue;
  if (shape.nullable && !shape.required && value == null) {
    // Ignore null values for fields that are nullable and not required
    return { value, valid: true };
  }
  if (shape.pre) {
    for (const preprocess of shape.pre) {
      value = preprocess(value);
    }
  }
  if (
    shape.required &&
    (value == null || value === "" || value?.length === 0)
  ) {
    addError(fieldname, "Ce champ est requis");
    return { originalValue, valid: false };
  }
  for (const rule of shape.rules) {
    const result = rule(`${fieldname}`, value, data);

    if (!result.valid) {
      console.warn(fieldname, value, typeof value, result);
      addError(fieldname, result.msg);
      return { originalValue, valid: false };
    }
  }
  if (shape.post) {
    for (const postprocess of shape.post) {
      value = postprocess(value);
    }
  }
  return { value, valid: true };
}

function scrollToField(fieldname) {
  const elt = document.getElementsByName(fieldname);
  elt?.[0]?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function validate(
  data,
  schema,
  fullSchema,
  { noScroll, skipDependenciesCheck }
) {
  let validatedData = {};
  let isValid = true;
  let doneOnce = false;

  Object.keys(schema).forEach((fieldname) => delete currentErrors[fieldname]);
  formErrors.set(currentErrors);

  Object.entries(schema).forEach(([fieldname, shape]) => {
    const { value, valid } = validateField(fieldname, shape, data);

    isValid &&= valid;
    validatedData[fieldname] = value;

    if (!noScroll && !doneOnce && !valid) {
      scrollToField(fieldname);
      doneOnce = true;
    }

    if (!skipDependenciesCheck) {
      shape.dependents?.forEach((depName) => {
        const { depValue, depValid } = validateField(
          depName,
          fullSchema[depName],
          data
        );

        isValid &&= depValid;
        validatedData[depName] = depValue;
        if (!noScroll && !doneOnce && !depValid) {
          scrollToField(depName);
          doneOnce = true;
        }
      });
    }
  });

  // Ensure we pass the fields that are not in the validation schema untouched
  // Those are mostly the hidden fields
  validatedData = { ...data, ...validatedData };

  return { validatedData, valid: isValid };
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
  Object.entries(parsedErrors).forEach(([key, values]) => {
    const fieldname = key;
    values.forEach((value) => {
      const errorCode = value.code;
      const errorMsg =
        (serverErrorsTranslation[fieldname] &&
          serverErrorsTranslation[fieldname][errorCode]) ||
        (serverErrorsTranslation._default &&
          serverErrorsTranslation._default[errorCode]) ||
        value.message;
      addError(fieldname, errorMsg);
      if (!doneOnce) {
        scrollToField(fieldname);
        doneOnce = true;
      }
    });
  });
}
