<template>
  <v-card color="#D9E1E8" rounded="lg" flat>
    <v-card-title class="justify-center mb-4">
      <v-btn plain fab text small color="grey darken-2" @click="prev">
        <v-icon>
          mdi-chevron-left
        </v-icon>
      </v-btn>
      <span style="text-align:center; font-style: Italic;">{{ myActiveData.name }}</span>
      <v-btn plain fab text small color="grey darken-2" @click="next">
        <v-icon>
          mdi-chevron-right
        </v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text style="font-style: Italic;">
      <v-row>
        <v-col cols="3">
          <img src="@/assets/img/good_logo.jpg" alt="" style="width: 7vh; border-radius: 70px;" />
        </v-col>
        <v-col cols="9">
          <Card title="학습효율" :text="activePercent + '%'" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="3">
          <img
            src="@/assets/img/timeline_logo.jpg"
            alt=""
            style="width: 7vh; border-radius: 70px;"
          />
        </v-col>
        <v-col cols="9">
          <Card title="학습평가" :text="activeRate" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="3">
          <img src="@/assets/img/group_logo.jpg" alt="" style="width: 7vh; border-radius: 70px;" />
        </v-col>
        <v-col cols="9">
          <Card title="총 학습시간" :text="getTimeString(myActiveData.studyTime)" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="3">
          <img
            src="@/assets/img/analysis_logo.jpg"
            alt=""
            style="width: 7vh; border-radius: 70px;"
          />
        </v-col>
        <v-col cols="9">
          <Card title="총 휴식시간" :text="getTimeString(myActiveData.restTime)" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="3">
          <img src="@/assets/img/sleep_logo.jpg" alt="" style="width: 7vh; border-radius: 70px;" />
        </v-col>
        <v-col cols="9">
          <Card title="총 예외시간" :text="getTimeString(myActiveData.otherTime)" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="3">
          <img src="@/assets/img/active_logo.jpg" alt="" style="width: 7vh; border-radius: 70px;" />
        </v-col>
        <v-col cols="9">
          <Card title="총 활동시간" :text="getTimeString(totalTime)" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
<script>
import Card from '@/components/mypage/analysis/Card';
export default {
  name: 'SubAnalysis',
  props: ['myActiveData'],
  components: {
    Card,
  },
  watch: {
    async myActiveData() {
      await this.getTotalTime(this.myActiveData);
      await this.getActivePercent(this.myActiveData);
    },
  },
  data() {
    return {
      totalTime: 0,
      activePercent: 0,
      activeRate: '',
    };
  },
  async created() {
    await this.getTotalTime(this.myActiveData);
    await this.getActivePercent(this.myActiveData);
  },
  methods: {
    getTotalTime(activeData) {
      var totalTime = activeData.studyTime + activeData.restTime + activeData.otherTime;
      this.totalTime = totalTime;
    },
    getActivePercent(activeData) {
      var activePercent = 0;
      var totalTime = this.totalTime;
      if (totalTime > 0) {
        activePercent = (activeData.studyTime / totalTime) * 100;
      } else {
        activePercent = 0;
      }
      activePercent = Math.round(activePercent);
      this.activePercent = activePercent;
      this.getActiveRate(activePercent);
    },
    getActiveRate(activePercent) {
      var activeRate = '';
      if (activePercent > 90) {
        activeRate = 'A';
      } else if (activePercent > 80) {
        activeRate = 'B';
      } else if (activePercent > 70) {
        activeRate = 'C';
      } else if (activePercent > 60) {
        activeRate = 'D';
      } else if (activePercent == 0) {
        activeRate = '-';
      } else {
        activeRate = 'E';
      }
      this.activeRate = activeRate;
    },
    prev() {
      this.$emit('prev-page');
    },
    next() {
      this.$emit('next-page');
    },
    getTimeString(time) {
      var cardString = '';
      if (time > 100) {
        cardString = time.toFixed(1) + '시간';
      } else if (time < 1 && time > 0) {
        let minutes = (time * 60).toFixed(0);
        let seconds = (time * 3600 - minutes * 60).toFixed(0);
        cardString = this.padTime(minutes) + '분 ' + this.padTime(seconds) + '초';
      } else {
        let hours = Math.floor(time);
        let minutes = ((time * 60) % 60).toFixed(0);
        cardString = hours + '시간 ' + this.padTime(minutes) + '분 ';
      }
      return cardString;
    },
    padTime(time) {
      // 1:2:3 => 01:02:03
      return (time < 10 ? '0' : '') + time;
    },
  },
};
</script>
