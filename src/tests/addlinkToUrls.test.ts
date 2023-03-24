import { addlinkToUrls } from "$lib/utils/misc";
import { describe, expect, test } from "vitest";

describe("addlinkToUrls", () => {
  test("ajout des liens - http", () => {
    const url = `http://perdu.com`;
    expect(addlinkToUrls(url)).toBe(
      '<a href="http://perdu.com" class="underline" target="_blank" rel="noopener ugc">http://perdu.com</a>'
    );
  });

  test("ajout des liens - https", () => {
    const url = `https://perdu.com`;
    expect(addlinkToUrls(url)).toBe(
      '<a href="https://perdu.com" class="underline" target="_blank" rel="noopener ugc">https://perdu.com</a>'
    );
  });

  test("ajout des liens - mailto", () => {
    const url = `mailto://mail@example.com`;
    const result = addlinkToUrls(url);
    expect(result).toBe(
      '<a href="mailto://mail@example.com" class="underline" target="_blank" rel="noopener ugc">mailto://mail@example.com</a>'
    );
  });
});
