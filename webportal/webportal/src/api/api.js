// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


import fetch from './fetch.js'
import { SERVER_BASE_URL } from './config'
import axios from 'axios'


// 登录
const  login = params => {
  var data = new URLSearchParams();
  data.append('username',params.username);
  data.append('password',params.password);
  data.append('expiration',86400);
  return fetch({
    baseURL:SERVER_BASE_URL,
    method:'post',
    url: `rest-server/api/v1/token`,
    data:data,
    headers: {
      'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    }
  })
}
// 登出
export function logout () {
  return fetch({
    url: '',
    method: 'post',
    headers: {
      'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    }
  })
}
//獲取用戶列表
const  jobList = params => {
  return fetch({
    baseURL:SERVER_BASE_URL,
    url: `rest-server/api/v1/jobs`,
    method:'get',
    params:'',
    headers: {
      'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    }
  })
}

const virtualClusters = params =>{
  return fetch({
    baseURL:SERVER_BASE_URL,
    url:'rest-server/api/v1/virtual-clusters',
    method:'get',
    params:'',
    headers: {
      'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    }
  })
}

//获取配置信息
const getConfig = params => {
  return fetch({
    baseURL:SERVER_BASE_URL,
    url: `rest-server/api/v1/jobs/${params}/config`,
    method: 'get',
    params: '',
    headers: {
      'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    }
  })
}

//获取用户工作详细信息
const getJobDetail = params => {
  return fetch({
    baseURL:SERVER_BASE_URL,
    url: `rest-server/api/v1/jobs/${params}`,
    method: 'get',
    params: '',
    headers: {
      'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    }
  })
}

const submit = params => {
  let jsonData = JSON.stringify(params.data);

  return fetch({
    baseURL:SERVER_BASE_URL,
    url: 'rest-server/api/v1/jobs/'+params.name,
    method: 'put',
    transformRequest: [function transformRequest(data, headers) {
      if (isObject(data)) {
        setContentTypeIfUnset(headers, 'application/x-www-form-urlencoded;charset=UTF-8');
        return JSON.stringify(data);
      }
    }],
    data:params.data,
    headers: {
      'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
      'Authorization': `Bearer `+params.token,
    }
  })
}


const apiList = {
  virtualClusters,
  login,
  getConfig,
  submit,
  jobList,
  getJobDetail
}

export default apiList
