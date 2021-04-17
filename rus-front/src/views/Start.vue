<template>
  <v-container class="mt-12 pt-12">
    <v-row>
      <div class="d-flex mx-auto">
        <v-col>
          <video ref="video" id="video" width="950" height="500" autoplay></video>
          <canvas v-show="capture" ref="canvas" id="canvas" width="950" height="500"></canvas>
          <v-img class="monitor" src="@/assets/img/monitor.png" width="950" min-width="950"></v-img>
        </v-col>
        <v-col
          ><Timer
            ref="timer"
            @start-video="startVideo"
            @stop-video="stopVideo"
            @send-active="sendActive"
            @send-image="DoCapture"
        /></v-col>
      </div>
    </v-row>
    <ResultModal ref="resultModal" :activeData="activeData" />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
  </v-container>
</template>
<script>
import http from '@/http-common';
import axios from 'axios';
import html2canvas from 'html2canvas';
import ResultModal from '@/components/start/ResultModal';
import Timer from '@/components/start/Timer';
export default {
  name: 'Start',
  components: {
    ResultModal,
    Timer,
  },
  data() {
    return {
      video: { srcObject: { getTracks: 0 } },
      canvas: null,
      activeData: null,
      capture: false,
    };
  },
  mounted() {
    this.video = this.$refs.video;
    this.canvas = this.$refs.canvas;
  },
  methods: {
    startVideo() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
          .getUserMedia({ video: { width: 800, height: 450 } })
          .then((stream) => {
            this.video.srcObject = stream;
            this.video.play();
          });
      }
    },
    stopVideo() {
      var stream = this.video.srcObject;
      var tracks = stream.getTracks;

      for (var i = 0; i < tracks.length; i++) {
        var track = tracks[i];
        track.stop();
      }

      this.video.srcObject = null;
    },
    async DoCapture() {
      this.capture = true;
      var context = this.canvas.getContext('2d');
      await context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
      await this.partShot();
    },
    partShot() {
      //특정부분 스크린샷
      html2canvas(this.canvas, { logging: false })
        //id container 부분만 스크린샷
        .then((canvas) => {
          //jpg 결과값
          this.drawImg(canvas.toDataURL('image/jpeg'));
        })
        .catch((err) => {
          console.log(err);
        });
    },
    drawImg(imgData) {
      this.sendImage(imgData);

      return new Promise(() => {
        //내가 결과 값을 그릴 canvas 부분 설정
        var ctx = this.canvas.getContext('2d');
        //canvas의 뿌려진 부분 초기화
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        var imageObj = new Image();
        imageObj.onload = function() {
          ctx.drawImage(imageObj, 10, 10);
          //canvas img를 그리겠다.
        };
        imageObj.src = imgData;
        //그릴 image데이터를 넣어준다.
      });
    },
    async sendActive(active) {
      this.activeData = active;

      await http.post('/actives/active/', active).then(() => {});

      await this.$refs.resultModal.openResultModal(this.activeData);
    },
    async sendImage(img) {
      var params = {
        img_base64: img,
      };
      const res = await axios.post('https://j4b102.p.ssafy.io/api/ais/ai/image/', params);
      await this.$refs.timer.changeActiveType(res.data.result);
      this.capture = false;
    },
  },
};
</script>
<style scoped>
#video {
  display: block;
  margin: auto;
  background-color: #666;
  z-index: 2;
}
#canvas {
  z-index: -1;
  position: absolute;
  top: 0;
  left: 0;
}
.monitor {
  z-index: 0;
  position: absolute;
  top: 4.8vh;
}
</style>
