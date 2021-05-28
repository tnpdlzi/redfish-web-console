<template>
  <div class="product">
    <SubHeader :id="id"/>
    <table id="detail-table">
      <div class="table-outline">
      <h2>상세 정보</h2>
      
      <h2>Systems</h2>
      <Systems />

      <h2>Chassis</h2>
      <Chassis />

      <h2>Processors</h2>
      <Processors />

      <h2>Memory</h2>
      <Memory />

      </div>
    </table>
  </div>
</template>

<script>
import SubHeader from '@/components/Main/SubHeader'
import Systems from './Systems'
import Chassis from './Chassis'
import Processors from './Processors'
import Memory from './Memory'

  export default {
  components: {
    SubHeader, Chassis, Systems, Processors, Memory
   },
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

  }
</script>

<style>
th {
  width: 200px;
  height: 50px;
  text-align: center;
  padding-right: 20px;
  border: 3px;
  border-color: black;
}

</style>