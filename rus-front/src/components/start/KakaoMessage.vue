<template>
  <div></div>
</template>
<script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
<script>
import axios from 'axios';

export default {
  name: 'KakaoMessage',
  computed: {
    refresh() {
      return this.$store.getters.refresh;
    },
  },
  methods: {
    sendKakaoMessage() {
      Kakao.API.request({
        url: '/v2/api/talk/memo/default/send',
        data: {
          template_object: {
            object_type: 'feed',
            content: {
              title: 'Johnny 알리미',
              description: '언제까지 자리를 비울 생각이신가요?',
              image_url:
                'https://rus-image.s3.ap-northeast-2.amazonaws.com/2021-04-0713:15:07.818722.jpeg',
              link: {
                web_url: 'https://j4b102.p.ssafy.io/kakaourlpage',
                mobile_web_url: 'https://j4b102.p.ssafy.io/kakaourlpage',
              },
            },
            button_title: '바로 확인',
          },
        },
        success: function() {
        },
        fail: function(error) {
          console.log(error);
          const clientId = process.env.VUE_APP_CLIENT_ID;
          axios
            .post(
              `https://kauth.kakao.com/oauth/token?grant_type=refresh_token&client_id=${clientId}&refresh_token=${this.refresh}`
            )
            .then((response) => {
              sessionStorage.setItem('access-token', response.data.access_token);
              Kakao.Auth.setAccessToken(response.data.access_token);

              this.sendKakaoMessage();
            })
            .catch(() => {
              //재로그인 필요한 경우
              this.$router.push('/login');
              this.$store.dispatch('logout');
            });
        },
      });
    },
  },
};
</script>
