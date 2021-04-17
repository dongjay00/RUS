<template>
  <v-card class="mx-1" height="80" width="160" color="white" flat>
    <v-card-text>
      <p style="font-size: 1.5vh; text-align: center; color: grey; margin-top: -1vh;">
        {{ title }}
      </p>
      <p
        :style="{ color: activeColor }"
        style="font-size: 2vh; text-align: center; font-weight: 500; margin-top: -0.5vh;"
      >
        {{ text }}
      </p>
    </v-card-text>
  </v-card>
</template>
<script>
export default {
  name: 'SmallCard',
  props: ['title', 'text'],
  watch: {
    text() {
      this.getActiveColor(this.text);
    },
  },
  data() {
    return {
      activeColor: 'black',
    };
  },
  created() {
    this.getActiveColor(this.text);
  },
  methods: {
    getActiveColor(text) {
      if (text == '낮음') {
        this.activeColor = 'red';
      } else if (text == '높음') {
        this.activeColor = 'green';
      } else if (text == 'A') {
        this.activeColor = 'green';
      } else if (text == 'B') {
        this.activeColor = '#2EA7E0';
      } else if (text == 'C') {
        this.activeColor = '#7D10C4';
      } else if (text == 'D') {
        this.activeColor = 'orange';
      } else if (text == 'E') {
        this.activeColor = 'red';
      } else if (text.substring(text.length - 1) == '%') {
        let activePercent = text.substring(0, text.length - 1);
        if (activePercent > 90) {
          this.activeColor = 'green';
        } else if (activePercent > 80) {
          this.activeColor = '#2EA7E0';
        } else if (activePercent > 70) {
          this.activeColor = '#7D10C4';
        } else if (activePercent > 60) {
          this.activeColor = 'orange';
        } else {
          this.activeColor = 'red';
        }
      } else {
        this.activeColor = 'black';
      }
    },
  },
};
</script>
<style></style>
