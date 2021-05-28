<template>
  <div class="content">
    <div>
      <div v-if="server == 'AddServer'">
        <AddServer />
      </div>
      <div v-if="server == 'DeleteServer'">
        <DeleteServer />
      </div>
    </div>
  </div>
</template>

<script>
import AddServer from '@/components/Server/AddServer'
import DeleteServer from '@/components/Server/DeleteServer'
export default {
  name: "Content",
  props: {
    server: String,
  },
  components: {
    AddServer, DeleteServer
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
