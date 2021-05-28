<template>
<div class="product">
  <SubHeader :id="id"/> 
    <div>
        <!-- <iframe :src= "`http://localhost:3000/d/${item[0]['grafanaUid']}/${item[0]['ip'].replace(/./g,'-')}?refresh=25s&viewPanel=2`" width="50%" height="550" frameborder="0"></iframe>
        <iframe :src= "`http://localhost:3000/d/${item[0]['grafanaUid']}/${item[0]['ip'].replace(/./g,'-')}?refresh=25s&viewPanel=3`" width="50%" height="550" frameborder="0"></iframe> -->
        <!-- <iframe :src= "`http://localhost:3000/d-solo/${item[0]['grafanaUid']}/${item[0]['ip'].replace(/./g,'-')}?refresh=25s&theme=light&panelId=2`" width="80%" height="550" frameborder="0"></iframe>
        <iframe :src= "`http://localhost:3000/d-solo/${item[0]['grafanaUid']}/${item[0]['ip'].replace(/./g,'-')}?refresh=25s&theme=light&panelId=3`" width="80%" height="550" frameborder="0"></iframe> -->
        <iframe :src= "`http://localhost:3000/d/${item[0]['grafanaUid']}?theme=light`" width="100%" height="700px" frameborder="0"></iframe>        
    </div>
    <a :href="`http://localhost:3000/d/${item[0]['grafanaUid']}`">Grafana에서 보기</a>
    <div>
      임계치 설정
      <EditAlert />
    </div>
    
</div>
</template>

<script>
import SubHeader from '@/components/Main/SubHeader'
import EditAlert from '@/components/Server/EditAlert'
import axios from 'axios';

  export default {
  components: { SubHeader, EditAlert },
    props: {
      id: Number
    },
    data() {
      return {
        item: null,
        url : "http://localhost:3000/d/"
      }
    },
    mounted() {
    this.id = this.$route.params.id 
  },
 
  created () {
      axios.get('http://localhost:8000/api/Charts?ip=' + this.$route.params.id)
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