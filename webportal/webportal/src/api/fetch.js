// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


// 导入模块
import axios from 'axios'

// import router from '@/router'
import iView, {Notice } from 'iview'
// import store from '@/store'






export default function fetch (options) {
  return new Promise((resolve, reject) => {
      const instance = axios.create({
        timeout:5000,
    })
    console.log(instance);
    // http request 拦截器
    instance.interceptors.request.use(
      config => {
        iView.LoadingBar.start()
        // config.headers.Authorization = 'token'
        return config
      },
      err => {
        iView.LoadingBar.error()
        return Promise.reject(err)
      })

    // http response 拦截器
    instance.interceptors.response.use(
      response => {
        iView.LoadingBar.finish()
        return response
      },
      error => {
        iView.LoadingBar.error()
        if (error) {
        }
        return Promise.reject(error) // 返回接口返回的错误信息
      })

    // 请求处理
    instance(options)
      .then((res) => {
        // 请求成功时,根据业务判断状态
        /*  if (code === port_code.success) {
         resolve({code, msg, data})
         return false
         } else if (code === port_code.unlogin) {
         setUserInfo(null)
         router.replace({name: "login"})
         } */

        resolve(res.data);
        return false
      })
      .catch((error) => {
        console.log('ssssssssssssssssss',error);
        // 请求失败时,根据业务判断状态
        // Notice.error({
        //   title: '出错了！',
        //   desc: '错误原因 ' + JSON.stringify(error),
        //   duration: 0
        // })
        reject(error)
      })
  })
}


