<template>
  <div>
    <SideBar />
    <v-container></v-container>
    <sequential-entrance fromBottom>
    <div class="group-header" style="text-align:center;">
      <img src="@/assets/img/group_logo.jpg" alt="" class="group-logo">
      <div style="margin: 3vh 0 0 2vh; font-size: 2vh; font-style: Italic; font-weight: bold;">
        <p>같은 목표를 지닌 사람들과 나를 비교해보고 싶나요?</p>
        <p>그룹에 가입하고 확인해보세요.</p>
      </div>
    </div>
    </sequential-entrance>
    <v-container my-2></v-container>
    <sequential-entrance fromBottom>
    <GroupItem />
    </sequential-entrance>
  </div>
</template>
<script>
import SideBar from '@/components/mypage/SideBar.vue';
import GroupItem from '@/components/mypage/group/GroupItem';
export default {
  name: 'Group',
  components: {
    SideBar,
    GroupItem,
  },
};
</script>
<style scoped>
.group-header {
  display: flex;
  justify-content: center;
}

.group-logo {
  width: 13vh;
  height: 13vh;
  border-radius: 70px;
}
</style>
