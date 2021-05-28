<template>
  <div class="product">
    <SubHeader :id="id"/>
    <table id="detail-table">
      <div class="table-outline">


      <br>

      <h2>상세 정보</h2>
      <div>

        <br>
            <h3>logStatus</h3>
        <br>

        <ul v-for="(service, index) in logStatus" :key="index">
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

        <br>
            <h3>logList</h3>
            <h4>로그는 최근으로부터 10개만 출력됩니다.</h4>
        <br>

        <ul v-for="(service, index) in logList" :key="index">
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
import SubHeader from '@/components/Main/SubHeader'

  export default {
  components: { SubHeader },
    props: {
      id: Number
    },
    data() {
      return {
        logStatus: null,
        logList: null,
      }
    },
    mounted() {
    this.id = this.$route.params.id 
  },
  
    created () {
      axios.get('http://localhost:8000/api/logs?ip=' + this.$route.params.id)
      .then(response => {
        console.log(response);
        this.logStatus = response.data.logStatus;
        this.logList = response.data.logList;
      })
      .catch(err => {
        console.log(err);
      });
    }
  }
</script>