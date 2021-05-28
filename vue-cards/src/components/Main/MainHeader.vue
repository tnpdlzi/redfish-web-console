<template>
  <section class="items">
    <div class="header">
      <router-link v-for="item in items"
      :key="item.title"
      link
      :to="item.to">
        <button class="itemButton">
          {{item.title}}
        </button>
      </router-link>
    </div>
      <!-- <router-view ></router-view> -->
  </section>
</template>
<script>
// eslint-disable-next-line
/* eslint-disable */

export default {
  components: {
  },

  data: () => ({
    // items에 표시될 메뉴 리스트
    items : [
      { title: 'Dashboard', to: '/dashboard' },
      { title: 'Server List', to: '/ServerList' },
    ]
  }),
};
</script>

<style>
.header {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: start;
  background-color: #fff;
  margin: 3px; padding: 3px;
}

.itemButton {
  height: 85px;
  margin: 10px;
  background: var(--button-bg-color);
    
  margin: 5px;
  /* padding: 0.5rem 1rem; */
  
  border: none;
  border-radius: 10px;
    
  display: inline-block;
  width: 85px;
  
  box-shadow: 3px 5px 5px 3px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  
  cursor: pointer;
}
</style>
