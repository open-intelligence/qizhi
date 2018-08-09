// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


import Vue from 'vue'
import Vuex from 'vuex'
import app from './app'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app
  }
})

export default store
