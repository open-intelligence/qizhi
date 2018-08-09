// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


const menu = [
  {
    path: '/index',
    name: 'index',
    icon: 'icon-dynamic_fill',
    level: 1,
    sort: 1,
    children: [],
    fixed: false
  },
  {
    level: 1,
    path: '/Submit',
    children: [],
    fixed: false,
    name: 'Submit Job'
  },
  {
    path: '/jobs',
    name: 'jobs',
    level: 1,
    children: [],
    fixed: false
  },
  {
    path: '/clusters',
    name: 'Virtual Clusters',
    level: 1,
    children: [],
    fixed: false
  },
  {
    path: '/Page',
    name: 'Page',
    level: 1,
    children: [],
    fixed: false
  },
  {
    path: '/',
    name: 'Documentation',
    level: 0,
    icon: 'icon-manage_fill',
    fixed: false,
    children: [
      // {
      //   level: 1,
      //   path: '/Submit',
      //   children: [],
      //   fixed: false,
      //   name: 'Submit Job'
      // },
      // {
      //   level: 1,
      //   path: '/Download',
      //   children: [],
      //   fixed: false,
      //   name: 'Download'
      // },
      // {
      //   level: 1,
      //   path: '/notFound',
      //   children: [],
      //   fixed: false,
      //   name: 'notFound'
      // },
      {
        level: 1,
        path: '/Introduction',
        children: [],
        fixed: false,
        name: 'Introduction'
      }
    ]
  },
]

export default menu
