// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


// 导入模块
import apiList from './api'

const install = function (Vue) {
  if (install.installed) return
  install.installed = true

  // 定义属性到Vue原型中
  Object.defineProperties(Vue.prototype, {
    $api: {
      get () {
        return apiList
      }
    }
  })
}

export default {
  install
}
