<template>
  <div class="product">
    <div class="form-group">
    <h1>서버 삭제하기</h1>
        IP Address: <input type="text" v-model="ip" placeholder="IP Address"/>
        <br/>
        <button @click="[deleteServer(), isModalViewed = true]">서버 삭제</button>     
        <ModalView 
            v-if="isModalViewed" 
            @close-modal="[isModalViewed = false, result = '로딩중입니다.']"> 
            <Content 
                :message="result"/> 
        </ModalView> 
<!-- 
        <button @click="validationCheck()">{{ connection }}</button>
        <br/> -->
    </div>
    

  </div>
</template>

<script>
import axios from 'axios';
import Content from "./Content";
import ModalView from "./ModalView";

export default {
    name : "DeleteServer",
    components: { 
        Content, 
        ModalView, 
    },
    data() {
        return {
            ip: '',
            username: '',
            password: '',
            isModalViewed: false,
            result: null
            // connection: '서버 연결 확인'
        }
    },
    methods : {
        deleteServer : function() {
            axios.post('http://localhost:8000/api/deleteServer', { ip:this.ip }
            ).then(response => {
                console.warn(response)
                this.result = response.data.message
                // return JSON.parse(response).data.get('data')
            }).catch((ex) => {
                console.warn("ERROR!!!!! : ",ex)
            })
        },
        // validationCheck : function() {
        //     axios.post('http://localhost:8000/api/server', { ip:this.ip, username:this.username, password:this.password }
        //     ).then(response => {
        //         console.warn(response)
        //         this.result = response.data
        //     }).catch((ex) => {
        //         console.warn("ERROR!!!!! : ",ex)
        //     })
        // },
    }
    
}
</script>

<style>
.form-group {
  position: relative;
  max-width: 35%;
  margin: auto;
  margin-top: 100px;
  padding: 0px;
  background-color: white;
  min-height: 500px;
  z-index: 10;
  opacity: 1;
  border-radius: 20px;
  border: 2px;
  border-color: black;
}
</style>