export type OrientationType = "sent" | "received";

class OrientationState {
  selectedType = $state<OrientationType>("received");

  setSelectedType = (type: string) => {
    this.selectedType = type as OrientationType;
  };
}

export const items = [
  { id: "received", name: "Orientations reçues" },
  { id: "sent", name: "Orientations envoyées" },
] as const;

export const orientationState = new OrientationState();
