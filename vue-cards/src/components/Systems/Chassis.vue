<template>
  <div class="product">
    <table id="detail-table">
      <div class="table-outline">
      <br>
      <div>
        <ul v-for="(service, index) in item" :key="index">
          <div v-for="(value, key) in service" :key="key">
            <div v-if="value == null"></div>
            <div v-else >
              <tbody>
                <tr>
                    <th>{{key}}</th>
                    <td>{{value}}</td>
                </tr>
              </tbody>
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

  export default {
  components: { },
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
      axios.get('/api/chassis?ip=' + this.$route.params.id)
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

<style>

</style>
