<template>
  <div>
    <Menu mode="horizontal" :theme="theme1" active-name="1"  @on-select="selectFn">
    <MenuItem name="config" >
      <Icon type="ios-paper"></Icon>
      View Job Config
    </MenuItem>
    <MenuItem name="Tracking">
        <Icon type="stats-bars"></Icon>
        Go to Application Tracking Page
    </MenuItem>
    <MenuItem name="Metrics">
      <Icon type="settings"></Icon>
      Go to Job Metrics Page
    </MenuItem>
  </Menu>

    <Row>
      <Col>
        <Card>
          <div slot="title"><Icon type="ios-film-outline"></Icon>Jobs</div>
            <Icon type="ios-loop-strong"></Icon>
          <Table stripe  :loading="loading" :show-header="showHeader" :height="fixedHeader ? 300 : ''" :size="tableSize"
                 :data="listData"
                 :columns="columns" ref="table" @on-select="onSelect" ></Table>
          <Page :total="100" show-sizer show-elevator @on-change="pageChange" style="margin-top: 10px"></Page>
        </Card>
      </Col>
    </Row>

    <Collapse  v-model="summary">
      <Panel  name="summary">
      &nbsp;View Application Summary
        <div slot="content">
          <p>Start Time: {{launchTime}}</p>
          <p>Finish Time: {{completedTime}}</p>
          <p>Exit Diagnostics:</p>
          <br>
        <pre >{{jobDetail}}</pre>
        </div>
      </Panel>
    </Collapse>

  </div>

</template>
<script>
  import config from '../../../config/index'
  export default {
    name: 'jobDetail',
    data () {
      return {
        modal: false,
        fixedHeader:true,
        showHeader:true,
        loading:false,
        summary:'summary',
        theme1: 'light',
        tableSize: 'small', // @:size
        name:'',
        trackingUrl:'',
        launchTime:'',
        completedTime:'',
        listData:[],
        params:{},
        jobDetail:{},
        columns: [
          {
            title: 'Task Role',
            key: 'name'
          },
          {
            title: 'Task Index',
            key: 'index',
            className: 'min-width'
          },
          {
            title: 'Container Name',
            key: 'container'
          },
          {
            title: 'IP',
            key: 'ip'
          },
          {
            title: 'http',
            key: 'http'
          },
          {
            title: 'ssh',
            key: 'ssh'
          },
          {
            title: 'GPUs',
            key: 'gpu',
           // sortable: true
          },
          {
            title: 'actions',
            key: 'action',
            width: 170,
            fixed: 'right',
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'text',
                    size: 'small'
                  },
                  style: {
                    color: '#5cadff'
                  },
                  on: {
                    click: () => {
                      /*this.$router.push('/jobs')*/
                      this.$Message.error('抱歉，暂无相关信息!')
                    }
                  }
                }, 'View SSH Info '),
                h('Button', {
                  props: {
                    type: 'text',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px',
                    color: '#5cadff'
                  },
                  on: {
                    click: () => {
                      console.log(params.row.containerLog);
                     window.open(params.row.containerLog) ;
                    }
                  }
                }, 'Go to Tracking Page'),
              ])
            }
          }
        ]

      }
    },
    mounted(){
      this.name = this.$store.state.app.jobDetailName;
      let jobName = this.name;
      this.$api.getConfig(this.name).then((res)=>{
        this.params = res;
        console.log(res);
      }).catch((err)=>{
        console.log('err',err)
      });
      this.$api.getJobDetail(this.name).then( res =>{
        this.trackingUrl = res.jobStatus.appTrackingUrl;
        this.launchTime= this.convertTime(res.jobStatus.appLaunchedTime);
        this.completedTime =this. convertTime(res.jobStatus.appCompletedTime);
        this.jobDetail = res.jobStatus.appExitDiagnostics ? res.jobStatus.appExitDiagnostics:'Not available yet.';
        for(let key of Object.keys(res.taskRoles)){
          res.taskRoles[key].taskStatuses.forEach((item)=>{
                    let data={};
                    data.name = key;
                    data.index = item.taskIndex;
                    data.container =  item.containerId;
                    data.ip = item.containerIp;
                    data.http = item.containerPorts.http;
                    data.ssh = item.containerPorts.ssh;
                    data.gpu = item.containerGpus;
                    data.containerLog = item.containerLog;
                    this.listData.push(data);
          })
        }
        console.log(this.listData);
      }).catch( err =>{
        console.log('err',err);
      })
    },
    methods:{
      selectFn(index){
        if(index === "config"){
          this.$Modal.info({
            title: this.name,
            content: '<pre><code>'+JSON.stringify(this.params, undefined, 2)+'</code></pre>'
          });
        }else if(index === "Tracking"){
           window.open(this.trackingUrl);
        }else if(index === "Metrics"){
           window.open(config.build.baseServerUrl+'/grafana/dashboard/db/joblevelmetrics?var-job='+this.name)
        }
      },
      convertTime(time){
        let newDate = new Date(time);
         return newDate.toLocaleString();
      },
      pageChange(){},
      onSelect(){},
    }
  }
</script>
<style>
  pre{
    display: block;
    padding: 9.5px;
    margin: 0 0 10px;
    font-size: 13px;
    line-height: 1.42857143;
    color: #333;
    word-break: break-all;
    word-wrap: break-word;
    background-color: #f5f5f5;
    border: 1px solid #ccc;
    border-radius: 4px;
    white-space: pre-wrap;
  }
  .ivu-modal-confirm-body{
    padding-left: 0;
  }
  .ivu-modal-confirm-body-icon-info{
    display:none
  }
  .ivu-collapse{
    margin-top: 10px;
  }
</style>
