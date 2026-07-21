<script lang="ts">
  import Button from "$lib/components/display/button.svelte";

  interface Props {
    current: number;
    totalPages: number;
    onPageChange: (activePage: number) => void;
  }

  let { current, totalPages, onPageChange }: Props = $props();

  function makePageRange(start: number, end: number): number[] {
    return Array.from(
      Array(end - start + 1)
        .keys()
        .map((i) => i + start)
    );
  }
  function pageRanges(): [number[], number[], number[]] {
    if (totalPages <= 10) {
      return [makePageRange(1, totalPages), [], []];
    }

    // Combien de page afficher avant et après la page active.
    const pageWindow = 4;
    let skipMiddle = false;

    let startLimit = 1 + pageWindow;
    if (current < startLimit) {
      skipMiddle = true;
    } else {
      startLimit = 1;
    }
    const start = makePageRange(1, startLimit);

    let endLimit = totalPages - pageWindow;
    if (current > endLimit) {
      skipMiddle = true;
    } else {
      endLimit = totalPages;
    }
    const end = makePageRange(endLimit, totalPages);

    const middle = skipMiddle ? [] : makePageRange(current - 1, current + 1);

    return [start, middle, end];
  }

  const [startPages, middlePages, endPages] = $derived.by(pageRanges);
</script>

{#if current && totalPages > 1}
  <div class="py-s32 flex justify-center">
    <span id="pages-label" class="sr-only">Pages :</span>
    <nav aria-labelledby="pages-label">
      {#snippet page(i: number)}
        <li class="inline">
          <Button
            type="button"
            secondary={i !== current}
            ariaAttributes={{
              "aria-label": `Aller à la page ${i}`,
              "aria-current": i === current ? "page" : undefined,
              "aria-disabled": i === current ? "true" : undefined,
            }}
            extraClass="m-s2"
            disabled={i === current}
            onclick={i === current ? undefined : () => onPageChange(i)}
            label={i.toString()}
          />
        </li>
      {/snippet}

      <ol class="inline">
        {#each startPages as p}
          {@render page(p)}
        {/each}
        {#if middlePages.length}
          <li class="inline"><span>…</span></li>
        {/if}
        {#each middlePages as p}
          {@render page(p)}
        {/each}
        {#if endPages.length}
          <li class="inline"><span>…</span></li>
        {/if}
        {#each endPages as p}
          {@render page(p)}
        {/each}
      </ol>
    </nav>
  </div>
{/if}
