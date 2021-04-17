<template>
  <div>
    <h1 v-if="!isBack" class="mx-8 my-6">{{ title }}</h1>
    <v-btn v-if="isBack" large color="#3D484E" class="my-4" dark @click="watchTimeline"
      >돌아가기</v-btn
    >
  </div>
</template>
<script>
export default {
  name: 'PageTitle',
  props: ['title', 'isBack'],
  methods: {
    watchTimeline() {
      this.$router.push('/mypage/timeline');
    },
  },
};
</script>
