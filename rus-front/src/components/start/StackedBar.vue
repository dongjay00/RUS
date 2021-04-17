<template>
  <div id="chart">
    <apexchart
      type="bar"
      height="100"
      width="400"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>
<script>
import VueApexCharts from 'vue-apexcharts';
export default {
  name: 'StackedBar',
  props: ['activeResult'],
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: null,
      chartOptions: {
        chart: {
          toolbar: {
            show: false, // 햄버거 버튼 지우기
          },
          stacked: true,
          stackType: '100%',
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0'],
        grid: {
          show: false,
        },
        xaxis: {
          labels: {
            show: false,
          },
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
        },
        yaxis: {
          labels: {
            show: false,
          },
          axisBorder: {
            show: false,
          },
        },
        fill: {
          opacity: 1,
        },
        tooltip: {
          y: {
            formatter(val) {
              let formatString = '';
              if (val < 60) {
                formatString = val + 's';
              } else if (val < 3600) {
                let minutes = Math.floor(val / 60);
                let seconds = val % 60;
                formatString = minutes + 'm ' + seconds + 's';
              } else if (val >= 36000) {
                let hours = (val / 3600).toFixed(1);
                formatString = hours + 'h';
              } else {
                let hours = Math.floor(val / 3600);
                let minutes = Math.floor((val % 3600) / 60);
                formatString = hours + 'h ' + minutes + 'm';
              }
              return formatString;
            },
          },
        },
      },
    };
  },
  created() {
    this.getChartData();
  },
  methods: {
    getChartData() {
      var series = [];

      var studyTime = this.changeToArray(this.activeResult.studyTime);
      var restTime = this.changeToArray(this.activeResult.restTime);
      var sleepTime = this.changeToArray(this.activeResult.sleepTime);
      var emptyTime = this.changeToArray(this.activeResult.emptyTime);
      var otherTime = this.changeToArray(this.activeResult.otherTime);

      series.push({ name: '학습', data: studyTime });
      series.push({ name: '휴식', data: restTime });
      series.push({ name: '졸음', data: sleepTime });
      series.push({ name: '자리비움', data: emptyTime });
      series.push({ name: '딴짓', data: otherTime });

      this.series = series;
    },
    changeToArray(singleData) {
      var arrayData = [];
      arrayData.push(singleData);
      return arrayData;
    },
  },
};
</script>
