type OrientationType = "sent" | "received";

class OrientationState {
  selectedType = $state<OrientationType>("received");

  setSelectedType = (type: string) => {
    this.selectedType = type as OrientationType;
  };
}

export const orientationState = new OrientationState();
