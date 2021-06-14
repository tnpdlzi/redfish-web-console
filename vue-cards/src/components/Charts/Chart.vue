<template>
<div class="product">
  <SubHeader :id="id"/> 
    <div>
        <iframe :src= "`http://${localIp}:3000/d/${item[0]['grafanaUid']}?theme=light`" width="100%" height="700px" frameborder="0"></iframe>        
    </div>
    <a :href="`http://${localIp}:3000/d/${item[0]['grafanaUid']}`">Grafana에서 보기</a>
    <div>
      임계치 설정
      <EditAlert />
    </div>
    <div>
      이메일 추가
      <AddEmail />
    </div>
    
</div>
</template>

<script>
import SubHeader from '@/components/Main/SubHeader'
import EditAlert from '@/components/Server/EditAlert'
import AddEmail from '@/components/Server/AddEmail'
import axios from 'axios';

  export default {
  components: { SubHeader, EditAlert, AddEmail },
    props: {
      id: String
    },
    data() {
      return {
        item: null,
        localIp: null
      }
    },
    mounted() {
    this.id = this.$route.params.id 
  },
 
  created () {
      axios.get('/api/Charts?ip=' + this.$route.params.id)
      .then(response => {
        console.log(response.data);
        this.item = response.data;
      })
      .catch(err => {
        console.log(err);
      });

      axios.get('/api/localip')
      .then(response => {
        console.log(response.data);
        this.localIp = response.data.ip;
      })
      .catch(err => {
        console.log(err);
      });
    }
    
  }
</script>
