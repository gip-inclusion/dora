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
      strict: true,
    });
  } catch (err) {
    const errors = err.inner.reduce(
      (acc, e) => ({ ...acc, [e.path]: e.message }),
      {}
    );

    let doneOnce = false;
    Object.entries(errors).forEach(([fieldName, message]) => {
      const name = fieldName.split("[")[0];
      if (!doneOnce) {
        const elt = document.getElementsByName(name);
        elt?.[0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
        doneOnce = true;
      }
      formErrors.update((value) => {
        value[name] = message;
        return value;
      });

      console.log(name, data[name], typeof data[name], message);
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
