import button from "./button.svelte";
import { menuIcon } from "../icons";

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
// More on argTypes: https://storybook.js.org/docs/svelte/api/argtypes
export default {
  /* 👇 The title prop is optional.
   * See https://storybook.js.org/docs/svelte/configure/overview#configure-story-loading
   * to learn how to generate automatic titles
   */
  title: "Elements/Button",
  component: button,
  argTypes: {
    label: { control: "text" },
    type: {
      control: { type: "select" },
      options: ["button", "submit"],
    },
    name: { control: "text" },
    icon: { control: "text" },
    iconOnRight: { control: "boolean" },
    disabled: { control: "boolean" },
    small: { control: "boolean" },
    secondary: { control: "boolean" },
    noBackground: { control: "boolean" },
    noPadding: { control: "boolean" },
    flashSuccess: { control: "boolean" },
    wFull: { control: "boolean" },
  },
};

// More on component templates: https://storybook.js.org/docs/svelte/writing-stories/introduction#using-args
const Template = (props) => ({
  Component: button,
  props,
  on: {
    click: props.onClick,
  },
});

// More on args: https://storybook.js.org/docs/svelte/writing-stories/args
export const Default = Template.bind({});
Default.args = {
  label: "Button label",
};

export const Icon = Template.bind({});
Icon.args = {
  label: "Button label",
  icon: menuIcon,
};
