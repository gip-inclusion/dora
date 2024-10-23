import { fireEvent, render, screen } from "@testing-library/svelte";
import { beforeAll, describe, expect, test } from "vitest";

import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
import { currentSchema } from "$lib/validation/validation";
import { serviceSchema } from "$lib/validation/schemas/service";

describe("BasicInputField", () => {
  beforeAll(() => {
    currentSchema.set(serviceSchema);
  });

  describe('when type="number"', () => {
    test('should render <input type="number" .../> with numeric value', () => {
      // given

      // when
      render(BasicInputField, {
        props: {
          type: "number",
          id: "spendingTimeTotalHours",
          description:
            "Nombre total d'heures investies par le bénéficiaire, ex : 18",
          value: 18,
        },
      });

      // then
      const input = screen.getByRole("spinbutton");
      expect(input).toBeInTheDocument();
      expect(input).toHaveValue(18);
    });

    test("should accept and set component value to user’s one when it is a valid number", async () => {
      // given
      render(BasicInputField, {
        props: {
          type: "number",
          id: "spendingTimeTotalHours",
          value: 18,
        },
      });
      const input = screen.getByRole("spinbutton");

      // when
      await fireEvent.input(input, { target: { value: "27" } });

      // then
      expect(input).toHaveValue(27);
    });

    test("should refuse and not set component value to user’s one when it is not a valid number", async () => {
      // given
      render(BasicInputField, {
        props: {
          type: "number",
          id: "spendingTimeTotalHours",
          value: 18,
        },
      });
      const input = screen.getByRole("spinbutton");

      // when
      await fireEvent.input(input, { target: { value: "not a number" } });

      // then
      expect(input).toHaveValue(null);
    });
  });
});
