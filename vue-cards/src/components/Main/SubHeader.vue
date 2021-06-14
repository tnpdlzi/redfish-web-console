<template>
  <section class="items">
    <div class="header">
      <template v-for="tab in tabs">
        <template v-if="tab == 'Dashboard'" class="dashList">
          <router-link
          :key="tab"
          :to="`/dashboard`">
            <button class="itemButton">
              {{tab}}
            </button>
          </router-link>
        </template>
        <template v-else-if="tab == 'Server List'" class="dashList">
          <router-link
          :key="tab"
          :to="`/ServerList`">
            <button class="itemButton">
              {{tab}}
            </button>
          </router-link>
          <div :key="tab" class="ipButton">
          {{id}}
          </div>

        </template>
        <template v-else>
          <router-link
          :key="tab"
          :to="`/dashboard/${ id }/${tab}`">
            <button class="subButton">
              {{tab}}
            </button>
          </router-link>
        </template>
      </template>
    </div>
      <!-- <router-view ></router-view> -->
  </section>
</template>
<script>
// eslint-disable-next-line
/* eslint-disable */
import { mapGetters } from 'vuex'

export default {
  components: {
  },
  props: {
        id: String,
    },
    methods: {
      clickMenuBtn: function(event) {
        console.log(event.target.nextElementSibling.childElementCount)
        console.log(event.target.nextElementSibling.children)
        if(event.target.nextElementSibling.style.display === 'none' ) {
          event.target.nextElementSibling.style.display = 'block';
        } else {
          event.target.nextElementSibling.style.display = 'none';
        }
      }
    },
    computed: {
        ...mapGetters({
            tabs: 'tabs/getTabs'
        }),
    },

  data: () => ({
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

.subButton {
  height: 55px;
  width: 55px;

  margin: 10px;
  background: var(--button-bg-color);
    
  margin: 5px;
  /* padding: 0.5rem 1rem; */
  
  border: none;
  border-radius: 10px;
    
  display: inline-block;
  
  box-shadow: 3px 5px 5px 3px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  
  cursor: pointer;
}

.ipButton {
  height: auto;
  background: var(--button-bg-color);
  /* margin: 10px; */
  margin-top: 20px;
  padding: 20px;    
  width: auto;
  font-size: 20px;
}
</style>
