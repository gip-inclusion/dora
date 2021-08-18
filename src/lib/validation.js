import { writable } from "svelte/store";
export const contextValidationKey = {};
export const formErrors = writable({});

let currentErrors;
formErrors.subscribe((value) => {
  currentErrors = value;
});

export function validate(data, schema) {
  let validatedData;

  Object.keys(schema.fields).forEach((key) => delete currentErrors[key]);
  formErrors.set(currentErrors);

  try {
    validatedData = schema.validateSync(data, {
      abortEarly: false,
      strict: false,
    });
  } catch (err) {
    const errors = err.inner.reduce(
      (acc, e) => ({ ...acc, [e.path]: e.message }),
      {}
    );

    Object.entries(errors).forEach(([fieldName, message]) => {
      formErrors.update((value) => {
        value[fieldName] = message;
        return value;
      });
    });
    console.log("Validation errors", errors);
    return false;
  }
  return validatedData;
}

export function injectAPIErrors(errors, serverErrors) {
  Object.entries(errors).forEach(([key, values]) => {
    const fieldName = key;
    values.forEach((value) => {
      const errorCode = value.code;
      const errorMessage =
        (serverErrors[fieldName] && serverErrors[fieldName][errorCode]) ||
        (serverErrors._default && serverErrors._default[errorCode]) ||
        value.message;
      // TODO append instead of overwrite; there might be more than one error
      // by field
      formErrors.update((errValue) => {
        errValue[fieldName] = errorMessage;
        return errValue;
      });
    });
  });
}
