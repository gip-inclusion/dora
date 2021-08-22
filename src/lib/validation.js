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
  if (shape.nullable && value == null) {
    return { value, valid: true };
  }
  if (shape.pre) {
    for (const prerun of shape.pre) {
      value = prerun(value);
    }
  }
  if (shape.required && (value == null || value === "" || value === [])) {
    addError(fieldname, "Ce champ est requis");
    return { originalValue, valid: false };
  }
  for (const rule of shape.rules) {
    const result = rule(`${fieldname}`, value, data);

    if (!result.valid) {
      console.log(fieldname, value, typeof value, result);
      addError(fieldname, result.msg);
      return { originalValue, valid: false };
    }
  }
  return { value, valid: true };
}

export function validate(data, schema, fullSchema, skipDeps = true) {
  const validatedData = {};
  let isValid = true;
  let doneOnce = false;

  Object.keys(schema).forEach((fieldname) => delete currentErrors[fieldname]);
  formErrors.set(currentErrors);

  Object.entries(schema).forEach(([fieldname, shape]) => {
    // console.log("value", data[fieldname]);
    const { value, valid } = validateField(fieldname, shape, data);
    isValid &&= valid;
    validatedData[fieldname] = value;
    if (!doneOnce && !valid) {
      const elt = document.getElementsByName(fieldname);
      elt?.[0]?.scrollIntoView({ behavior: "smooth", block: "start" });
      doneOnce = true;
    }
    if (!skipDeps) {
      shape.dependents?.forEach((depName) => {
        const { depValue, depValid } = validateField(
          depName,
          fullSchema[depName],
          data
        );
        isValid &&= depValid;
        validatedData[depName] = depValue;
        if (!doneOnce && !depValid) {
          const elt = document.getElementsByName(depName);
          elt?.[0]?.scrollIntoView({ behavior: "smooth", block: "start" });
          doneOnce = true;
        }
      });
    }
  });
  return { validatedData, valid: isValid };
  // try {
  //   validatedData = schema.validateSync(data, {
  //     abortEarly: false,
  //     strict: true,
  //   });
  // } catch (err) {
  //   const errors = err.inner.reduce(
  //     (acc, e) => ({ ...acc, [e.path]: e.message }),
  //     {}
  //   );

  //   let doneOnce = false;
  //   Object.entries(errors).forEach(([fieldName, message]) => {
  //     const name = fieldName.split("[")[0];
  //     if (!doneOnce) {
  //       const elt = document.getElementsByName(name);
  //       elt?.[0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  //       doneOnce = true;
  //     }
  //     formErrors.update((value) => {
  //       value[name] = message;
  //       return value;
  //     });

  //     console.log(name, data[name], typeof data[name], message);
  //   });

  //   console.log("Validation errors", errors);
  //   return false;
  // }
  return data;
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
