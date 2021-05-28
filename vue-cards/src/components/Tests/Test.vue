<template>
<div>
  <MainHeader class="product"/>
  <div id="Instance" class="ttmain">
  <!-- <button class="ttButton" @click="swipeLeft()"/> -->
  <div class="ttrows"  ref="content">
    <div class="ttwrapper">

        <section class="ttproducts">
          <div v-for="product in data" :key="product.result">

          <TestProduct
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

          <TestProduct
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

          <TestProduct
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
import TestProduct from './TestProduct';
// import axios from 'axios';
import MainHeader from '@/components/Main/MainHeader'

export default {
  components: {
    TestProduct,
    MainHeader
  },
  data () {
    return {
        // data: null
        data: [
    {
        "result": [
            {
                "ip": "192.168.0.1",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "CPU1 Temp",
                "ReadingCelsius": 38
            },
            {
                "Name": "CPU2 Temp",
                "ReadingCelsius": 39
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 148
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.2",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.3",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "CPU1 Temp",
                "ReadingCelsius": 38
            },
            {
                "Name": "CPU2 Temp",
                "ReadingCelsius": 39
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 148
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.4",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.5",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "CPU1 Temp",
                "ReadingCelsius": 38
            },
            {
                "Name": "CPU2 Temp",
                "ReadingCelsius": 39
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 148
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.6",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.7",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "CPU1 Temp",
                "ReadingCelsius": 38
            },
            {
                "Name": "CPU2 Temp",
                "ReadingCelsius": 39
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 148
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.8",
                "tempThreshold": 60,
                "powerThreshold": 200
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Blue",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.9",
                "tempThreshold": 30,
                "powerThreshold": 220
            },
            {
                "Name": "CPU1 Temp",
                "ReadingCelsius": 38
            },
            {
                "Name": "CPU2 Temp",
                "ReadingCelsius": 39
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 148
            }
        ],
        "color": "Red",
        "part": "Temp"
    },
    {
        "result": [
            {
                "ip": "192.168.0.10",
                "tempThreshold": 35,
                "powerThreshold": 120
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Red",
        "part": "Both"
    },
    {
        "result": [
            {
                "ip": "192.168.0.12",
                "tempThreshold": 35,
                "powerThreshold": 120
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Red",
        "part": "Power"
    },
    {
        "result": [
            {
                "ip": "192.168.0.13",
                "tempThreshold": 35,
                "powerThreshold": 150
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 32
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 31
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Orange",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.14",
                "tempThreshold": 35,
                "powerThreshold": 150
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 33
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 34
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Orange",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.15",
                "tempThreshold": 65,
                "powerThreshold": 115
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 105
            }
        ],
        "color": "Orange",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.16",
                "tempThreshold": 65,
                "powerThreshold": 112
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 105
            }
        ],
        "color": "Orange",
        "part": null
    },
    {
        "result": [
            {
                "ip": "192.168.0.17",
                "tempThreshold": 45,
                "powerThreshold": 125
            },
            {
                "Name": "02-CPU 1",
                "ReadingCelsius": 40
            },
            {
                "Name": "03-CPU 2",
                "ReadingCelsius": 40
            },
            {
                "Name": "PowerControl",
                "PowerConsumedWatts": 120
            }
        ],
        "color": "Orange",
        "part": null
    },
]
    }
  },
  methods: {
    
    // scrollTo: function scrollTo(element, scrollPixels, duration) {
    //   const scrollPos = element.scrollLeft;
    //   // Condition to check if scrolling is required
    //   if ( !( (scrollPos === 0 || scrollPixels > 0) && (element.clientWidth + scrollPos === element.scrollWidth || scrollPixels < 0))) 
    //   {
    //     // Get the start timestamp
    //     const startTime =
    //       "now" in window.performance
    //         ? performance.now()
    //         : new Date().getTime();
        
    //     let scroll = function(timestamp) {
    //       //Calculate the timeelapsed
    //       const timeElapsed = timestamp - startTime;
    //       //Calculate progress 
    //       const progress = Math.min(timeElapsed / duration, 1);
    //       //Set the scrolleft
    //       element.scrollLeft = scrollPos + scrollPixels * progress;
    //       //Check if elapsed time is less then duration then call the requestAnimation, otherwise exit
    //       if (timeElapsed < duration) {
    //         //Request for animation
    //         window.requestAnimationFrame(scroll);
    //       } else {
    //         return;
    //       }
    //     }
    //     //Call requestAnimationFrame on scroll function first time
    //     window.requestAnimationFrame(scroll);
    //   }
    // },
    // swipeLeft: function swipeLeft() {
    //   const content = this.$refs.content;
    //   this.scrollTo(content, -350, 500);
    // },
    // swipeRight: function swipeRight() {
    //   const content = this.$refs.content;
    //   this.scrollTo(content, 350, 500);
    // }
  },

  // created () {
  //     axios.get('http://localhost:8000/api/CardList')
  //     .then(response => {
  //       console.log(response);
  //       this.data = response.data;
  //     })
  //     .catch(err => {
  //       console.log(err);
  //     });
  //   }
}


</script>

<style>

ttbody {
  font-family: 'montseratt', sans-serif;
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
  max-height: 120;
  border: 1px solid #ddd;
  display: table-cell;
  overflow: auto;
}

/* .ttwrapper::-webkit-scrollbar {
  width: 0;
} */

.ttButton {
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
}

.ttrows {
    display: table-cell; 
    vertical-align: bottom;
    overflow: auto;
}

</style>
