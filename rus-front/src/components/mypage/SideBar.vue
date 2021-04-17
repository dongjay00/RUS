<template>
  <v-navigation-drawer id="navigation-drawer" clipped permanent app>
    <v-list>
      <router-link to="/mypage/timeline">
        <v-list-item>
          <v-list-item-icon>
            <v-icon>fas fa-calendar-alt</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="list-item-title">타임라인</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </router-link>

      <router-link to="/mypage/analysis">
        <v-list-item>
          <v-list-item-icon>
            <v-icon>fas fa-chart-bar</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="list-item-title">분석</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </router-link>

      <router-link to="/mypage/group">
        <v-list-item>
          <v-list-item-icon>
            <v-icon style="font-size: 2vh">fas fa-users</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="list-item-title">그룹관리</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </router-link>
    </v-list>
  </v-navigation-drawer>
</template>
<script>
export default {
  name: 'SideBar',
  components: {},
  methods: {},
};
</script>
<style scoped>
div a {
  text-decoration: none;
}
#navigation-drawer {
  background-color: #282c37;
}
.theme--light.v-icon {
  color: #f2f2f2;
}
.list-item-title {
  color: #f2f2f2;
}
</style>
