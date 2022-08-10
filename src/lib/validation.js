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

function validateField(fieldname, shape, data, extraData) {
  const originalValue = data[fieldname];

  let value = originalValue;
  if (!shape.required && value == null) {
    // Ignore null values for fields that are not required
    return { value, valid: true };
  }

  if (shape.pre && value) {
    for (const preprocess of shape.pre) {
      value = preprocess(value);
    }
  }

  if (
    shape.required &&
    ((Array.isArray(value) && !value.length) ||
      (!Array.isArray(value) && (value == null || value === "")))
  ) {
    return { originalValue, valid: false, msg: "Information requise" };
  }

  for (const rule of shape.rules) {
    const result = rule(`${fieldname}`, value, data, extraData);

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

function scrollToField(fieldname) {
  const elt = document.getElementsByName(fieldname);
  elt?.[0]?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function validate(
  data,
  schema,
  { noScroll = false, fullSchema, showErrors = true, extraData } = {}
) {
  let validatedData = {};
  let isValid = true;
  let doneOnce = false;
  const errorFields = [];

  if (showErrors) {
    Object.keys(schema).forEach((fieldname) => delete currentErrors[fieldname]);
    formErrors.set(currentErrors);
  }

  Object.entries(schema).forEach(([fieldname, shape]) => {
    const { value, valid, msg } = validateField(
      fieldname,
      shape,
      data,
      extraData
    );

    isValid &&= valid;
    validatedData[fieldname] = value;

    if (!valid) {
      errorFields.push(shape.name);
    }

    if (showErrors) {
      clearError(fieldname);

      if (!valid) {
        addError(fieldname, msg);
      }

      if (!noScroll && !doneOnce && !valid) {
        scrollToField(fieldname);
        doneOnce = true;
      }
    }

    // Vérification des dépendances
    if (shape.dependents?.length && fullSchema) {
      shape.dependents.forEach((depName) => {
        const {
          value: depValue,
          valid: depValid,
          msg: depMsg,
        } = validateField(depName, fullSchema[depName], data, extraData);

        isValid &&= depValid;
        validatedData[depName] = depValue;
        if (!depValid) {
          errorFields.push(fullSchema[depName].name);
        }

        if (showErrors) {
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
