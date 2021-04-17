<template>
  <v-row justify="center">
    <v-dialog v-model="openCreateGroupModal" persistent max-width="600px">
      <v-card>
        <v-card-title class="grey lighten-2 text-h6">
          그룹 생성
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
                  <v-text-field :label="groupLeader" disabled required></v-text-field>
                </div>
              </v-col>
              <v-col cols="12">
                <v-file-input
                  v-model="groupImage"
                  chips
                  color="#4A4A48"
                  label="그룹 대표 이미지"
                ></v-file-input>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  color="#4A4A48"
                  v-model="groupDescription"
                  label="그룹 소개"
                  counter
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
          <v-btn color="#3C474D" class="white--text" @click="createGroup" depressed>
            생성
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import axios from '@/http-common';

export default {
  props: ['openCreateGroupModal'],
  data() {
    return {
      groupName: '',
      groupImage: null,
      groupDescription: '',
      groupLeader: '',
      maxUser: 30,
      rules: [(v) => !!v || '필수 입력란입니다.'],
    };
  },
  computed: {
    nickname() {
      return this.$store.getters.nickname;
    },
    user_pk() {
      return this.$store.getters.user_pk;
    },
  },
  methods: {
    closeModal() {
      this.$emit('close');
      this.groupName = '';
      this.groupImage = null;
      this.groupDescription = '';
      this.groupLeader = '';
    },
    createGroup() {
      this.$emit('close');
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

            axios.post(`/users/group/create/${this.user_pk}/`, group).then(() => {
              this.groupName = '';
              this.groupImage = null;
              this.groupDescription = '';
              this.$emit('reload');
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
          group_img: '',
          description: this.groupDescription,
        };
        axios.post(`/users/group/create/${this.user_pk}/`, group).then(() => {
          this.groupName = '';
          this.groupImage = null;
          this.groupDescription = '';
          this.$emit('reload');
        });
      }
    },
  },
  created() {
    this.groupLeader = this.nickname;
  },
};
</script>
