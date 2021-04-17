<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title class="text-h6 grey lighten-2">
          학습결과
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row class="mx-auto mb-3"><StackedBar :activeResult="activeResult"/></v-row>
            <v-row>
              <v-col class="pb-0" cols="4">
                <v-chip class="mx-2 px-1" small label>
                  활동시간
                </v-chip>
                {{ activeResult.totalTime }}
              </v-col>
              <v-col class="pb-0" cols="4">
                <v-chip class="mx-2 px-1" small label>
                  학습시간
                </v-chip>
                {{ activeResult.studyTime }}
              </v-col>
              <v-col class="pb-0" cols="4">
                <v-chip class="mx-2 px-1" small label>
                  휴식시간
                </v-chip>
                {{ activeResult.restTime }}
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-chip class="mx-2 px-1" small label>
                  졸음시간
                </v-chip>
                {{ activeResult.sleepTime }}
              </v-col>
              <v-col cols="4">
                <v-chip class="mx-2 px-1" small label>
                  자리비움
                </v-chip>
                {{ activeResult.emptyTime }}
              </v-col>
              <v-col cols="4">
                <v-chip class="mx-2 px-1" small label>
                  딴짓시간
                </v-chip>
                {{ activeResult.otherTime }}
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#3C474D" dark @click="dialog = false">
            확인
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import moment from 'moment';
import StackedBar from '@/components/start/StackedBar';
export default {
  name: 'ResultModal',
  components: {
    StackedBar,
  },
  data() {
    return {
      dialog: false,
      activeResult: {
        studyTime: 0,
        restTime: 0,
        sleepTime: 0,
        emptyTime: 0,
        otherTime: 0,
        totalTime: 0,
      },
    };
  },
  created() {},
  methods: {
    openResultModal(activeData) {
      this.dialog = true;
      this.getModalData(activeData.active_details);
    },
    getModalData(activeDetailData) {
      var studyTime = this.getActiveTimeByType(activeDetailData, 1);
      var restTime = this.getActiveTimeByType(activeDetailData, 0);
      var sleepTime = this.getActiveTimeByType(activeDetailData, 2);
      var emptyTime = this.getActiveTimeByType(activeDetailData, 3);
      var otherTime = this.getActiveTimeByType(activeDetailData, 4);
      var totalTime = studyTime + restTime + sleepTime + emptyTime + otherTime;

      var activeResult = {
        studyTime: this.timeFormat(studyTime),
        restTime: this.timeFormat(restTime),
        sleepTime: this.timeFormat(sleepTime),
        emptyTime: this.timeFormat(emptyTime),
        otherTime: this.timeFormat(otherTime),
        totalTime: this.timeFormat(totalTime),
      };

      this.activeResult = activeResult;
    },
    getActiveTimeByType(activeDetailData, type) {
      var activeTime = 0;
      for (let i = 0; i < activeDetailData.length; i++) {
        if (activeDetailData[i].active_type == type) {
          var startTime = activeDetailData[i].start_time;
          var endTime = activeDetailData[i].end_time;
          activeTime += this.getTimeDiff(startTime, endTime);
        }
      }
      return activeTime;
    },
    getTimeDiff(startTime, endTime) {
      var t1 = moment(startTime);
      var t2 = moment(endTime);
      var dt = t2.diff(t1) / 1000; // 초 단위
      // var hours = dt / (60 * 60); // 시간 단위
      return dt;
    },
    timeFormat(time) {
      let formatString = '';
      if (time < 60) {
        formatString = time + 's';
      } else if (time < 3600) {
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        formatString = minutes + 'm ' + seconds + 's';
      } else if (time >= 36000) {
        let hours = (time / 3600).toFixed(1);
        formatString = hours + 'h';
      } else {
        let hours = Math.floor(time / 3600);
        let minutes = Math.floor((time % 3600) / 60);
        formatString = hours + 'h ' + minutes + 'm';
      }
      return formatString;
    },
  },
};
</script>
