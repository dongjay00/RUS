<template>
  <v-app-bar app dark clipped-left>
    <div class="d-flex align-center">
      <router-link to="/" class="linkStyle">
        <v-btn text>
          <i class="fas fa-eye fa-2x mr-2 headerTextColor headerTextColor"></i>
          <span class="text-h5 font-weight-black headerTextColor">RUS</span>
        </v-btn>
        <span style="margin-left: 0.5vw; font-style: Italic; font-size: 1.2vh; color: #f2f2f2;">aRe yoU Sleeping?</span>
      </router-link>
    </div>

    <v-spacer></v-spacer>

    <router-link to="/about" class="linkStyle">
      <v-btn text>
        <i class="fas fa-info-circle"></i>
        <span class="ml-1 mr-2 headerTextColor">RUS소개</span>
      </v-btn>
    </router-link>

    <router-link v-if="isLogin == true" to="/" class="linkStyle">
      <v-btn text>
        <i class="fas fa-desktop"></i>
        <span class="ml-1 mr-2 headerTextColor">학습하기</span>
      </v-btn>
    </router-link>

    <router-link v-if="isLogin == true" to="/mypage/timeline" class="linkStyle">
      <v-btn text>
        <i class="fas fa-user-circle"></i>
        <span class="ml-1 mr-2 headerTextColor">마이페이지</span>
      </v-btn>
    </router-link>

    <router-link v-if="isLogin == false" to="/login" class="linkStyle">
      <v-btn text>
        <i class="fas fa-sign-in-alt"></i>
        <span class="ml-1 mr-2 headerTextColor">로그인</span>
      </v-btn>
    </router-link>

    <v-btn v-if="isLogin == true" text>
      <i class="fas fa-sign-out-alt"></i>
      <span class="ml-1 mr-2 headerTextColor" @click="logout">로그아웃</span>
    </v-btn>
  </v-app-bar>
</template>
<script src="https://developers.kakao.com/sdk/js/kakao.js"></script>

<script>
export default {
  name: 'Header',
  components: {},
  data() {
    return {};
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin;
    },
    token() {
      return this.$store.getters.token;
    },
  },
  methods: {
    onClick(e, item) {
      e.stopPropagation();

      if (item.to || !item.href) return;

      this.$vuetify.goTo(item.href);
    },
    scrollToTop() {
      window.scrollTo(0, 0);
    },
    logout() {
      if (!Kakao.Auth.getAccessToken()) {
        return;
      }
      var vm = this;

      Kakao.API.request({
        url: '/v1/user/unlink',
        success: function(response) {
          vm.$router.push('/login');
          vm.$store.dispatch('logout');
          // unlink 이후 이전 토큰이 남아있지만 만료처리된 토큰이라 상관없음
          // 재로그인하면 토근 재발급됨
        },
        fail: function() {
          vm.$router.push('/login');
          vm.$store.dispatch('logout');
        },
      });
    },
  },
};
</script>
<style scoped>
.headerTextColor {
  color: #f2f2f2;
}
.linkStyle {
  text-decoration: none;
}
</style>
