<template>
  <div>
    <v-row>
      <v-col cols="3">
        <v-card color="#D9E1E8" rounded="lg" flat height="425" style="margin-top: -10px;">
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
        <v-card-text class="px-6" style="font-style: Italic;">
          <v-container></v-container>
          <v-container></v-container>
          <v-row>
            <v-col cols="3">
              <img src="@/assets/img/good_logo.jpg" alt="" style="width: 7vh; border-radius: 70px;">
            </v-col>
            <v-col cols="9">
              <Card title="그룹 대비 학습시간" :text="compareActiveTime()" />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="3">
              <img src="@/assets/img/active_logo.jpg" alt="" style="width: 7vh; border-radius: 70px;">
            </v-col>
            <v-col cols="9">
              <Card title="그룹 대비 집중도" :text="compareActivePercent()" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      </v-col>
      <v-col cols="9">
        <v-container style="margin-top: -54px">
          <v-card class="mt-8 px-2 py-2" flat color="#D9E1E8" rounded="lg">
            <v-card-title class="headline">
              <p style="font-style: Italic; font-size: 2vh; font-weight: bold;">선택한 그룹과 비교해 볼까요?</p>
            </v-card-title>
            <v-card-text>
              <BarChart :myActiveData="myActiveData" :groupActiveData="groupActiveData" />
            </v-card-text>
          </v-card>
        </v-container>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import BarChart from '@/components/mypage/analysis/BarChart';
import Card from '@/components/mypage/analysis/Card';
export default {
  name: 'SubAnalysisGroup',
  props: ['myActiveData', 'groupActiveData'],
  components: {
    BarChart,
    Card,
  },
  data() {
    return {};
  },
  created() {},
  methods: {
    compareActiveTime() {
      if (this.groupActiveData.length == 0) {
        return '-';
      } else if (this.myActiveData.studyTime >= this.groupActiveData.studyTime) {
        return '높음';
      } else {
        return '낮음';
      }
    },
    compareActivePercent() {
      if (this.groupActiveData.length == 0) {
        return '-';
      } else if (
        this.getActivePercent(this.myActiveData) >= this.getActivePercent(this.groupActiveData)
      ) {
        return '높음';
      } else {
        return '낮음';
      }
    },
    getTotalTime(activeData) {
      var totalTime = activeData.studyTime + activeData.restTime + activeData.otherTime;
      return totalTime;
    },
    getActivePercent(activeData) {
      var activePercent = (activeData.studyTime / this.getTotalTime(activeData)) * 100;
      return Math.round(activePercent);
    },
    prev() {
      this.$emit('prev-page');
    },
    next() {
      this.$emit('next-page');
    },
  },
};
</script>
