<template>
    <div class="edit-form">
        <ModalView 
            v-if="isModalViewed" 
            @close-modal="[isModalViewed = false, result = '로딩중입니다.']"> 
            <Content 
                :message="result"/> 
        </ModalView> 
        
        온도 임계치: <input type="number" v-model="tempThreshold" placeholder="Temperature Threshold"/>
        <br/>
        파워 임계치: <input type="number" v-model="powerThreshold" placeholder="Power Threshold"/>
        <br/>
        
        
<!-- 
        <button @click="validationCheck()">{{ connection }}</button>
        <br/> -->
        <button @click="[addServer(), isModalViewed = true]">임계값 변경</button>
    </div>
</template>

<script>
import axios from 'axios';
import Content from "./Content";
import ModalView from "./ModalView";

export default {
    name : "AddServer",
    props: {
      id: Number
    },
    components: { 
        Content, 
        ModalView, 
    },
    data() {
        return {
            tempThreshold: null,
            powerThreshold: null,
            isModalViewed: false,
            result: null,
            item: null,
        }
    },
    methods : {
        addServer : function() {
            axios.post('/api/EditDashboard', { tempThreshold:this.tempThreshold, powerThreshold:this.powerThreshold, ip:this.id }
            ).then(response => {
                console.warn(response)
                this.result = response.data.status
                // return JSON.parse(response).data.get('data')
            }).catch((ex) => {
                console.warn("ERROR!!!!! : ",ex)
            })
        },

    },
    mounted() {
        this.id = this.$route.params.id 
    },
    
}
</script>
<style>
.edit-form {
  width: 100%;
  height: 80px;
  /* background-color: chartreuse; */
}
</style>