<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title
          class="text-h6 grey lighten-2 justify-center"
          style="font-style: Italic; font-weight: bold;"
        >
          경고
          <i class="fas fa-exclamation-triangle ml-2"></i>
        </v-card-title>

        <v-card-text class="mt-4">
          <img src="@/assets/img/icon_cry.png" alt="" width="400px" />
          <v-container class="d-flex justify-center" style="font-style: Italic; font-size: 2vh;">
            <p>당신은 현재 {{ status_stack * 10 }}초간</p>
            <p v-if="active_status == 2" class="text-h7" style="color: red; font-weight: bold;">
              졸고 있습니다!!
            </p>
            <p v-else class="text-h7" style="color: red; font-weight: bold;">딴짓하고 있습니다!!</p>
          </v-container>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#3C474D" dark @click="dialog = false" depressed>
            확인
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
export default {
  name: 'AlarmModal',
  props: ['status_stack'],
  watch: {
    dialog() {
      if (!this.dialog) {
        this.$emit('close-alarm');
      }
    },
  },
  data() {
    return {
      dialog: false,
      active_status: 0,
    };
  },
  created() {},
  methods: {
    openAlarmModal(status) {
      this.dialog = true;
      this.active_status = status;
    },
  },
};
</script>
