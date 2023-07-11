<script lang="ts">
  export let label: string;
  export let icon: string;
</script>

<div class="flex items-center gap-s16">
  <div class="inline-block rounded-xl bg-blue-light p-s12">
    <div class="h-s24 w-s24 fill-current text-france-blue">
      {@html icon}
    </div>
  </div>
  <div class="text-f18 font-bold text-france-blue">
    {label}
  </div>
</div>
