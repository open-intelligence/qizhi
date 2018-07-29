<!--
<style>
  @import "../assets/styles/jsonEditor.less";
</style>

<template>

  <Row>
    <Col span="15">
      <Card>
        <div id="editor_holder"></div>
        <div style="text-align: center">
          <Button class="submit" @click="checkValidate">Submit</Button>
        </div>
      </Card>
    </Col>
    <Col span="9">
      <Card class="margin-left-10" >
        <p slot="title">
          <Icon type="android-hand"></Icon>
          Json Code:
        </p>
        <pre id="code_context" style="height: 800px;overflow: scroll"></pre>
      </Card>
    </Col>
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
    watch:{
      editor:{
        handler:function(cur,old){
          this.syntaxHighlight(cur.getValue())
        },
        deep:true
      }
    },
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
        this.syntaxHighlight(this.editor.getValue());

      },
      syntaxHighlight(json) {
        if (typeof json !== 'string') {
          json = JSON.stringify(json, undefined, 2);
        }
        json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
        document.getElementById('code_context').innerHTML = json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
          var cls = 'number';
          var sty = 'darkorange';
          if (/^"/.test(match)) {
            if (/:$/.test(match)) {
              cls = 'key';
              sty = 'red';
            } else {
              cls = 'string';
              sty = 'green';
            }
          } else if (/true|false/.test(match)) {
            cls = 'boolean';
            sty = 'blue'
          } else if (/null/.test(match)) {
            cls = 'null';
            sty = 'magenta'
          }
          return '<span class="' + cls + '" style="color:' + sty + '">' + match + '</span>';
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
          type: 'PUT',
          dataType: 'json',
          success: (data) => {
            this.jump();
          },
          error: (xhr, message, error) => {
            const res = JSON.parse(xhr.responseText);
            this.$Message.error(res.message)
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
-->
