<template>
    <div class="edit-form">
        
        <ModalView 
            v-if="isModalViewed" 
            @close-modal="[isModalViewed = false, result = '로딩중입니다.']"> 
            <Content 
                :message="result"/> 
        </ModalView> 
        알림 받을 이메일: <input type="email" v-model="email" placeholder="Email Address"/>
        <br/>
        
<!-- 
        <button @click="validationCheck()">{{ connection }}</button>
        <br/> -->
        <button @click="[addServer(), isModalViewed = true]">이메일 추가</button>
    </div>
</template>

<script>
import axios from 'axios';
import Content from "./Content";
import ModalView from "./ModalView";

export default {
    name : "AddEmail",
    props: {
      id: Number
    },
    components: { 
        Content, 
        ModalView, 
    },
    data() {
        return {
            email: null,
            isModalViewed: false,
            result: null,
            item: null,
        }
    },
    methods : {
        addServer : function() {
            axios.post('/api/notification', { email: this.email }
            ).then(response => {
                console.warn(response)
                this.result = response.data.message
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