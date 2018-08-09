<template>
  <div class="list">

    <Row>
      <Col>
      <Card>
        <div slot="title"><Icon type="ios-film-outline"></Icon>Jobs</div>
        <a href="#" slot="extra" @click.prevent="refresh">
          <Icon type="ios-loop-strong"></Icon>
        </a>
        <Table stripe  :loading="loading2" :show-header="showHeader" :height="fixedHeader ? 300 : ''" :size="tableSize"
               :data="listData"
               :columns="columns" ref="table" @on-select="onSelect" @on-selection-change="onSelectionChange"></Table>
        <Page :total="100" show-sizer show-elevator @on-change="pageChange" style="margin-top: 10px"
              @on-page-size-change="PageSizeChange"></Page>
      </Card>
      </Col>
    </Row>
  </div>
</template>tableSize
<script>
  import elementResizeDetectorMaker from 'element-resize-detector'
  var erd = elementResizeDetectorMaker()
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
        columns: [
          {
            title: 'name',
            key: 'name'
          },
          {
            title: 'capacity',
            key: 'capacity',
            className: 'min-width'
          },
          {
            title: 'memory',
            key: 'memory'
          },
          {
            title: 'GPUs',
            key: 'GPUs'
          },
          {
            title: 'vCores',
            key: 'vCores'
          },
          {
            title: 'ActiveJobs',
            key: 'numActiveJobs',
            sortable: true
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
                      this.$router.push('/jobs')
                    }
                  }
                }, 'View'),
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
                    this.jumpUrl(params.row.name)
                    }
                  }
                }, 'Go to Yarn Page'),
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
        this.$api.virtualClusters(params).then((res) => {
          let data = [];
             for(let item in res){
               let obj = {};
               obj.name = item;
               obj.capacity = res[item]['capacity']+'%';
               obj.numActiveJobs = res[item]['numActiveJobs'];
               obj.GPUs = res[item]['resourcesUsed']['GPUs'];
               obj.memory = res[item]['resourcesUsed']['memory']+'MB';
               obj.vCores = res[item]['resourcesUsed']['vCores'];
               data.push(obj);
             }
          this.listData = data;
          this.DateReady = true;
          this.loading2 = false
        })
      },
      /**
       * 页面跳转*
       * */
      jumpUrl(item){
        window.open('http://162.105.95.173:8088/cluster/scheduler?openQueues='+item);
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
      },
      onSelectionChange (selection) {
        this.selection = selection
      }
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

