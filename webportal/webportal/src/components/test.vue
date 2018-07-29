<style>
  @import "../assets/styles/jsonEditor.less";
</style>

<template>

  <Row>
    <Col span="24">
      <Card>
        <div id="editor_holder"></div>
        <div style="text-align: center">
          <Button class="submit" @click="checkValidate">Submit</Button>
        </div>
      </Card>
    </Col>
   <!-- <Col span="9">
        <Card class="margin-left-10" >
        <p slot="title">
          <Icon type="android-hand"></Icon>
          Json Code:
        </p>
        <pre id="code_context" style="height: 800px;overflow: scroll"></pre>
      </Card>
    </Col>-->
  </Row>
</template>
<script>
  import Vue from 'vue'
  import jQuery from 'jquery'
  import scheme from '../assets/js/scheme.js'
  import Cookies from 'js-cookie'
  import JsonEditor from 'json-editor'
  import config from '../../config'
  Vue.use(jQuery);
  export default {
    name:'jsonEditor,',
    data(){
      return{
        params:{
          token:'',
          data:{},
          name:''
        },
        editor:{}
      }
    },
    watch:{},
    mounted(){
      this.getData()
    },
    methods:{
      getData: function () {
        let element = document.getElementById('editor_holder');
        this.editor = new JSONEditor(element, {
          schema: scheme,
          theme: 'html',
          iconlib: 'html',
          disable_array_reorder: true,
          no_additional_properties: true,
          show_errors: 'always',
        });

      },
      checkValidate(){
        let errors = this.editor.validate();
        if( errors.length ){
          let message = errors.length === 1 ? ' is ONE ERROR ':' are '+errors.length +' ERRORS ';
          this.$Message.error('There'+message+' that need to be resolved. These errors are marked with red boxes');
        }else {
         this.submitJob();
        }
      },
      submitJob(){
        let data = this.editor.getValue();
        let token = Cookies.get('token');
        jQuery.ajax({
          url: config.build.baseServerUrl+'/rest-server/api/v1/jobs/'+ data.jobName,
          data: data,
          headers: {
            Authorization: `Bearer `+token,
          },
          type: 'GET',
          dataType: '',
          success: (data) => {
           this.jump();
          },
          error: ( error) => {
            console.log(error)
          },
        });
      },
      jump(){
        this.$router.push('/jobs')
      }
    }
  }
</script>
<style scoped>
</style>
