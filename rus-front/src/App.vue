<template>
  <v-app id="app" data-app>
    <Header v-if="!isDummy" />
    <v-main id="main">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
<script>
import Header from '@/components/common/Header.vue';

export default {
  name: 'App',
  components: {
    Header,
  },
  data: () => ({
    isDummy: false,
  }),
  created() {
    if (document.location.pathname === '/kakaourlpage') {
      this.isDummy = true;
    }

    // SDK를 초기화 합니다. 사용할 앱의 JavaScript 키를 설정해 주세요.
    const JAVASCRIPT_KEY = process.env.VUE_APP_JAVASCRIPT_KEY
    Kakao.init(JAVASCRIPT_KEY);


    // SDK 초기화 여부를 판단합니다.
    Kakao.isInitialized();
  },
};
</script>
<style>
#app {
  background-color: #f2f2f2;
  background-repeat: repeat;
}
</style>
