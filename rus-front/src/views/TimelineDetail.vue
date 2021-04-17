<template>
  <v-container>
    <SideBar />
    <sequential-entrance fromBottom>
      <div class="analysis-header" style="text-align:center;">
        <img src="@/assets/img/analysis_logo.jpg" alt="" class="analysis-logo" />
        <div style="margin: 3vh 0 0 2vh; font-size: 2vh; font-style: Italic; font-weight: bold;">
          <p>선택하신 학습의 분석 내용이에요.</p>
          <p>얼마나 오랜 시간 집중하셨나요?</p>
        </div>
      </div>
      <PageTitle title="타임라인" :isBack="true" />
    </sequential-entrance>

    <sequential-entrance fromBottom>
      <v-card class="mt-2 mb-6 px-2 py-2" color="#D9E1E8" flat rounded="lg">
        <v-card-title class="headline">
          <span style="font-style: Italic; font-size: 2vh; font-weight: bold;"
            >{{ id }}번 학습 분석 내용입니다.</span
          >
          <span style="font-style: Italic; font-size: 1.5vh; margin-left: 1vw;"
            >({{ detailTitle }})</span
          >
        </v-card-title>
        <v-card-text class="pr-6 pt-6">
          <v-row v-if="activeData">
            <v-col md="5" sm="12">
              <PieChart :activeData="activeData" />
            </v-col>
            <v-col md="3" sm="6" v-if="activeData">
              <DetailTable :activeData="activeData" />
            </v-col>
            <v-col md="3" sm="6" v-if="activeData">
              <v-card flat rounded="lg" width="500" height="320">
                <v-card-title style="font-style: Italic; font-weight: bold;">
                  <span>활동 평가</span>
                </v-card-title>
                <v-divider></v-divider>
                <v-row class="mt-8">
                  <v-col cols="3" class="px-10">
                    <img
                      src="@/assets/img/good_logo.jpg"
                      alt=""
                      style="width: 7vh; border-radius: 70px;"
                    />
                  </v-col>
                  <v-col>
                    <SmallCard title="학습효율" :text="activeData.activePercent" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="3" class="px-10">
                    <img
                      src="@/assets/img/timeline_logo.jpg"
                      alt=""
                      style="width: 7vh; border-radius: 70px;"
                    />
                  </v-col>
                  <v-col>
                    <SmallCard title="학습평가" :text="activeData.activeRate" />
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <v-card class="px-2 pd-2 my-4" color="#D9E1E8" flat rounded="lg">
        <v-card-title class="headline">
          <span style="font-style: Italic; font-size: 2vh; font-weight: bold; margin: 1vh 0 0 0;"
            >얼마나 지속적으로 집중했는지 알아볼까요?</span
          >
        </v-card-title>
        <v-card-text>
          <StackedBarChart
            class="pr-4"
            v-if="activeDetailData"
            :activeDetailData="activeDetailData"
          />
          <v-row>
            <v-col cols="1" style="text-align: left">{{ start_time_text }}</v-col>
            <v-col> </v-col>
            <v-col cols="1" style="text-align: right">{{ end_time_text }}</v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </sequential-entrance>
  </v-container>
</template>
<script>
import axios from '@/http-common';
import moment from 'moment';
import SideBar from '@/components/mypage/SideBar.vue';
import PageTitle from '@/components/mypage/PageTitle';
import StackedBarChart from '@/components/mypage/timeline/StackedBarChart';
import PieChart from '@/components/mypage/timeline/PieChart';
import DetailTable from '@/components/mypage/timeline/DetailTable';
import SmallCard from '@/components/mypage/timeline/SmallCard';
export default {
  name: 'TimelineDetail',
  components: {
    SideBar,
    PageTitle,
    StackedBarChart,
    PieChart,
    DetailTable,
    SmallCard,
  },
  data() {
    return {
      id: this.$route.query.id,
      detailTitle: '',
      start_time_text: '',
      end_time_text: '',
      activeData: null,
      activeDetailData: null,
    };
  },
  created() {
    this.getActiveDetailData();
  },
  methods: {
    async getActiveDetailData() {
      const res = await axios.get('/actives/active/detail/' + this.id + '/');
      this.activeDetailData = res.data;
      await this.getDetailTitle(res.data);
      this.activeData = await this.getActiveData(res.data);
    },
    getDetailTitle(activeDetailData) {
      var startTime = activeDetailData[0].startTime;
      var endTime = activeDetailData[activeDetailData.length - 1].endTime;
      this.detailTitle = moment(startTime).format('YYYY년 MM월 DD일');
      this.start_time_text = moment(startTime).format('HH:mm:ss');
      this.end_time_text = moment(endTime).format('HH:mm:ss');
    },
    getActiveData(activeDetailData) {
      var studyTime = this.getActiveTimeByType(activeDetailData, 1);
      var restTime = this.getActiveTimeByType(activeDetailData, 0);
      var sleepTime = this.getActiveTimeByType(activeDetailData, 2);
      var emptyTime = this.getActiveTimeByType(activeDetailData, 3);
      var otherTime = this.getActiveTimeByType(activeDetailData, 4);
      var totalTime = studyTime + restTime + sleepTime + emptyTime + otherTime;
      var activePercent = this.getActivePercent(studyTime, totalTime);
      var activeRate = this.getActiveRate(activePercent);

      var activeData = {
        studyTime: studyTime,
        restTime: restTime,
        sleepTime: sleepTime,
        emptyTime: emptyTime,
        otherTime: otherTime,
        activePercent: activePercent + '%',
        activeRate: activeRate,
      };

      return activeData;
    },
    getActiveTimeByType(activeDetailData, type) {
      var activeTime = 0;
      for (let i = 0; i < activeDetailData.length; i++) {
        if (activeDetailData[i].active_type == type) {
          var startTime = activeDetailData[i].startTime;
          var endTime = activeDetailData[i].endTime;
          activeTime += this.getTimeDiff(startTime, endTime);
        }
      }
      return activeTime;
    },
    getTimeDiff(startTime, endTime) {
      var t1 = moment(startTime);
      var t2 = moment(endTime);
      var dt = t2.diff(t1) / 1000; // 초 단위
      var hours = dt / (60 * 60); // 시간 단위
      return hours;
    },
    getActivePercent(studyTime, totalTime) {
      var activePercent = (studyTime / totalTime) * 100;
      return Math.round(activePercent);
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
      } else {
        activeRate = 'E';
      }
      return activeRate;
    },
  },
};
</script>
<style scoped>
.analysis-header {
  display: flex;
  justify-content: center;
  margin: 1.5vh 0 0 0;
}

.analysis-logo {
  width: 13vh;
  height: 13vh;
  border-radius: 70px;
}
</style>
