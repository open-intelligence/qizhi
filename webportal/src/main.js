// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import store from './vuex/store.js'
import VueI18n from 'vue-i18n'
import router from './router'
import iView from 'iview'
import api from './api/index.js'
import Cookies from 'js-cookie'

import 'highlight.js/styles/default.css';
import Highlight from 'vue-markdown-highlight'

Vue.use(Highlight);
Vue.use(api)
Vue.use(iView)
Vue.use(VueI18n);



import 'iview/dist/styles/iview.css' // 使用 CSS
import '@/assets/styles/layout/layout.less' // 引入布局样式
import '@/assets/styles/cover/cover.less' // 覆盖样式
import '@/assets/styles/base/base.less'

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  watch:{
    '$router':'checkLogin'
  },
  created(){
   this.checkLogin();
  },
  methods:{
    checkLogin(){
      //检查是否存在session
      if(!Cookies.get('session')){
        this.$router.push('/login');//若未登录则跳转到登陆状态
      }else{
        this.$router.push('/index');//已登陆则跳转到主界面
      }
    }
  }
});
