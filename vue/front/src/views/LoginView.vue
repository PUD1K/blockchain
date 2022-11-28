<template>
    <div class="page-login">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Авторизация</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Логин</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Пароль</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Войти</button>
                        </div>
                    </div>

                    <hr>

                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'LoginView',
    data() {
        return{
            username:'',
            password:'',
            errors:[]
        }
    },
    mounted(){
        document.title = 'Авторизация'
    },
    methods:{
        async submitForm(){
            this.errors = []

            const formData = {
                username: this.username,
                password: this.password
            }
            
            await axios
                .post('/login/', formData)
                .then(response => {
                    localStorage.setItem("username", formData.username)
                    localStorage.setItem("password", formData.password)
                    console.log(response)
                    this.$router.push('/')
                })
                .catch(error => {
                    this.errors.push('Неверное имя пользователя или пароль.')
                    console.log(error)
                })
        }
    }
}
</script>
