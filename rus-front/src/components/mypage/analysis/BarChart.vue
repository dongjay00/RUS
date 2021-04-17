<template>
  <div id="chart">
    <apexchart type="bar" height="300" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
<script>
import VueApexCharts from 'vue-apexcharts';
export default {
  name: 'BarChart',
  props: ['myActiveData', 'groupActiveData'],
  components: {
    apexchart: VueApexCharts,
  },
  watch: {
    myActiveData() {
      this.getChartData();
    },
    groupActiveData() {
      this.getChartData();
    },
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          toolbar: {
            show: false, // 햄버거 버튼 지우기
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
            dataLabels: {
              position: 'top',
            },
          },
        },
        dataLabels: {
          enabled: true,
          style: {
            fontSize: '12px',
            colors: ['#fff'],
          },
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
          width: 1,
          colors: ['#fff'],
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
        xaxis: {
          categories: [], // x축, 화면에는 xy 반전되어 표시
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
      var myData = [];
      var groupData = [];
      var categories = ['학습시간', '휴식시간', '예외시간'];

      myData = this.getActiveData(this.myActiveData);
      groupData = this.getActiveData(this.groupActiveData);

      series.push({ name: '내 활동', data: myData });
      series.push({ name: '그룹 평균 활동', data: groupData });

      this.series = series;
      this.chartOptions.xaxis.categories = categories;
    },
    getActiveData(activeData) {
      var arrayData = [];
      arrayData.push(activeData.studyTime);
      arrayData.push(activeData.restTime);
      arrayData.push(activeData.otherTime);
      return arrayData;
    },
  },
};
</script>
