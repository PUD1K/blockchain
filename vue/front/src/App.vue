<template>

  <div class="main_page">
    <div class="columns mt-2">
      <div class="column is-6 is-offset-3">
        <a id="main" class="is-size-4" @click="main=0">Main</a>
        <a id="chains" class="is-size-4" @click="main=1">Chains</a>
        <a id="chains" class="is-size-4" @click="main=2">Messages</a>
      </div>
    </div>
    <div class="main" v-if="main==0">
        <div class="columns">

            <div class="column is-6 is-offset-3 box mt-5">
                <div class="field">
                    <label>Hach</label>
                    <div class="control is-link">
                        <input type="text" class="input is-link" v-model="hach" :readonly="true">
                    </div>
                </div>

                <div class="field">
                    <label>Coins</label>
                    <div class="control">
                        <input type="text" class="input is-link" v-model="coins" :readonly="true">
                    </div>
                </div>

                <div class="field">
                    <label>Pass</label>
                    <div class="control is-link">
                        <input type="text" class="input is-link" v-model="pass" :readonly="true">
                    </div>
                </div>

                <div class="field">
                  <div class="control has-text-centered">
                      <button class="button is-link" @click="update_coins">Update coins</button>
                  </div>
                </div>
            </div>

        </div>   

        <div class="columns mt-4">
        <div class="column is-6 is-offset-3 box">
                <div class="field">
                    <label>To hach</label>
                    <div class="control">
                        <input type="text" class="input is-link" v-model="to_hach">
                    </div>
                </div>

                <div class ="field">
                  <label>Type task</label>
                  <div class="select is-link is-normal is-6">
                    <select v-model="type_task">
                        <option>send_coins</option>
                        <option>custom</option>
                    </select>
                  </div>
                </div>

                <div class="field">
                    <div class="control">
                      <label>Body</label>
                        <input type="text" class="input is-link" v-model="body">
                    </div>
                </div>

                <div class="field">
                  <div class="control has-text-centered">
                      <button class="button is-link" @click="send_task">Send task</button>
                  </div>
                </div>
            </div> 
          </div>

          <div class="column box mt-4 is-offset-3 mb-3" id="foo">
                <div class="control has-text-left">
                  <button v-if="!doing_tasks" id="do_tasks" class="button is-link " @click="do_tasks">Do tasks</button>
                  <button v-if="doing_tasks" id="do_tasks" class="button is-link " @click="stop_tasks">Stop doing tasks</button>
                  <!-- <strong id="doing_tasks" class="is-size-5">Doing tasks: </strong><span class="is-size-5">{{doing_tasks}}</span> -->
            </div>
          </div>

          <div class="column box mt-4 is-offset-3 mb-6" id="foo">
              <div class="control has-text-left">
                <button class="button is-link" @click="get_chains">Update chains</button>
                <button id="get_tasks" class="button is-link " @click="get_tasks">Get tasks</button>
            </div>
          </div>

        </div>

          <div class="column mt-4" v-if="main==1">
            <BlockChain
                v-for="block in blocks"
                v-bind:key ="block.id"
                v-bind:block="block"/>
          </div>

          <div class="column mt-4" v-if="main==2">
            <div class="columns">

            <div class="column is-7 is-offset-3 box mt-5">
                <div class="field">
                    <label>Hach</label>
                    <div class="control is-link">
                        <input type="text" class="input is-link" v-model="selected_hach" :readonly="false">
                    </div>
                </div>

                <div class="field">
                  <div class="control has-text-centered">
                      <button class="button is-link" @click="get_messages">Update_messages</button>
                  </div>
                </div>
            </div>

        </div> 

            <MessagesChain 
                v-for="block in chat"
                v-bind:key ="block.id"
                v-bind:block="block"/>
          </div>

      </div>

</template>

<script>
import axios from 'axios';
import BlockChain from '@/components/BlockChain.vue'
import MessagesChain from '@/components/MessagesChain.vue'


import { toast } from 'bulma-toast'



export default {
  components:{
    BlockChain,
    MessagesChain
  },
  data(){
    return{
      username: "tum",
      password: "1",
      hach: "",
      type_task: "",
      body: "",
      doing_tasks: false,
      main: true,

      selected_hach: "",
      pass: "123",

      blocks: [],
      chat: []
    }
  },
  async mounted(){
    this.get_data()
    await this.get_chains()

    this.get_messages()
    console.log(this.chat)
  },
  methods:{
    async get_data(){
      await axios 
        .get('/my_data/')
        .then(response => {
          this.username = response.data.username
          this.hach = response.data.hach
          this.selected_hach = this.hach
          this.coins = response.data.coins
        })
        .catch(error => {
          console.log(error)
        })
    },
    async update_coins(){
      await axios
        .get('/update_coins/')
        .then(response => {
          this.coins = response.data.coins
          console.log(this.coins)
        })
        .catch(error => {
          console.log(error)
        })
    },

    async get_chains(){
      await axios
        .get('/get_chains/')
        .then(response => {
          response.data.chains.block_active.forEach((elem) => {
            if(elem.data_json.length != 0)
              this.blocks.push({"id": elem.id, "data_json": elem.data_json})
          })
        })
        .catch(error => {
          console.log(error)
        })
    },

    async send_task(){

      if(!!this.hach && !!this.to_hach && !!this.type_task && !!this.body){
        console.log(this.type_task)
        if(this.type_task == "custom"){
          const encrypt_body = {
            password: this.pass,
            message: this.body 
          }

          var msg = {}
          await axios
            .post('/encrypt_message/', encrypt_body)
            .then(response => {
              msg = response.data
            })
            .catch(error => {
              console.log(error)
            })


          const request_body = {
            from_hach: this.hach,
            to_hach: this.to_hach,
            type_task: this.type_task,
            message: msg
          }
          await axios
            .post('/send_message/', request_body)
            .then(response => {
              console.log(response)

              toast({
                    message: 'You are successful send message',
                    type: 'is-success',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'bottom-right',
                })
            })
            .catch(e =>{
              console.log(e)
            })
        }else if(this.type_task == "send_coins"){
          const request_body = {
            from_hach: this.hach,
            to_hach: this.to_hach,
            type_task: this.type_task,
            count_coins: this.body
          }
          await axios
            .post('/send_coins/', request_body)
            .then(response => {
              console.log(response)

              toast({
                    message: `You are successful send ${request_body.count_coins} coins`,
                    type: 'is-success',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'bottom-right',
                })
            })
            .catch(e =>{
              console.log(e)
            })
        }
      } else {
        toast({
              message: `Somebody parameter was skipped`,
              type: 'is-danger',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'bottom-right',
          })
      }
    },
    async get_tasks(){
      await axios
        .get('/get_tasks/')
        .then(response => {
          console.log(response)
        })
        .catch(e =>{
          console.log(e)
        })
    },
    async do_tasks(){
      axios
        .get('/do_tasks/')
        .then(response => {
          this.doing_tasks = true
          console.log('popa')
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },
    async stop_tasks(){
      axios
        .get('/stop_tasks/')
        .then(response => {
          this.doing_tasks = false
          console.log(response)
        })
        .catch(e => {
          console.log(e)
        })
    },

    get_messages(){
      this.chat = []
      // c кем ведется переписка
      var user_hach = ""
      var from_hach = ""
      var to_hach = ""

      this.blocks.forEach(block => {
        block.data_json.forEach(elem => {
            if(elem.data_json.type_task == "custom" && (elem.data_json.to_hach == this.selected_hach|| elem.data_json.from_hach == this.selected_hach)){
              // если мне отправили
              if(elem.data_json.to_hach == this.selected_hach){
                user_hach = elem.data_json.from_hach
                from_hach = user_hach
                to_hach = "me"
              }

              if(elem.data_json.from_hach == this.selected_hach){
                // если я отправил
                user_hach = elem.data_json.to_hach
                from_hach = "me"
                to_hach = user_hach
              }

              let index = this.search_value(this.chat, user_hach)
              if(index == null){
                  this.chat.push({
                      "user_hach": user_hach,
                      "messages": []
                  })
                  index = this.search_value(this.chat, user_hach)
              }
              this.chat[index]["messages"].push({
                "from_hach": from_hach,
                "to_hach": to_hach,
                "message": elem.data_json.message
              })

            }
        })
      })
    },
    search_value(obj, hach){
        for(var i = 0; i < obj.length; i++){
            if(obj[i]["user_hach"] == hach){
                return i
            }
        }
    }
  }
}
</script>

<style lang="scss">
@import '../node_modules/bulma';

.select, .select select{ 
width: 100%;
}

button#get_tasks {
    position: relative;
    left: 510px;
    right: 0 "";
}

div#foo{
  width:740px;
}

strong#doing_tasks{
  padding-left:30px;
}

a#chains{
  padding-left:200px;
}

a#main{
  padding-left:50px
}

a:link {
  text-decoration: none;
}

a:visited {
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

a:active {
  text-decoration: underline;
}
</style>

