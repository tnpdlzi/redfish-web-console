<template>
  <div class="mmodal">
    <div class="moverlay" @click="[$emit('close-modal'), location.reload()]"></div>
    <div class="mmodal-card">
      <slot />
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
/* Modal */
.modal,
.moverlay {
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
}
.moverlay {
  opacity: 0.5;
  background-color: black;
}
.mmodal-card {
  position: relative;
  max-width: 1000px;
  margin: auto;
  margin-top: 30px;
  padding: 20px;
  background-color: white;
  min-height: 200px;
  z-index: 10;
  opacity: 1;
  text-align: center;
}
</style>