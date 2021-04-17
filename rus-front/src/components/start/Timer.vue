<template>
  <v-card width="300" height="450" rounded="lg">
    <div>
      <h1 class="mb-1 pt-3" style="text-align:center; font-style: Italic;">
        {{ totalTimeString }}
      </h1>
    </div>

    <v-divider class="mx-4"></v-divider>

    <v-container style="text-align: center">
      <img v-if="getTimerStatus() == 0" height="200" src="@/assets/img/status_ready.png" />
      <img v-if="getTimerStatus() == 2" height="200" src="@/assets/img/status_rest.png" />
      <img
        v-if="getTimerStatus() == 1 && active_status == 1"
        height="200"
        src="@/assets/img/status_study.png"
      />
      <img
        v-if="getTimerStatus() == 1 && active_status == 2"
        height="200"
        src="@/assets/img/status_sleep.png"
      />
      <img
        v-if="getTimerStatus() == 1 && active_status == 3"
        height="200"
        src="@/assets/img/status_empty.png"
      />
      <img
        v-if="getTimerStatus() == 1 && active_status == 4"
        height="200"
        src="@/assets/img/status_other.png"
      />
    </v-container>

    <v-divider class="mx-4"></v-divider>

    <v-card-text>
      <v-btn
        v-if="getTimerStatus() == 0"
        class="my-1"
        width="268"
        color="#687B87"
        x-large
        dark
        @click="openTutorialDialog"
        depressed
      >
        <i class="far fa-question-circle"></i>
        <div>도움말</div>
      </v-btn>
      <v-btn
        v-if="getTimerStatus() == 0"
        class="my-3"
        width="268"
        color="#3C474D"
        dark
        x-large
        @click="startTimer"
        depressed
      >
        기록시작
      </v-btn>
      <v-btn
        v-if="getTimerStatus() == 1"
        class="my-1"
        width="268"
        x-large
        dark
        color="#687B87"
        @click="stopTimer"
        depressed
      >
        휴식타임
      </v-btn>
      <v-btn
        v-if="getTimerStatus() == 2"
        class="my-1"
        width="268"
        x-large
        dark
        color="#687B87"
        @click="startTimer"
        depressed
      >
        휴식 끝
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
        v-if="getTimerStatus() != 0"
        class="my-3"
        width="268"
        x-large
        color="#3C474D"
        dark
        @click="resetTimer"
        depressed
      >
        기록종료
      </v-btn>
    </v-card-text>
    <TutorialDialog ref="tutorialDialog" />
    <KakaoMessage ref="kakaoMessage" />
    <AudioAlarm ref="audioAlarm" />
    <AlarmModal ref="alarmModal" :status_stack="status_stack" @close-alarm="closeAlarm" />
  </v-card>
</template>
<script>
import TutorialDialog from '@/components/start/TutorialDialog';
import KakaoMessage from '@/components/start/KakaoMessage';
import AudioAlarm from '@/components/start/AudioAlarm';
import AlarmModal from '@/components/start/AlarmModal';
import moment from 'moment';
export default {
  name: 'Timer',
  components: {
    TutorialDialog,
    KakaoMessage,
    AudioAlarm,
    AlarmModal,
  },
  watch: {
    status_stack() {
      if (this.active_status == 2 && this.status_stack == 3 && !this.isAlarm) {
        this.$refs.audioAlarm.toggleSound();
        this.$refs.alarmModal.openAlarmModal(2);
        this.isAlarm = true;
      } else if (this.active_status == 4 && this.status_stack == 3 && !this.isAlarm) {
        this.$refs.audioAlarm.toggleSound();
        this.$refs.alarmModal.openAlarmModal(4);
        this.isAlarm = true;
      } else if (this.active_status == 3 && this.status_stack == 6) {
        this.$refs.kakaoMessage.sendKakaoMessage();
      }
    },
  },
  data() {
    return {
      title: 'Timer',
      timer: null,
      totalTime: 0,
      timeCount: 0, // timeCount=sendCount일때 이미지 전송
      sendCount: 10, // 이미지 보내는 간격
      active_status: 0,
      status_stack: 0,
      resetButton: false,
      activeTime: [0, 0, 0],
      activeDetailTime: 0,
      active_details: [],
      active_detail: {
        active_type: 0,
        start_time: '',
        end_time: '',
      },
      isAlarm: false,
    };
  },
  created() {
    this.resetTimer();
  },
  methods: {
    getTimerStatus() {
      var status = 0;
      if (this.timer != null) {
        status = 1; // 일시정지, 종료하기
      } else if (this.totalTime == 0) {
        status = 0; // 도움말, 시작하기
      } else {
        status = 2; // 일시정지 해제, 종료하기
      }
      return status;
    },
    openTutorialDialog() {
      this.$refs.tutorialDialog.openDialog();
    },
    startTimer() {
      this.$emit('start-video');

      this.timer = setInterval(() => this.addTime(), 1000);
      this.resetButton = true;
      this.changeActiveType(1);
    },
    stopTimer() {
      clearInterval(this.timer);
      this.timer = null;
      this.resetButton = true;
      this.changeActiveType(0);
    },
    resetTimer() {
      this.$emit('stop-video');

      if (this.totalTime > 0) {
        this.updateActiveDetail(this.getNowDateString());
        var len = this.active_details.length;
        var active = {
          user_pk: this.$store.state.user_pk,
          start_time: this.active_details[0].start_time,
          end_time: this.active_details[len - 1].end_time,
          active_details: this.active_details,
        };
        this.$emit('send-active', active);
      }
      this.totalTime = 0;
      this.timeCount = 0;
      clearInterval(this.timer);
      this.timer = null;
      this.active_status = 1;
      this.status_stack = 0;
      this.resetButton = false;
      this.active_details = [];
    },
    addTime() {
      this.totalTime++;
      this.addCount();
    },
    addCount() {
      this.timeCount++;
      if (this.timeCount >= this.sendCount) {
        this.$emit('send-image');
        this.timeCount = 0;
      }
    },
    clearStack() {
      this.status_stack = 0;
    },
    changeActiveType(type) {
      if (this.active_detail.active_type != type) {
        if (this.totalTime > 0) {
          this.updateActiveDetail(this.getNowDateString());
        }
        this.setActiveDetail(type, this.getNowDateString());
      }
      this.status_stack++;
    },
    setActiveDetail(type, start_time) {
      this.active_status = type;
      this.status_stack = 0;
      this.active_detail.active_type = type;
      this.active_detail.start_time = start_time;
    },
    updateActiveDetail(end_time) {
      this.active_detail.end_time = end_time;

      var type = this.active_detail.active_type;
      var start_time = this.active_detail.start_time;
      this.active_details.push({
        active_type: type,
        start_time: start_time,
        end_time: end_time,
      });
    },
    getNowDateString() {
      var dateString = moment().format('YYYY-MM-DD HH:mm:ss');
      return dateString;
    },
    getTimeString(time) {
      const hours = Math.floor(time / 3600);
      const minutes = Math.floor((time % 3600) / 60);
      const seconds = time - minutes * 60;
      return this.timeToString(hours, minutes, seconds);
    },
    timeToString(hour, minute, second) {
      // 12:34:56
      return this.padTime(hour) + ':' + this.padTime(minute) + ':' + this.padTime(second);
    },
    padTime(time) {
      // 1:2:3 => 01:02:03
      return (time < 10 ? '0' : '') + time;
    },
    closeAlarm() {
      if (this.isAlarm) {
        this.$refs.audioAlarm.toggleSound();
        this.isAlarm = false;
        this.clearStack();
      }
    },
  },
  // =======================
  computed: {
    totalTimeString() {
      return this.getTimeString(this.totalTime);
    },
  },
};
</script>
