<template>
  <div class="ttproduct">
    <div :class="`ttproduct-inner${color}`"> 
      <div class="ttproduct-image-wrap">
          <!-- <div> -->
            <!-- <img :src="images[0].image" class="ttimage"/> -->
            <router-link :to="`dashboard/${products[0].ip}/details`" class="ttimage"></router-link>
          <!-- </div> -->
      </div>

      <div class="ttproduct-detail">
        <div v-for="product in products" :key="product.ip" >   
          <h2 v-if="product.ip != null">{{ product.ip }}</h2>
          <div class="ttdetails">
            <div v-if="product.tempThreshold != null || product.powerThreshold != null " class="threshold">            
              온도 임계치 : {{product.tempThreshold}} | 파워 임계치 : {{product.powerThreshold}}
            </div>

            <div v-if="part == null">
              <div v-if="product.Name != null" class="dName">
                {{product.Name}}
              </div>
            </div>

            <div v-if="part == null">
              <div v-if="product.ReadingCelsius != null">
                {{product.ReadingCelsius}}℃
              </div>
            </div>
            <div v-if="part == 'Both' || part == 'Temp'" class="partFont">
              <div v-if="product.ReadingCelsius != null">
                {{product.ReadingCelsius}}℃
              </div>
            </div>

            <div v-if="part == null">            
              <div v-if="product.PowerConsumedWatts != null">
                {{product.PowerConsumedWatts}} Watts
              </div>
            </div>
            <div v-if="part == 'Both' || part == 'Power'" class="partFont">            
              <div v-if="product.PowerConsumedWatts != null">
                {{product.PowerConsumedWatts}} Watts
              </div>
            </div>

          </div>
        </div>
       </div>
    </div>
  </div>

</template>

<script>
export default {
  name: 'products',
  props: ['products', 'color', 'part'],
  data() {
    return {
      images: [
        {
          id: 'on',
          image: require('../../assets/on.png')
        },
        {
          id: 'off',
          image: require('../../assets/off.png')
        },
      ],
      
    }
    
  },
}
</script>

<style>
  .ttproduct {
    flex: 1 1 33.333%;
    width: 100%;
    height: 100%;
    padding: 15px;
  }

  .ttproduct-innerBlue {
    position: relative;
    width: 200px;
    height: 250px;
    border-radius: 20px;
    padding-inline: 25px;
     /* x, y, z 축 값이다. 오른쪽은 색 값. */
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.35);
    background-color: #4B96E7;
  }

  .ttproduct-innerRed {
    position: relative;
    width: 200px;
    height: 250px;
    border-radius: 20px;
    padding-inline: 25px;
     /* x, y, z 축 값이다. 오른쪽은 색 값. */
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.35);
    background-color: red;
  }

  .ttproduct-innerOrange {
    position: relative;
    width: 200px;
    height: 250px;
    border-radius: 20px;
    padding-inline: 25px;
     /* x, y, z 축 값이다. 오른쪽은 색 값. */
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.35);
    background-color: orange;
  }

  .ttproduct-innerYellow {
    position: relative;
    width: 200px;
    height: 250px;
    border-radius: 20px;
    padding-inline: 25px;
     /* x, y, z 축 값이다. 오른쪽은 색 값. */
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.35);
    background-color: yellow;
  }

  /* .ttproduct-text-wrap {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 0;
    overflow: hidden;
  } */

  /* .ttproduct-text-wrap h2 {
    color: #313131;
    margin: 65px 16px 0px;
    font-size: 15px;
    font-weight: 900;
    opacity: 0.2; 
    transform-origin: center; 
  } */

  .ttproduct-image-wrap {
    position: relative;
    /* z-index: 1;  */
    /* transform-origin: center; */
    /* display:grid; */
  }

  .ttproduct-image-wrap .ttimage {
    width: 200px;
    height: 38px;
    margin: 0px -25px 0px;
    /* filter: drop-shadow(0px 0px 12px rgb(255, 255, 255, 0.25)); */
    /* float: right; */
    /* background-color: chartreuse; */
  }

  .ttproduct-detail {
    vertical-align: bottom;
    background-color: #FFF;
    border-radius: 20px;
    padding: 15px;
    height: 85%;
    margin: 0px -25px -25px; /* 이렇게 줌으로 해서 위쪽을 제외한 부분을 흰색으로 채워 카드 효과를 연출했다. */
  }

  /* 글씨 색과 마진 변경 */
  .ttproduct-detail h2 {
    font-size: 14px;
    font-weight: 700;
    color: #000;
    margin-bottom: 0px;
  }

  /* 안 쪽 설명에 대한 설정 */
  .ttproduct-detail h3 {
    font-size: 10px;
    line-height: 1.5; /* 줄 간격 조정 */
    /* font-weight: 500; */
    color: #000;
  }

  .ttdetails {
      font-size: 20px;
      padding-bottom: 10px;
      font-weight: 700;

  }
  .dName {
      font-size: 12px;
  }
  .threshold {
      font-size: 5px;
  }
  .partFont {
      font-size: 30px;
      color: Red;
  }

</style>
