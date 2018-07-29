<style>
  iframe{
    display:block;
    width:100%;
    height:921px;
    border:none;
  }

</style>
<template>
  <iframe  :src="url"></iframe>
</template>
<script>
  import config from '../../../config'
  export default {
    name: 'index',
    data () {
      return {
        url:config.pai_clusterview.url
      }
    },
  }
</script>
