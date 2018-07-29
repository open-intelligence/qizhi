
<template>
  <div class="index">
    <Row  :gutter="24">
      <Col :md="24" :lg="8" >
        <Card>
          <p slot="title" class="card-title">
            <Icon type="android-wifi"></Icon>
            各类用户服务调用变化统计
          </p>
          <div class="data-source-row">
            <user-flow></user-flow>
          </div>
        </Card>
      </Col>
      <Col :md="24" :lg="16">
        <Row :gutter="5">
          <Col :xs="24" :sm="12" :md="6" :style="{marginBottom: '10px'}">
            <infor-card
              id-name="user_created_count"
              :end-val="count.createUser"
              iconType="android-person-add"
              color="#2d8cf0"
              intro-text="今日新增用户"
            ></infor-card>
          </Col>
          <Col :xs="24" :sm="12" :md="6" :style="{marginBottom: '10px'}">
            <infor-card
              id-name="visit_count"
              :end-val="count.visit"
              iconType="ios-eye"
              color="#64d572"
              :iconSize="50"
              intro-text="今日浏览量"
            ></infor-card>
          </Col>
          <Col :xs="24" :sm="12" :md="6" :style="{marginBottom: '10px'}">
            <infor-card
              id-name="collection_count"
              :end-val="count.collection"
              iconType="upload"
              color="#ffd572"
              intro-text="今日数据采集量"
            ></infor-card>
          </Col>
          <Col :xs="24" :sm="12" :md="6" :style="{marginBottom: '10px'}">
            <infor-card
              id-name="transfer_count"
              :end-val="count.transfer"
              iconType="shuffle"
              color="#f25e43"
              intro-text="今日服务调用量"
            ></infor-card>
          </Col>
        </Row>
        <Row>
          <Card :padding="0">
            <p slot="title" class="card-title">
              <Icon type="map"></Icon>
              今日服务调用地理分布
            </p>
            <div class="map-con">
              <Col span="9">
                <map-data-table :cityData="cityData" height="281" :style-obj="{margin: '12px 0 0 11px'}"></map-data-table>
              </Col>
              <Col span="14" class="map-incon">
                <Row type="flex" justify="center" align="middle">
                  <home-map :city-data="cityData"></home-map>
                </Row>
              </Col>
            </div>
          </Card>
        </Row>
      </Col>
    </Row>
    <Row :gutter="24">
      <Col :md="24" :lg="8" :style="{marginTop: '10px'}">
        <Card>
          <p slot="title" class="card-title">
            <Icon type="android-wifi"></Icon>
            内存使用量統計
          </p>
            <div class="data-chart-row">
          <memory-map></memory-map>
        </div>
        </Card>
      </Col>
      <Col :md="24" :lg="8" :style="{marginTop: '10px'}">
        <Card>
          <p slot="title" class="card-title">
            <Icon type="android-wifi"></Icon>
            編不下去了
          </p>
          <div class="data-chart-row">
            <line-data></line-data>
          </div>
        </Card>
      </Col>
      <Col :md="24" :lg="8" :style="{marginTop: '10px'}">
        <Card>
          <p slot="title" class="card-title">
            <Icon type="android-wifi"></Icon>
            老子不幹了
          </p>
          <div class="data-chart-row">
            <line-map></line-map>
          </div>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>
  import cityData from '../assets/js/get-city-value'
  import lineMap from './views/lineMap'
  import lineData from './views/lineData'
  import inforCard from './views/inforCard'
  import mapDataTable from './views/mapDataTable'
  import homeMap from './views/map'
  import userFlow from './views/userFlow'
  import memoryMap from './views/memoryMap'

  export default {
    name: 'index',
    components:{
      userFlow,
      inforCard,
      mapDataTable,
      homeMap,
      memoryMap,
      lineData,
      lineMap
    },
    data () {
      return {
        params: {
          page: 1,
          limit: 10
        },
        count: {
          createUser: 496,
          visit: 3264,
          collection: 24389305,
          transfer: 39503498
        },
        cityData: cityData,
      }
    },
    computed: {},
    methods: {
      /**
       * 刷新页面请求
       * */
      refresh () {

      }
    },
    created () {

    }
  }
</script>
<style lang="less" scoped>
  .cardMessage {
    .ivu-icon {
      font-size: 38px;
    }
    .subText {
      color: #9ea7b4;
    }
  }
</style>
