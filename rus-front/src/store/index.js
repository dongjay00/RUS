import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLogin: false,
    email: '',
    nickname: '',
    profileImage: null,
    token: '',
    user_pk: '',
    refresh: '',
  },
  getters: {
    isLogin: state => {
      return state.isLogin
    },
    email: state => {
      return state.email
    },
    nickname: state => {
      return state.nickname
    },
    profileImage: state => {
      return state.profileImage
    },
    token: state => {
      return state.token
    },
    user_pk: state => {
      return state.user_pk
    },
    refresh: state => {
      return state.refresh
    }
  },
  mutations: {
    LOGIN: function (state, user) {
      state.isLogin = true
      state.email = user.email
      state.nickname = user.nickname
      state.profileImage = user.profileImage
      state.token = user.token
      state.refresh = user.refresh
      localStorage.setItem('access-token', user.token)
    },
    LOGOUT: function (state) {
      state.isLogin = false
      state.email = ''
      state.nickname = ''
      state.profileImage = null
      state.token = ''
      state.refresh = ''
      state.user_pk = ''
      localStorage.removeItem('access-token')
    },
    SAVE_USER_PK: function (state, user_pk) {
      state.user_pk = user_pk;
    }
  },
  actions: {
    login: function ({ commit }, user) {
      commit('LOGIN', user)
    },
    logout: function ({ commit }) {
      commit('LOGOUT')
    },
    saveUserPK: function ({ commit }, user_pk) {
      commit('SAVE_USER_PK', user_pk)
    }
  },
  modules: {},
  plugins: [
    createPersistedState()
  ]
});
