<script lang="ts">
  interface Props {
    label: string;
    icon: string;
  }

  let { label, icon }: Props = $props();
</script>

<div class="gap-s16 flex items-center">
  <div class="bg-blue-light p-s12 inline-block rounded-3xl">
    <div class="h-s24 w-s24 text-france-blue fill-current">
      {@html icon}
    </div>
  </div>
  <div class="text-f18 text-france-blue font-bold">
    {label}
  </div>
</div>
