// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


'use strict'
// Template version: 1.3.1
// see http://vuejs-templates.github.io/webpack for documentation.

const path = require('path');

var config = {
  dev: {

    // Paths
    assetsSubDirectory: 'static',
    /***
     * 添加服务器环境，就是用这个替换下面那一行assetsPublicPath: './',
     * */
    assetsPublicPath: '/',
    /***********over**********/

    proxyTable: {},

    // Various Dev Server settings
    host: 'localhost', // can be overwritten by process.env.HOST
    port: 8080, // can be overwritten by process.env.PORT, if port is in use, a free one will be determined
    autoOpenBrowser: false,
    errorOverlay: true,
    notifyOnErrors: true,
    poll: false, // https://webpack.js.org/configuration/dev-server/#devserver-watchoptions-
    env: require('./dev.env'),
 /*   baseServerUrl: 'http://gank.io',*/
    baseServerUrl: 'http://qizhi.pkuml.org',

    // Use Eslint Loader?
    // If true, your code will be linted during bundling and
    // linting errors and warnings will be shown in the console.
    useEslint: false,
    // If true, eslint errors and warnings will also be shown in the error overlay
    // in the browser.
    showEslintErrorsInOverlay: false,


    /**
     * Source Maps
     */

    // https://webpack.js.org/configuration/devtool/#development
    devtool: 'cheap-module-eval-source-map',

    // If you have problems debugging vue-files in devtools,
    // set this to false - it *may* help
    // https://vue-loader.vuejs.org/en/options.html#cachebusting
    cacheBusting: true,

    cssSourceMap: true
  },
  build: {
    // Template for index.html
    index: path.resolve(__dirname, '../dist/index.html'),

    // Paths
    assetsRoot: path.resolve(__dirname, '../dist'),
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    baseServerUrl: 'http://qizhi.pkuml.org',
    /**
     * Source Maps
     */

    productionSourceMap: true,
    // https://webpack.js.org/configuration/devtool/#production
    devtool: '#source-map',

    // Gzip off by default as many popular static hosts such as
    // Surge or Netlify already gzip all static assets for you.
    // Before setting to `true`, make sure to:
    // npm install --save-dev compression-webpack-plugin
    productionGzip: false,
    productionGzipExtensions: ['js', 'css'],

    // Run the build command with an extra argument to
    // View the bundle analyzer report after build finishes:
    // `npm run build --report`
    // Set to `true` or `false` to always turn it on or off
    bundleAnalyzerReport: process.env.npm_config_report
  },
  pai_clusterview:{
    url:'http://qizhi.pkuml.org:3000/dashboard/db/pai_clusterview'   //process.env
    // url:'112.31.12.175:8280/grafana/dashboard/db/pai_clusterview'
  },
}

// 需要代理的接口
var proxyList = [
  '/*/person/**/*'
]

const targetPath = config.build.baseServerUrl ;// 服务器的地址 可以使www.xx.com

for (let i = 0; i < proxyList.length; i++) {
  config.dev.proxyTable[proxyList[i]] = {
    target: targetPath,
    secure: false,
    changeOrigin: true
  }
}

// console.info(Object.keys(config.dev.proxyTable))
module.exports = config;
