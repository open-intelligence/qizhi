// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


import Vue from 'vue'
import Router from 'vue-router'
import iView from 'iview'


import Index from '@/components/layout/index'
const Chart = () => import('@/components/layout/Chart')
//const Lock = () => import('@/components/layout/base/Lock')
const jobs = () => import('@/components/layout/jobs')
const jobDetail = () => import('@/components/layout/jobDetail')
const clusters = () => import('@/components/layout/VirtualClusters')
const Submit = () => import('@/components/layout/Submit')
const Introduction = () => import('@/components/layout/Introduction')
const test = () => import('@/components/test')
const Page = () => import('@/components/Page')


import E404 from '@/components/E404.vue'
import Login from '@/components/login.vue'
import Home from '@/components/Home'

Vue.use(Router);
Vue.use(iView);

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      name: 'home',
      component: Home,
      redirect: '/index',
      children: [
        {
          path: '/index',
          name: 'index',
          component: Index,
          icon: 'icon-wujiaoxing',
          level: 1,
          meta: {
            requiresAuth: true // 是否需要登录
          }
        },
        {
          path: '/chart',
          name: 'chart',
          component: Chart,
          meta: {
            requiresAuth: true // 是否需要登录
          }
        },
        {
          path: '/jobDetail',
          name: 'jobDetail',
          component: jobDetail,
          meta: {
            requiresAuth: true // 是否需要登录
          }
        },
        {
          path: '/jobs',
          name: 'jobs',
          component: jobs,
          meta: {
            requiresAuth: true // 是否需要登录
          }
        },
        {
          path:'/clusters',
          name:'clusters',
          component:clusters,
          meta:{
            requiresAuth:true// 是否需要登录
        }
        },
        {
          path: '/Submit',
          name: 'Submit',
          component: test,
          meta: {
            requiresAuth: true // 是否需要登录
          }
        },
        {
          path: '/Introduction',
          name: 'Introduction',
          component: Introduction,
          meta: {
            requiresAuth: true // 是否需要登录
          }
        },
        {
          path: '/Page',
          name: 'Page',
          component: Page,
          meta: {
            requiresAuth: true // 是否需要登录
          }
        }
      ]
    },
/*    {
      path: '/lock',
      name: 'lock',
      component: Lock
    },
*/
    {
    path: '*',
    name: 'E404',
    component: E404
  }
  ]
})
