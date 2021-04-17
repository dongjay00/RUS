<template>
  <v-container style="width: 1200px">
    <sequential-entrance fromBottom>
    <v-row class="d-flex justify-center" max-width="1000">
      <v-col cols="10">
        <v-card>
          <v-row class="d-flex flex-no-wrap justify-space-between">
            <v-col cols="6">
              <div class="d-flex justify-center my-10">
                <div class="text-h1 font-weight-bold">RUS</div>
                <div class="text-h4 font-weight-bold mt-11">를 소개합니다.</div>
              </div>
              <v-card class="mx-auto" color="#A3A19D" dark max-width="400">
                <v-card-text class="subtitle-1 font-weight-bold">
                  "아무리 약한 사람이라도 단 하나의 목적에 자신의 온 힘을 집중한다면 무엇인가 성취할
                  수 있지만 아무리 강한 사람이라도 힘을 많은 목적에 분산하면 어떤 것도 성취할 수
                  없다."
                </v-card-text>

                <v-card-actions>
                  <v-list-item class="grow">
                    <v-list-item-avatar color="grey darken-3">
                      <v-img
                        class="elevation-6"
                        alt=""
                        src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Montesquieu_1.png/260px-Montesquieu_1.png"
                      ></v-img>
                    </v-list-item-avatar>

                    <v-list-item-content>
                      <v-list-item-title>Charles de Montesquieu</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-card-actions>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-img src="@/assets/img/about_study.png"></v-img>
            </v-col>
          </v-row>

          <v-row class="d-flex flex-no-wrap justify-space-between">
            <v-col cols="6">
              <v-img src="@/assets/img/about_computer.png"></v-img>
            </v-col>
            <v-col cols="6">
              <v-card class="mx-auto" max-width="400" elevation="0">
                <v-card-text class="subtitle-1 font-weight-bold">
                  <v-badge left color="red" content="!">
                    <div
                      class="text-h6 font-weight-bold"
                      style="color: black; border-bottom: solid 3px black"
                    >
                      여러분의 공부 패턴은 어떤가요?
                    </div>
                  </v-badge>
                  <br />
                  <br />
                  <div>
                    제대로 집중하면 6시간 걸릴 일을 30분 안에 끝낼 수 있지만, 그렇지 못하면 30분만에
                    끝낼 일을 6시간을 해도 끝내지 못한다죠.
                  </div>
                  <br />
                  <br />
                  <div>
                    자리에 앉자마자 글씨가 어질어질해 자고 싶은 욕구, 넷상의 이야기가 궁금해 폰을
                    뒤적뒤적하고픈 욕구,
                  </div>
                  <br />
                  <br />
                  <div>
                    여러분은 잘 이겨내고 계신가요?
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-row class="d-flex flex-no-wrap justify-space-between">
            <v-col cols="6">
              <v-card class="mx-auto" max-width="400" elevation="0">
                <v-card-text class="subtitle-1 font-weight-bold">
                  <div>
                    RUS는 의지가 부족한 사람들을 위한 맞춤형 서비스입니다.
                  </div>
                  <br />
                  <div>
                    실시간 영상 분석을 통해 여러분의 행동을 체크하여 공부시간엔 공부에만 전념할 수
                    있도록 도와주고, 여러분의 공부 패턴을 기록하여 피드백을 제공합니다.
                  </div>
                  <br />
                  <div>
                    어떠신가요?
                  </div>
                  <br />
                  <div>
                    혼자서 몰입하기 어렵다면,
                  </div>
                  <div>
                    저희 RUS와 함께해보시는 건 어떨까요?
                  </div>
                  <br />
                  <router-link to="/" style="text-decoration: none;">
                    <v-btn
                      block
                      large
                      color="#4A4A48"
                      style="color: #FFFBF4;"
                      class="font-weight-bold"
                    >
                      지금 당장 출발하시죠!
                    </v-btn>
                  </router-link>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-img src="@/assets/img/about_think.png"></v-img>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    </sequential-entrance>
  </v-container>
</template>
<script>
export default {
  name: 'About',
};
</script>
<style scoped>
.part {
  margin: 20vh 0;
  font-size: 2vh;
  text-align: center;
}
.part2 {
  margin: 10vh 0;
  font-size: 2vh;
  text-align: center;
}
.part3 {
  margin: 10vh 0;
  font-size: 2vh;
  text-align: center;
}
</style>
