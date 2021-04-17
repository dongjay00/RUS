<template>
  <v-container>
    <apexchart
      type="bar"
      height="450"
      :options="chartOptions"
      :series="series"
      @change="analysisData"
    ></apexchart>
  </v-container>
</template>
<script>
import VueApexCharts from 'vue-apexcharts';
export default {
  name: 'ColumnChart',
  props: ['analysisData'],
  components: {
    apexchart: VueApexCharts,
  },
  watch: {
    analysisData() {
      this.getChartData();
    },
    chartOptions() {
      this.getChartData();
    },
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          id: 'column-chart',
          toolbar: {
            show: false, // 햄버거 버튼 지우기
          },
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded',
          },
        },
        dataLabels: {
          enabled: true,
          formatter: function(val) {
            let formatString = '';
            if (val % 1 == 0) {
              formatString = val;
            } else {
              formatString = val.toFixed(1);
            }
            return formatString;
          },
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent'],
        },
        xaxis: {
          categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'], // x축
        },
        yaxis: {
          title: {
            text: '시간',
          },
          labels: {
            formatter: function(val) {
              let formatString = '';
              if (val % 1 == 0) {
                formatString = val;
              } else {
                formatString = val.toFixed(1);
              }
              return formatString;
            },
          },
        },
        fill: {
          opacity: 1,
        },
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
    getCategories() {
      var chartOptions = this.chartOptions;
      var categories = [];

      for (let i = 0; i < this.analysisData.length; i++) {
        categories.push(this.analysisData[i].name);
      }

      chartOptions.xaxis.categories = categories;
      this.chartOptions = chartOptions;
    },
    getChartData() {
      this.getCategories();

      var series = [];
      var studyTimes = [];
      var restTimes = [];
      var otherTimes = [];

      for (let i = 0; i < this.analysisData.length; i++) {
        studyTimes.push(this.analysisData[i].studyTime);
        restTimes.push(this.analysisData[i].restTime);
        otherTimes.push(this.analysisData[i].otherTime);
      }

      series.push({ name: '학습시간', data: studyTimes });
      series.push({ name: '휴식시간', data: restTimes });
      series.push({ name: '예외시간', data: otherTimes });

      this.series = series;
    },
  },
};
</script>
