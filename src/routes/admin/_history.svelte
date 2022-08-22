<script>
  import Date from "$lib/components/date.svelte";

  export let notes;
</script>

<div class="max-h-s160 overflow-scroll">
  {#each notes as note}
    <div class="bg-gray-01">
      <Date date={note.date} /> par {note.user.email}
    </div>
    <div class="ml-s32">
      {#each note.message.split("\n") as msg}
        {msg}<br />
      {/each}
    </div>
  {/each}
</div>
