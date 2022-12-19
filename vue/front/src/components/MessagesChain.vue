<template>
    <div class="column box is-offset-3 is-7 has-border-info">
        <h3 class="is-size-4 mb-3">{{block.user_hach}}</h3>

        <div
            v-for="message in block.messages"
            v-bind:key="message.id">
                <!-- <div class="field">
                    <label>From hach</label>
                    <div class="control is-link">
                        <input type="text" class="input is-link" v-model="message.from_hach" :readonly="true">
                    </div>
                </div>
                <div class="field">
                    <label>To hach</label>
                    <div class="control is-link">
                        <input type="text" class="input is-link" v-model="message.to_hach" :readonly="true">
                    </div>
                </div> -->
                <!-- <div class="field" v-if="message.from_hach == 'me'">
                    <h3 class="is-size-5">Me</h3>
                    <div class="control is-link">
                        <input type="text" id="message" class="input is-primary mb-2" v-model="message.message" :readonly="true">
                    </div> 
                </div>
                <div class="field" v-else style="text-align:right;">
                    <label class="is-size-5">He/She</label>
                    <div class="control is-link">
                        <input type="text" id="message" class="input is-link mb-2" v-model="    message.message" :readonly="true" style="text-align:right;">
                    </div>
                </div> -->

                <div class="field">
                    <div class="control is-link">
                        <p>{{decryptMessage(message.message)}}</p>
                    </div>
                </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "BlockChain",
  data(){
    return{
    }
  },
  props: {
      block: Object  
    },
  mounted(){
  },
  methods: {
    getKeyByValue(object, value){
        return Object.keys(object).find(key => object[key] === value)
      },
    decryptMessage(message){
        var msg = ""
        if(typeof message != "string"){
            const body = {
                private_key: "123",
                message: message
            }
            axios
                .post('/decrypt_message/', body)
                .then(response => {
                    msg = response.data.message
                })
                .catch(error => {
                    console.log(error)
                })
            console.log("msg: " + msg)
            return msg
        }
        return message.toString()   
    }
  }
};
</script>

<style lang="scss">
</style>
