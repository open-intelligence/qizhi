<template>
  <div class="list">
    <Row>
      <Col>
      <Card>
        <a href="#" slot="extra" @click.prevent="refresh">
          <Icon type="ios-loop-strong"></Icon>
        </a>
        <Table stripe  :loading="loading2" :show-header="showHeader" :height="fixedHeader ? 300 : ''" :size="tableSize"
               :data="listData"
               :columns="columns1" ref="table" @on-select="onSelect" @on-selection-change="onSelectionChange"></Table>
        <Page :total="100" show-sizer show-elevator @on-change="pageChange" style="margin-top: 10px"
              @on-page-size-change="PageSizeChange"></Page>
      </Card>
      </Col>
    </Row>
  </div>
</template>
<script>
  import elementResizeDetectorMaker from 'element-resize-detector'
  import Vue from 'vue'
  var erd = elementResizeDetectorMaker();
  import jQuery from 'jquery'
  import Cookies from 'js-cookie'
  import config from '../../../config'
  Vue.use(jQuery);
  export default {
    name: 'list',
    components: {},
    data () {
      return {
        formItem: {
          input: '',
          select: '',
          date: '',
          time: '',
          radio: '',
          checkbox: []
        },
        searchState: false,
        editModal: false,
        detailModal: false,
        deleteTip: false,
        showHeader: true, // 是否显示表头 @:show-header
        loading2: true, // 分页loading
        fixedHeader: false, // 是否固定表头 @:height
        tableSize: 'small', // @:size
        DateReady: false, // 判断异步数据加载完成，避免报错
        loading: false, // save
        currDate: {}, // 当前编辑和新增的行数据
        currIndex: 0, // 当前编辑和新增的行号
        saveDisabled: false,
        params: {
          page: 1,
          limit: 10,
          category: 'Android'
        },
        status_style:{},
        selection: [], // 表格选中项
        listData: [], // @:data
         columns1: [
         {
           title: 'Job',
           key: 'name'
         },
         {
           title: 'User',
           key: 'username'
         },
         {
           title: 'Start Time',
           key: 'createdTime',
           sortable: true   //是否允許排序
         },
         {
           title: 'Retries',
           key: 'retries',
         },
         {
             title: 'Status',
             key: 'state',
             color: '#5cadff'
           },
           {
           title: '操作',
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
                   marginRight: '5px',
                   color: '#5cadff'
                 },
                 on: {
                   click: () => {
                     this.$store.state.app.jobDetailName = params.row.name;
                     this.$router.push('/jobDetail');
                   }
                 }
               }, '查看'),
               h('Button', {
                 props: {
                   type: 'text',
                   size: 'small'
                 },
                 style: {
                   color: '#ff3300'
                 },
                 on: {
                   click: () => {
                     if(params.row.state ==="FAILED"|| params.row.state ==="SUCCEEDED"||params.row.state ==="STOPPED")
                       this.$Message.error("this job has being finished");
                     else {
                       this.remove(params.index);
                       this.stopProcess(params)
                     }
                   }
                 }
               }, '終止')
             ])
           }
         }
       ]
      }
    },
    watch: {
      /**
       * @params 监听参数变化重新获取数据
       * */
      params: {
        handler (val) {
          this.getData(val)
        },
        deep: true
      },
      fixedHeader: {
        handler (val) {
          if (val) {
            this.$Message.info('表头已固定')
          }
        }
      },
      currDate: {
        handler (val) {
          for (let i = 0; i < Object.values(val).length; i++) {
            if (Object.values(val)[i] === '') {
              this.saveDisabled = true
              return
            } else {
              this.saveDisabled = false
            }
          }
        },
        deep: true
      }
    },
    computed: {
      state () {
        return this.$store.state.app
      }
    },
    methods: {
      searchShow () {
        this.searchState = !this.searchState
      },
      /**
       * 刷新页面请求
       * */
      refresh () {
        this.getData(this.params)
      },
      /**
       * @params:category 分类 page：页码 limit:条数
       * */
      getData (params) {
        this.loading2 = true;
        this.$api.jobList(params).then((res) => {
           if(res.length){
             res.forEach((item,index)=>{
               var newDate = new Date(item.createdTime);
               item.createdTime = newDate.toLocaleString();
              if(item.state==="SUCCEEDED"){
                item.cellClassName={
                  state: 'demo-table-info-cell-name-success'
                }
              }else if(item.state==="FAILED"){
                item.cellClassName={
                  state: 'demo-table-info-cell-name-fail'
                }
              }else{
                item.cellClassName={
                  state: 'demo-table-info-cell-name-wait'
                }
              }
             });
             this.listData = res;
             this.DateReady = true;
             this.loading2 = false
           }
        })
      },
      /**
       * @on-change 页码改变的回调，返回改变后的页码
       * */
      pageChange (page) {
        this.params.page = page
      },
      /**
       * @on-page-size-change 切换每页条数时的回调，返回切换后的每页条数
       * */
      PageSizeChange (limit) {
        this.params.limit = limit
      },
      /**
       * 表格对应操作方法
       * @show 查看
       * @remove 删除
       * @edit
       */
      show (index) {
        this.currIndex = index
        this.currDate = this.listData[index]
        this.detailModal = true
        this.$Modal.info({
          title: '详情',
          content: `姓名：${this.listData[index].who}<br>平台：${this.listData[index].type}<br>描述：${this.listData[index].desc}`
        })
      },
      remove (index) {
        this.listData.splice(index, 1)
      },
      edit (index) {
        this.editModal = true;
        this.currIndex = index;
        if (index === -1) { // 新增
          this.currDate = {
            createdAt: '',
            desc: '',
            publishedAt: '',
            type: '',
            used: true,
            who: '',
            url: 'c.fwone.com'
          }
        } else { // 编辑
          this.currDate = this.listData[index]
        }
      },
      /**
       * 批量删除
       */
      deleteBatch () {
        this.deleteTip = false
        // ...
      },
      saveBatch () {
        this.loading = true
        setTimeout(() => {
          this.loading = false
          this.$Message.info('保存成功')
          this.editModal = false
        }, 3000)
      },
      /**
       * 数据导出
       * @ type 1 原始数据 2过滤数据
       */
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: '原始数据'
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: '排序和过滤后的数据',
            original: false
          })
        }
      },
      /**
       * 多选
       * selection：已选项数据 row：刚选择的项数据
       */
      onSelect (selection, row) {
        // console.log(selection,row)
      },
      onSelectionChange (selection) {
        this.selection = selection
      },
      /**
       * 删除正在进行的作业
       * */
      stopProcess(params){
        let token = Cookies.get('token');
        jQuery.ajax({
          url: config.build.baseServerUrl+"/rest-server/api/v1/jobs/"+params.row.name+"/executionType",
          type: 'PUT',
          data: {
            value: 'STOP',
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
          success: (data) => {
          },
          error: (xhr, textStatus, error) => {
            const res = JSON.parse(xhr.responseText);
            alert(res.message);
          },
        });
      },

    },
    created () {
      this.getData(this.params)//獲取的數據入口
    },
    mounted () {
      erd.listenTo(window, 'resize', this.handleResize)
    }
  }
</script>
<style lang="less" scoped>
  .search-filter {
    opacity: 0;
    display: none;
    overflow: hidden;
    transition: all 0.28s ease-out;
    &.active {
      opacity: 1;
      display: block;
    }
  }
</style>

