
<template>
  <vue-markdown v-highlight>{{msg}}</vue-markdown>
</template>
<script>

  import VueMarkdown from 'vue-markdown'
  import text from '../../../static/job-docs.md'
  export default {
    components: {
      VueMarkdown
    },
    data () {
      return {
        msg: text
      }
    }
  }
</script>
