<template>
  <div class="d-flex justify-center main my-10">
    <sequential-entrance fromBottom>
    <v-card elevation="2">
      <div class="d-flex justify-center align-center loginMainImage">
        <v-img src="@/assets/img/background_login.png"></v-img>
        <!-- <a href="http://www.freepik.com">Designed by stories / Freepik</a> -->

        <div class="mainName d-flex align-top">
          <div class="text-h1 font-weight-bold pr-5">RUS</div>
          <div class="caption font-weight-bold pt-3">
            <div>
              RUS를 카톡으로 간편 로그인하세요.
            </div>
            <div>
              로그인 후에 RUS의 모든 서비스를 이용할 수 있습니다.
            </div>
          </div>
        </div>
        <img
          class="loginBtn"
          @click="kakaoLogin"
          src="../assets/kakao_login_medium_wide.png"
          alt="kakaoLogin"
        />
      </div>
    </v-card>
    </sequential-entrance>
    <!-- </v-col -->
    <v-snackbar v-model="snackbar" timeout="2000">
      이미 로그인했습니다.

      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
          확인
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>
<script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
<script>
import axios from '@/http-common';

export default {
  data() {
    return {
      snackbar: false,
      email: '',
      nickname: '',
      profileImage: '',
      token: '',
      refresh: '',
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin;
    },
  },
  methods: {
    kakaoLogin() {
      var vm = this;
      if (this.isLogin == false) {
        Kakao.Auth.login({
          scope: 'profile, account_email, talk_message',
          success: function(authObj) {
            Kakao.Auth.setAccessToken(authObj['access_token']);
            Kakao.API.request({
              url: '/v2/user/me',
              success: (res) => {
                const kakao_account = res.kakao_account;
                vm.email = kakao_account['email'];
                vm.nickname = kakao_account['profile']['nickname'];
                if (kakao_account['profile']['profile_image_url']) {
                  vm.profileImage = kakao_account['profile']['profile_image_url'];
                }
                localStorage.setItem('refresh-token', authObj['refresh_token'])
                vm.token = authObj['access_token'];
                vm.refresh = authObj['refresh_token'];
                const user = {
                  email: vm.email,
                  nickname: vm.nickname,
                  profileImage: vm.profileImage,
                  token: vm.token,
                  refresh: vm.refresh,
                };

                vm.$store.dispatch('login', user);
                vm.$router.push('/about');
                axios.get(`/users/user/${user.email}/`).then((response) => {
                  if (response.data['user_pk'] == 'null') {
                    const userInfo = {
                      account_email: vm.email,
                      nickname: vm.nickname,
                      profile_img: vm.profileImage,
                    };
                    axios.post('/users/user/', userInfo).then(() => {
                      // 회원가입하는 코드
                    });
                  } else {
                    vm.$store.dispatch('saveUserPK', response.data['user_pk']);
                  }
                });
              },
              fail: (error) => {
                console.log(error);
              },
            });
          },
        });
      } else {
        this.$router.push('/about')
      }
    },
  },
};
</script>
<style scoped>
.main {
  position: relative;
}

.mainName {
  position: absolute;
  top: 10%;
  left: 10%;
}
.loginMainImage {
  position: relative;
  width: 1000px;
}
.loginCard {
  margin-top: 10%;
}
.loginBtn {
  cursor: pointer;
  position: absolute;
  bottom: 30%;
  /* border-radius */
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  /* box-shadow */
  -webkit-box-shadow: rgba(0, 0, 0, 0.8) 0px 0 10px;
  -moz-box-shadow: rgba(0, 0, 0, 0.8) 0 0 10px;
  box-shadow: rgba(0, 0, 0, 0.8) 0 0 10px;
}
.loginBtn:hover {
  -webkit-transform: scale(1.02);
  -moz-transform: scale(1.02);
  -ms-transform: scale(1.02);
  -o-transform: scale(1.02);
  transform: scale(1.02);
}
</style>
