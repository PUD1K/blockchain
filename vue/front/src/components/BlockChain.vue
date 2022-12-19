<template>
    <div class="column box is-offset-3 is-6 has-border-info">
        <h3 class="is-size-4 mb-6">Block №{{ block.id }}</h3>

        <div class="box"
            v-for="elem in block.data_json"
            v-bind:key="elem.id">
                <div class="field"
                    v-for="(i, index) in elem.data_json"
                    v-bind:key="i.id">
                    <label>{{getKeyByValue(elem.data_json, i)}}</label>
                    <div class="control is-link">
                        <input type="text" class="input is-link" v-model="elem.data_json[index]" :readonly="true">
                    </div>
                </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "BlockChain",
  data(){
  },
  props: {
      block: Object
  },
  mounted(){
  },
  methods: {
    getKeyByValue(object, value){
        return Object.keys(object).find(key => object[key] === value)
      }
  }
};
</script>

<style lang="scss">
</style>
