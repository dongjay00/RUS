<template>
  <v-data-iterator :items="items" hide-default-footer>
    <template v-slot:default="props">
      <v-row>
        <v-col v-for="item in props.items" :key="item.name">
          <v-card flat rounded="lg" style="font-style: Italic;">
            <v-card-title class="subheading font-weight-bold">
              {{ item.name }}
            </v-card-title>

            <v-divider></v-divider>

            <v-list>
              <v-list-item>
                <v-list-item-content>학습시간</v-list-item-content>
                <v-list-item-content class="align-end">
                  <span style="text-align: right; font-weight: bold;">{{ item.studyTime }}</span>
                </v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content>휴식시간</v-list-item-content>
                <v-list-item-content class="align-end">
                  <span style="text-align: right; font-weight: bold;">{{ item.restTime }}</span>
                </v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content>졸음시간</v-list-item-content>
                <v-list-item-content class="align-end">
                  <span style="text-align: right; font-weight: bold;">{{ item.sleepTime }}</span>
                </v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content>자리비움</v-list-item-content>
                <v-list-item-content class="align-end">
                  <span style="text-align: right; font-weight: bold;">{{ item.emptyTime }}</span>
                </v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content>딴짓시간</v-list-item-content>
                <v-list-item-content class="align-end">
                  <span style="text-align: right; font-weight: bold;">{{ item.otherTime }}</span>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-data-iterator>
</template>
<script>
export default {
  name: 'DetailTable',
  props: ['activeData'],
  data: () => ({
    items: null,
  }),
  created() {
    this.getTableData();
  },
  methods: {
    getTableData() {
      var items = [
        {
          name: '활동 분석',
          studyTime: this.getTimeString(this.activeData.studyTime),
          restTime: this.getTimeString(this.activeData.restTime),
          sleepTime: this.getTimeString(this.activeData.sleepTime),
          emptyTime: this.getTimeString(this.activeData.emptyTime),
          otherTime: this.getTimeString(this.activeData.otherTime),
        },
      ];
      this.items = items;
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
