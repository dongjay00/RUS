<template>
  <v-row justify="center">
    <v-dialog v-model="openUpdateGroupModal" persistent max-width="600px">
      <v-card>
        <v-card-title class="text-h6 grey lighten-2">
          그룹 수정
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <div class="d-flex align-baseline">
                  <v-chip
                    class="mr-2"
                    label
                    small
                  >
                    그룹명
                  </v-chip>
                  
                  <v-text-field
                    :rules="rules"
                    v-model="groupName"
                    color="#4A4A48"
                    required
                  ></v-text-field>
                </div>
              </v-col>
              <v-col cols="12">
                <div class="d-flex align-baseline">
                  <v-chip
                    class="mr-2"
                    label
                    small
                  >
                    그룹장
                  </v-chip>
                  <v-text-field v-model="groupLeader" disabled required></v-text-field>
                </div>
              </v-col>
              <v-col cols="12">
                <v-file-input
                  v-model="groupImage"
                  color="#4A4A48"
                  chips
                  label="그룹 대표 이미지"
                ></v-file-input>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="groupDescription"
                  label="그룹 소개"
                  counter
                  color="#4A4A48"
                  maxlength="120"
                  full-width
                  single-line
                  filled
                  :rules="rules"
                  required
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions class="mx-5 pb-5">
          <v-spacer></v-spacer>
          <v-btn color="white" @click="closeModal" depressed>
            취소
          </v-btn>
          <v-btn color="#3C474D" class="white--text" @click="updateGroup" depressed>
            수정
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import axios from '@/http-common';

export default {
  props: ['openUpdateGroupModal', 'groupDetail'],
  data() {
    return {
      groupName: '',
      groupImage: null,
      groupDescription: '',
      groupLeader: '',
      maxUser: 30,
      originalImage: '',
      rules: [(v) => !!v || '필수 입력란입니다.'],
    };
  },
  computed: {
    user_pk() {
      return this.$store.getters.user_pk;
    },
  },
  methods: {
    closeModal() {
      this.$emit('closeModal');
      this.groupName = '';
      this.groupImage = null;
      this.groupDescription = '';
      this.groupLeader = '';
    },
    updateGroup() {
      this.$emit('closeModal');
      // 그룹정보 보내기
      if (this.groupImage != null) {
        const fd = new FormData();
        fd.append('filename', this.groupImage);

        axios
          .post('/users/group/image/', fd, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then((response) => {
            const group = {
              name: this.groupName,
              leader_pk: this.user_pk,
              max_user: this.maxUser,
              group_img: response.data['image_url'],
              description: this.groupDescription,
            };

            axios.put(`/users/group/${this.groupDetail['group_info']['id']}/`, group).then(() => {
              this.groupName = '';
              this.groupImage = null;
              this.groupDescription = '';
              this.groupLeader = '';
            });
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        const group = {
          name: this.groupName,
          leader_pk: this.user_pk,
          max_user: this.maxUser,
          group_img: this.originalImage,
          description: this.groupDescription,
        };

        axios
          .put(`/users/group/${this.groupDetail['group_info']['id']}/`, group)
          .then(() => {
            this.groupName = '';
            this.groupImage = null;
            this.groupDescription = '';
          });
      }
      this.$emit('reload');
    },
  },

  created() {
    this.groupName = this.groupDetail['group_info']['name'];
    this.groupDescription = this.groupDetail['group_info']['description'];
    this.groupLeader = this.groupDetail['leader_info']['nickname'];
    this.originalImage = this.groupDetail['group_info']['group_img'];
  },
};
</script>
