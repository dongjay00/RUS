<template>
  <div>
    <SideBar />
    <v-container></v-container>
    <sequential-entrance fromBottom>
    <div class="analysis-header" style="text-align:center;">
      <img src="@/assets/img/analysis_logo.jpg" alt="" class="analysis-logo">
      <div style="margin: 3vh 0 0 2vh; font-size: 2vh; font-style: Italic; font-weight: bold;">
        <p>일정 기간 동안의 여러분의 학습을 돌아보세요.</p>
        <p>얼마나 많은 발전이 있었나요?</p>
      </div>
    </div>
    </sequential-entrance>
    <v-container my-2></v-container>
    <sequential-entrance fromBottom>
    <v-card
      class="analysis"
      max-height="500"
      max-width="1600"
      rounded="lg"
      flat
    >
      <v-tabs dark class="mr-10 mb-10" background-color="#3C474D">
        <v-tab @click="changeTab">내 활동</v-tab>
        <v-tab @click="changeTab">그룹</v-tab>

        <!-- 내 활동 분석 -->
        <v-tab-item style="background-color: white;">
          
          <v-row>
            <v-col cols="3">
              <v-container style="margin-top: 13px">
              <SubAnalysis
                v-if="myActiveData"
                :myActiveData="myActiveData"
                @prev-page="prevPage"
                @next-page="nextPage"
              />
              </v-container>
            </v-col>
            <v-col cols="9">
              <v-container style="margin-top: -20px;">
                <v-card class="mt-8 px-2 py-2" flat color="#D9E1E8" rounded="lg">
                  <v-card-title class="headline">
                    
                    <v-container>
          <v-row>
            <v-col cols="10">
              <p style="font-style: Italic; font-size: 2vh; font-weight: bold;">선택한 구간을 차트로 확인해볼까요?</p>
            </v-col>
            <v-col cols="2"
              ><v-select
                v-model="selectedDate"
                :items="dateSelectItems"
                item-text="name"
                item-value="type"
                label="기간 선택"
                @change="getPageData"
                solo
                flat
              ></v-select
            ></v-col>
          </v-row>
          </v-container>
                  </v-card-title>
                  <v-card-text>
                    <ColumnChart v-if="analysisData" :analysisData="analysisData" />
                  </v-card-text>
                </v-card>
              </v-container>
            </v-col>
          </v-row>
        </v-tab-item>

        <!-- 그룹 분석 -->
        <v-tab-item style="background-color: white;">
          <v-container>
          <v-row>
            <v-col>
            </v-col>
            <v-col cols="2"
              ><v-select
                style="position: absolute; z-index: 2; width: 250px; max-width: 70%;"
                class="mt-10"
                v-model="selectedGroup"
                :items="myGroupListData"
                item-text="name"
                item-value="member"
                label="그룹 선택"
                @change="getGroupActiveData"
                solo
                flat
              ></v-select
            ></v-col>
            <v-col cols="2"
              ><v-select
                style="position: absolute; z-index: 2;"
                class="mt-10 mr-15"
                v-model="selectedDate"
                :items="dateSelectItems"
                item-text="name"
                item-value="type"
                label="기간 선택"
                @change="getPageData"
                solo
                flat
              ></v-select
            ></v-col>
          </v-row>
          </v-container>
          <v-container>
            <SubAnalysisGroup
              :myActiveData="myActiveData"
              :groupActiveData="groupActiveData"
              @prev-page="prevPage"
              @next-page="nextPage"
            />
          </v-container>
        </v-tab-item>
      </v-tabs>
    </v-card>
    </sequential-entrance>
  </div>
</template>
<script>
import axios from '@/http-common';
import { mapGetters } from 'vuex';
import moment from 'moment';
import SideBar from '@/components/mypage/SideBar.vue';
import SubAnalysis from '@/components/mypage/analysis/SubAnalysis';
import SubAnalysisGroup from '@/components/mypage/analysis/SubAnalysisGroup';
import ColumnChart from '@/components/mypage/analysis/ColumnChart';
import dateSelectItemsData from '@/assets/data/dateSelectItemsData';
export default {
  name: 'Analysis',
  components: {
    SideBar,
    SubAnalysis,
    SubAnalysisGroup,
    ColumnChart,
  },
  computed: {
    ...mapGetters(['user_pk']),
  },
  watch: {
    nowDate() {
      this.getPageData();
    },
  },
  data() {
    return {
      selectedDate: 'week',
      dateSelectItems: dateSelectItemsData.dateSelectItems,
      selectedGroup: null,
      myGroupListData: null,
      analysisData: null,
      myActiveData: null,
      groupActiveData: null,
      nowDate: moment().format('YYYY-MM-DD'),
    };
  },
  created() {
    this.getPageData();
  },
  methods: {
    changeTab() {
      this.getPageData();
    },
    getPageUrl(user_pk) {
      var start_date = this.getStartDate();
      var end_date = this.getEndDate();
      var url = user_pk + '/' + this.selectedDate + '/' + start_date + '/' + end_date + '/';

      return url;
    },
    async getPageData() {
      this.analysisData = null;
      this.analysisData = await this.getAnalysisData(this.user_pk);
      this.myActiveData = await this.getActiveData(this.analysisData);
      await this.getMyGroupListData();
    },
    async getAnalysisData(user_pk) {
      const res = await axios.get('/actives/active/analysis/' + this.getPageUrl(user_pk));

      return res.data;
    },
    async getMyGroupListData() {
      const res = await axios.get('/users/group/my/' + this.user_pk + '/');

      this.myGroupListData = res.data;
      await this.getGroupActiveData();
    },
    async getGroupActiveData() {
      if (this.selectedGroup == null) {
        this.groupActiveData = [];
        return;
      }

      var groupMembersData = this.selectedGroup;

      var studyTime = 0;
      var restTime = 0;
      var otherTime = 0;

      for (let i = 0; i < groupMembersData.length; i++) {
        var user_pk = groupMembersData[i];
        var analysisData = await this.getAnalysisData(user_pk);
        var activeData = await this.getActiveData(analysisData);
        studyTime += activeData.studyTime;
        restTime += activeData.restTime;
        otherTime += activeData.otherTime;
      }

      var groupActiveData = {
        studyTime: studyTime / groupMembersData.length,
        restTime: restTime / groupMembersData.length,
        otherTime: otherTime / groupMembersData.length,
      };
      this.groupActiveData = groupActiveData;
    },
    getActiveData(analysisData) {
      var name = this.getStartDate() + ' ~ ' + this.getEndDate();
      var studyTime = 0;
      var restTime = 0;
      var otherTime = 0;

      for (let i = 0; i < analysisData.length; i++) {
        studyTime += analysisData[i].studyTime;
        restTime += analysisData[i].restTime;
        otherTime += analysisData[i].otherTime;
      }

      var activeData = {
        name: name,
        studyTime: studyTime,
        restTime: restTime,
        otherTime: otherTime,
      };

      return activeData;
    },
    prevPage() {
      var nowDate = this.nowDate;
      this.nowDate = moment(nowDate)
        .add(-1, this.selectedDate)
        .format('YYYY-MM-DD');
    },
    nextPage() {
      var nowDate = this.nowDate;
      this.nowDate = moment(nowDate)
        .add(1, this.selectedDate)
        .format('YYYY-MM-DD');
    },
    getStartDate() {
      var start_date = '';
      if (this.selectedDate == 'day') {
        start_date = this.nowDate;
      } else if (this.selectedDate == 'week') {
        start_date = moment(this.nowDate)
          .add(-6, 'd')
          .format('YYYY-MM-DD');
      } else if (this.selectedDate == 'month') {
        start_date = moment(this.nowDate)
          .startOf('month')
          .format('YYYY-MM-DD');
      } else {
        start_date = moment(this.nowDate)
          .startOf('year')
          .format('YYYY-MM-DD');
      }
      return start_date;
    },
    getEndDate() {
      var end_date = '';
      if (this.selectedDate == 'day') {
        end_date = this.nowDate;
      } else if (this.selectedDate == 'week') {
        end_date = this.nowDate;
      } else if (this.selectedDate == 'month') {
        end_date = moment(this.nowDate)
          .endOf('month')
          .format('YYYY-MM-DD');
      } else {
        end_date = moment(this.nowDate)
          .endOf('year')
          .format('YYYY-MM-DD');
      }
      return end_date;
    },
  },
};
</script>
<style scoped>
/* .theme--light.v-tabs > .v-tabs-bar {
  background-color: #fff3e0;
}
.theme--light.v-tabs-items {
  background-color: #fff3e0;
} */
.analysis {
  margin: 0 auto;
}

.analysis-header {
  display: flex;
  justify-content: center;
}

.analysis-logo {
  width: 13vh;
  height: 13vh;
  border-radius: 70px;
}
</style>
