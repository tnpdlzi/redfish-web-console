<template>
  <div class="product">
    <SubHeader :id="id"/>

    <table id="detail-table">
      <div class="table-outline">


      <br>

      <h2>상세 정보</h2>
      <div>
        <ul v-for="(service, index) in item" :key="index">
          <div v-for="(value, key) in service" :key="key" style="display: flex">

            <tbody>
              <tr>
                  <th v-if="key != 'Attributes'">{{key}}</th>
                  <td v-if="key != 'Attributes'">{{value}}</td>
              </tr>
            </tbody>
            

            <div v-if="key == 'Attributes'">
              <div v-for="(value, key) in value" :key="key">

                <div v-if="value == null"></div>
                <div v-else >
                  <tbody>
                    <tr>
                        <th >{{key}}</th>
                        <td >{{value}}</td>
                    </tr>
                  </tbody>
                </div>

                
              </div>
            </div>
          </div>
          <br>
        </ul>
        

      </div>

      <br>

      </div>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import SubHeader from '@/components/Main/SubHeader'

  export default {
  components: { SubHeader },
    props: {
      id: Number
    },
    data() {
      return {
        item: null,
      }
    },
    mounted() {
    this.id = this.$route.params.id 
  },
    
    created () {
      axios.get('/api/bios?ip=' + this.$route.params.id)
      .then(response => {
        console.log(response);
        this.item = response.data;
      })
      .catch(err => {
        console.log(err);
      });
    }
  }
</script>