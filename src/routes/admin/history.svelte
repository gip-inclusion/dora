<script lang="ts">
  import DateLabel from "$lib/components/utilities/date-label.svelte";

  export let notes;
</script>

<div class="max-h-s160 overflow-scroll">
  {#each notes as note}
    <div class="bg-gray-01">
      <DateLabel date={note.date} /> par {note.user.email}
    </div>
    <div class="ml-s32">
      {#each note.message.split("\n") as msg}
        {msg}<br />
      {/each}
    </div>
  {/each}
</div>
