<template>
  <div>
    <p>
      {{ count }}
    </p>
    <div v-bind:seen="true" v-show="!seen">
      <button v-on:click="count += 1">+1</button>
      <button v-on:click="count -= 1">-1</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    count: {
      type: Number,
      default: 0,
    },
    seen: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
<style>
</style>

