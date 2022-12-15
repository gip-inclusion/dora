export function clickOutside(node: HTMLElement) {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore erreurs de typage inextricables...
  const handleClick = (event) => {
    if (node && !node.contains(event.target) && !event.defaultPrevented) {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore erreurs de typage inextricables...
      node.dispatchEvent(new CustomEvent("click_outside", node));
    }
  };

  document.addEventListener("click", handleClick, true);

  return {
    destroy() {
      document.removeEventListener("click", handleClick, true);
    },
  };
}
