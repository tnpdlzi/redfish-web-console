<template>
<div>
  <MainHeader class="product"/>
  <div id="Instance" class="ttmain">
  <!-- <button class="ttButton" @click="swipeLeft()"/> -->
  <div class="ttrows"  ref="content">
    <div class="ttwrapper">

        <section class="ttproducts">
          <div v-for="product in data" :key="product.result">
          <CardProduct
            v-if="product.color == 'Red'"
            :key="product.result"
            :products="product.result"
            :color="product.color"
            :part="product.part"
          />
          </div>
        </section>

        <section class="ttproducts">
          <div v-for="product in data" :key="product.result">

          <CardProduct
            v-if="product.color == 'Orange'"
            :key="product.result"
            :products="product.result"
            :color="product.color"
            :part="product.part"
          />
          </div>
        </section>

        <section class="ttproducts">
          <div v-for="product in data" :key="product.result">

          <CardProduct
            v-if="product.color == 'Blue'"
            :key="product.result"
            :products="product.result"
            :color="product.color"
            :part="product.part"
          />
          </div>
        </section>
      
    </div>
  </div>
    
  <!-- <button class="ttButton" @click="swipeRight()"/> -->
  </div>
</div>
</template>

<script>
import CardProduct from './CardProduct';
import axios from 'axios';
import MainHeader from '@/components/Main/MainHeader'

export default {
  components: {
    CardProduct,
    MainHeader
  },
  data () {
    return {
        data: null
    }
  },
  
  created () {
      axios.get('http://localhost:8000/api/CardList')
      .then(response => {
        console.log(response);
        this.data = response.data;
      })
      .catch(err => {
        console.log(err);
      });
    }
}


</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.ttmain {
  width: 100vw;
  min-height: 100vh;
  overflow: hidden;

  background-color: #eee;
  display: flex;
  /* justify-content: center;
  align-items: center; */
  padding: 25px;
}

.ttproducts {
  display: flex;
  max-width: 100%;
  margin: 0 auth;
  height: 100%;
}

.ttwrapper {
  height: 100%;
  border: 1px solid #ddd;
  display: table-cell;
  overflow: auto;
}

/* .ttwrapper::-webkit-scrollbar {
  width: 0;
} */

/* .ttButton {
  width: 50px;
  height: 50px;
  align-self: center;
  background: var(--button-bg-color);        
  border: none;
  --button-bg-color: #fff;
  --button-hover-bg-color: #fff;
  border-radius: 100px;
  box-shadow: 3px 5px 5px 3px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  cursor: pointer;
} */

.ttrows {
    display: table-cell; 
    vertical-align: bottom;
    overflow: auto;
}

</style>
