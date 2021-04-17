<template>
  <div v-if="series != null" id="chart">
    <apexchart type="bar" height="130" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
<script>
import VueApexCharts from 'vue-apexcharts';
import moment from 'moment';
export default {
  name: 'StackedBarChart',
  props: ['activeDetailData'],
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          type: 'bar',
          height: 200,
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
        grid: {
          show: false,
        },
        xaxis: {
          labels: {
            show: false,
          },
          axisBorder: {
            show: false, // 왼쪽 테두리 지우기
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
        tooltip: {
          y: {
            formatter(val) {
              let formatString = '';
              let hours = val / 3600;
              if (hours % 1 == 0) {
                formatString = hours + 'h';
              } else if (hours < 0.1) {
                let minutes = hours * 60;
                formatString = minutes.toFixed(0) + 'm';
              } else {
                formatString = hours.toFixed(1) + ' h';
              }
              return formatString;
            },
          },
        },
        fill: {
          opacity: 1,
        },
        legend: {
          show: false, // 범례 감추기
        },
      },
    };
  },
  created() {
    this.getChartData(this.activeDetailData);
  },
  methods: {
    getChartData(activeDetailData) {
      var series = [];
      var colors = [];
      var charColors = ['#00E396', '#008FFB', '#FEB019', '#FF4560', '#775DD0']; // 5개 색상 필요함

      for (let i = 0; i < activeDetailData.length; i++) {
        var type = activeDetailData[i].active_type;
        var startTime = activeDetailData[i].startTime;
        var endTime = activeDetailData[i].endTime;
        var dt = this.getTimeDiff(startTime, endTime);
        var timeData = [];
        timeData.push(dt);
        series.push({ name: 'a', data: timeData });
        colors.push(charColors[type]);
      }

      this.series = series;
      this.chartOptions.colors = colors;
    },
    getTimeDiff(startTime, endTime) {
      var t1 = moment(startTime);
      var t2 = moment(endTime);
      var dt = t2.diff(t1) / 1000;
      return dt;
    },
    getChartXaxisTime(val) {
      var len = this.activeDetailData.length;
      var startTime = this.activeDetailData[0].startTime;
      var endTime = this.activeDetailData[len - 1].endTime;
      var dt = this.getTimeDiff(startTime, endTime);
      var seconds = (dt / 100) * val;
      var xaxisTime = moment(startTime)
        .add(seconds, 'second')
        .format('HH:mm:ss');
      return xaxisTime;
    },
  },
};
</script>
