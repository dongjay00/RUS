<template>
  <v-dialog v-model="dialog" max-width="650" overlay-opacity="0.8">
    <v-stepper v-model="e1">
      <v-stepper-header style="background-color: rgba(0, 0, 0, 0.12);">
        <v-stepper-step color="#4A4A48" step="1">
          학습기록
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step color="#4A4A48" step="2">
          휴식타임
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step color="#4A4A48" step="3">
          경고알림
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step color="#4A4A48" step="4">
          마이페이지
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-row>
            <v-col cols="4" align-self="center">
              <v-img src="@/assets/img/tutorial_1.png" width="200"></v-img>
            </v-col>
            <v-col cols="8">
              <v-card-text style="text-align: center;">
                <div
                  class="text-h7 font-weight-bold"
                  style="color: black; border-bottom: solid 3px black; display: inline;"
                >
                  <i class="fas fa-clipboard-list"></i>
                  회원님의 학습을 기록하세요!
                </div>
                <div class="text-caption">
                  <br />
                  <br />
                  <p>RUS는 실시간 영상 분석 서비스입니다.</p>
                  <p>영상이 기록되는 동안 회원님의 학습태도가 어떠한지</p>
                  <p>실시간 감독 및 기록을 통한 분석을 받을 수 있습니다.</p>
                  <p>사용법은 아주 간단합니다.</p>
                  <div class="d-flex justify-center align-baseline">
                    <p>그저</p>
                    <v-chip class="mx-2" label dark small color="#4A4A48">
                      기록시작
                    </v-chip>
                    <p>버튼을 누른 후</p>
                    <p class="ml-1">학습에 집중하시면 됩니다.</p>
                  </div>
                </div>
              </v-card-text>
            </v-col>
          </v-row>
          <div class="d-flex justify-center mt-4">
            <v-btn class="mx-1" text dense @click="e1 = 2">
              <i class="fas fa-arrow-alt-circle-right fa-2x"></i>
            </v-btn>
          </div>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-row>
            <v-col cols="6">
              <v-card-text style="text-align: center;">
                <br />
                <div
                  class="text-h7 font-weight-bold"
                  style="color: black; border-bottom: solid 3px black; display: inline;"
                >
                  <i class="fas fa-coffee"></i>
                  휴식도 잊지 마세요!
                </div>
                <div class="text-caption">
                  <br />
                  <br />
                  <p>너무 오랜 시간 한 일에 집중한다면</p>
                  <p>피로가 쌓여 건강이 나빠질 우려가 있습니다.</p>
                  <p>적절한 휴식은 학습의 질을 향상시킵니다.</p>
                  <div class="d-flex justify-center align-baseline">
                    <p>쉬고 싶을 때는</p>
                    <v-chip class="mx-2" label small outlined color="#4A4A48">
                      휴식타임
                    </v-chip>
                    <p>을 클릭하세요!</p>
                  </div>
                </div>
              </v-card-text>
            </v-col>
            <v-col cols="3" class="pr-0" align-self="center">
              <v-img src="@/assets/img/tutorial_2.png"></v-img>
            </v-col>

            <v-col class="pl-0" cols="3" align-self="center">
              <v-img src="@/assets/img/tutorial_3.png"></v-img>
            </v-col>
          </v-row>
          <div class="d-flex justify-center mt-4">
            <v-btn class="mx-1" text dense @click="e1 = 1">
              <i class="fas fa-arrow-alt-circle-left fa-2x"></i>
            </v-btn>
            <v-btn class="mx-1" text dense @click="e1 = 3">
              <i class="fas fa-arrow-alt-circle-right fa-2x"></i>
            </v-btn>
          </div>
        </v-stepper-content>

        <v-stepper-content step="3">
          <v-row>
            <v-col cols="6" align-self="center">
              <v-img src="@/assets/img/tutorial_5.png"></v-img>
            </v-col>

            <v-col cols="6">
              <br />
              <v-card-text style="text-align: center;">
                <div
                  class="text-h7 font-weight-bold"
                  style="color: black; border-bottom: solid 3px black; display: inline;"
                >
                  <i class="fas fa-surprise"></i>
                  잠깐! 지금 뭘 하고 계신거죠?
                </div>
                <div class="text-caption">
                  <br />
                  <br />
                  <p>지금 또 핸드폰을 만지작 거리고 계신건가요?</p>
                  <p>지금 또 고개를 숙이고 눈을 감으실건가요?</p>
                  <p>어서 다시 학습에 집중하세요!</p>
                </div>
              </v-card-text>
            </v-col>
          </v-row>

          <div class="d-flex justify-center mt-4">
            <v-btn class="mx-1" text dense @click="e1 = 2">
              <i class="fas fa-arrow-alt-circle-left fa-2x"></i>
            </v-btn>
            <v-btn class="mx-1" text dense @click="e1 = 4">
              <i class="fas fa-arrow-alt-circle-right fa-2x"></i>
            </v-btn>
          </div>
        </v-stepper-content>

        <v-stepper-content step="4">
          <v-row>
            <v-col cols="8">
              <v-card-text style="text-align: center;">
                <br />
                <div
                  class="text-h7 font-weight-bold"
                  style="color: black; border-bottom: solid 3px black; display: inline;"
                >
                  <i class="fas fa-signal"></i>
                  나의 기록을 확인하세요!
                </div>
                <div class="text-caption">
                  <br />
                  <br />
                  <p>과거 학습태도가 어땠는지 궁금한가요?</p>
                  <div class="d-flex justify-center align-baseline">
                    <p>메뉴에서</p>
                    <v-chip class="mx-2" label small dark color="#4A4A48">
                      마이페이지
                    </v-chip>
                    <p>를 클릭하면</p>
                  </div>
                  <p>다양한 방법으로 과거 학습기록을 분석할 수 있습니다.</p>
                  <p>더 자세한 분석을 원한다면 지금 바로 시작하세요!</p>
                </div>
              </v-card-text>
            </v-col>

            <v-col cols="4" align-self="center">
              <v-img src="@/assets/img/tutorial_6.png"></v-img>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="5"></v-col>
            <v-col>
              <v-btn class="mx-1" text dense @click="e1 = 3">
                <i class="fas fa-arrow-alt-circle-left fa-2x"></i>
              </v-btn>
            </v-col>
            <v-col cols="3"></v-col>
            <v-col>
              <v-btn class="mx-1" color="#3C474D" dark @click="dialog = false" depressed>
                닫기
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-dialog>
</template>
<script>
export default {
  name: 'TutorialDialog',
  data: () => ({
    e1: 1,
    dialog: false,
  }),
  methods: {
    openDialog() {
      this.e1 = 1;
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
  },
};
</script>
