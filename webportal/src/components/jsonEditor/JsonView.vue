<template>
    <Row>
      <Col span="12">
            <div v-for="(item,index) in flowData" :key="index" :class="['block', 'clearfix', {'hide-block': hideMyBlock[index] == true}]">

            </div>
      </Col>
    </Row>
</template>

<script>
  export default {
    name: 'JsonView',
    props: {'parsedData': {}},
    data: function () {
      return {
        value1:'',
        'flowData': [],
        'toAddItem': false,
        'hideMyBlock': {}
      }
    },

    created: function () {
      this.flowData = this.parsedData
    },

    components: {
      'item-add-form': ItemAddForm
    },
    methods: {
      'delItem': function (parentDom, item, index) {
        this.flowData = this.flowData.rmIndex(index)
        if(this.hideMyBlock[index]) this.hideMyBlock[index] = false
        this.$emit('input', this.flowData)
      },

      'closeBlock': function (index, e) {
        this.$set(this.hideMyBlock, index, this.hideMyBlock[index]?false:true)
      },

      'addItem': function () {
        this.toAddItem = true
      },

      'cancelNewItem': function () {
        this.toAddItem = false
      },

      'newItem': function (obj) {

        let oj = {
          'name': obj.key,
          'type': obj.type
        }
        if(obj.type == 'array' || obj.type == 'object') {
          oj.childParams = obj.val
          oj.remark = null
        } else {
          oj.childParams = null
          oj.remark = obj.val
        }

        if(!oj.name) {
          alert('please must input a name!')
          return
        } else {

          this.flowData.push(oj)
          this.$emit('input', this.flowData)
          this.cancelNewItem()
        }
      },

      'keyInputBlur': function (item, e) {
        if(item.name.length <= 0) {
          alert('please must input a name!')
          item.name = "null"
          e.target.focus()
          // return 1
        }
        console.debug(item)
        console.debug(e)
      }
    }
  }
</script>

<style scoped>

</style>
