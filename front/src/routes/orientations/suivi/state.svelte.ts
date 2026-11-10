export type OrientationType = "sent" | "received";

class OrientationState {
  selectedType = $state<OrientationType>("received");

  setSelectedType = (type: OrientationType) => {
    this.selectedType = type;
  };
}

export const orientationState = new OrientationState();
