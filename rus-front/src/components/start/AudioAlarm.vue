<template>
  <div class="music-player">
    <audio ref="audio" src="@/assets/alarm.mp3" preload loop id="audio" muted></audio>
    <v-btn v-show="false" @click="toggleSound()" class="toggle-sound paused">토글</v-btn>
  </div>
</template>
<script>
export default {
  name: 'AudioAlarm',
  data: () => ({}),
  methods: {
    toggleSound() {
      let audio = this.$refs.audio;
      if (audio.paused && document.querySelector('.toggle-sound').classList.contains('paused')) {
        audio.play();
        document.querySelector('.toggle-sound').classList.remove('paused');
      } else {
        audio.pause();
        document.querySelector('.toggle-sound').classList.add('paused');
      }
    },
  },
};
</script>
