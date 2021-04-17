<template>
  <div>
    <SideBar />
    <v-container></v-container>
    <sequential-entrance fromBottom>
    <div class="timeline-header" style="text-align:center;">
      <img src="@/assets/img/timeline_logo.jpg" alt="" class="timeline-logo">
      <div style="margin: 3vh 0 0 2vh; font-size: 2vh; font-style: Italic; font-weight: bold;">
        <p>여러분의 학습 내역을 확인하세요.</p>
        <p>과거의 나는 어땠을까요?</p>
      </div>
    </div>
    </sequential-entrance>
    <v-container my-2></v-container>
    <sequential-entrance fromBottom>
    <v-card
      class="calender"
      max-height="500"
      max-width="1620"
      rounded="lg"
    >
      <Calendar v-if="activeListData" :activeListData="activeListData" />
    </v-card>
    </sequential-entrance>
  </div>
</template>
<script>
import axios from '@/http-common';
import { mapGetters } from 'vuex';
import SideBar from '@/components/mypage/SideBar';
import Calendar from '@/components/mypage/timeline/Calendar';
export default {
  name: 'Timeline',
  components: {
    SideBar,
    Calendar,
  },
  computed: {
    ...mapGetters(['user_pk']),
  },
  data() {
    return {
      activeListData: null,
    };
  },
  created() {
    this.getActiveListData();
  },
  methods: {
    async getActiveListData() {
      const res = await axios.get('/actives/active/timeline/' + this.user_pk + '/');
      this.activeListData = res.data;
    },
  },
};
</script>
<style scoped>
.calender {
  margin: 0 auto;
}

.timeline-header {
  display: flex;
  justify-content: center;
}

.timeline-logo {
  width: 13vh;
  height: 13vh;
  border-radius: 70px;
}
</style>
