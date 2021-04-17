<template>
  <div id="chart">
    <apexchart type="pie" width="450" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
<script>
import VueApexCharts from 'vue-apexcharts';
export default {
  name: 'PieChart',
  props: ['activeData'],
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          toolbar: {
            show: false, // 햄버거 버튼 지우기
          },
          width: 380,
          type: 'pie',
        },
        colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0'],
        labels: [], // 범례
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 200,
              },
              legend: {
                position: 'bottom',
              },
            },
          },
        ],
        tooltip: {
          y: {
            formatter: function(val) {
              let formatString = '';
              if (val % 1 == 0) {
                formatString = val + 'h';
              } else if (val < 0.1) {
                let minutes = val * 60;
                formatString = minutes.toFixed(0) + 'm';
              } else {
                formatString = val.toFixed(1) + ' h';
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
      var labels = ['학습시간', '휴식시간', '졸음시간', '자리비움', '딴짓시간'];

      series.push(this.activeData.studyTime);
      series.push(this.activeData.restTime);
      series.push(this.activeData.sleepTime);
      series.push(this.activeData.emptyTime);
      series.push(this.activeData.otherTime);

      this.series = series;
      this.chartOptions.labels = labels;
    },
  },
};
</script>
