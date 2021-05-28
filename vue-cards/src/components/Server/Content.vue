<template>
  <div class="content">
    <div>
      <h2>{{message}}</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "Content",
  props: {
    message: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
