import type { Model, Service, ServicesOptions } from "$lib/types";

export interface FieldGroupProps {
  servicesOptions: ServicesOptions;
  service: Service;
  model?: Model;
}

export interface FieldSetProps extends FieldGroupProps {
  noTopPadding?: boolean;
}
