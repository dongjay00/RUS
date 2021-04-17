<template>
  <v-row justify="center">
    <v-dialog id="groupDetailDialog" v-model="openGroupDetailModal" persistent max-width="600px">
      <v-card>
        <v-card-title class="text-h6 grey lighten-2">
          <span>그룹 정보</span>
        </v-card-title>

        <v-list-item three-line class="px-7 mb-4">
          <v-avatar rounded size="70" color="grey darken-3 mr-4">
            <v-img
              v-if="groupDetail['group_info']['group_img'] == ''"
              class="elevation-6"
              alt=""
              src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
            ></v-img>
            <v-img
              v-else
              class="elevation-6"
              alt=""
              :src="groupDetail['group_info']['group_img']"
            ></v-img>
          </v-avatar>
          <v-list-item-content>
            <v-list-item-title class="heading6 mb-1 d-flex align-baseline">
              <v-chip
                class="mx-2"
                label
                small
              >
                그룹명
              </v-chip>
              <div>
                {{ groupDetail['group_info']['name'] }}
              </div>
            </v-list-item-title>
            <v-list-item-title class="heading6 mb-1 d-flex align-baseline">
              <v-chip
                class="mx-2"
                label
                small
              >
                그룹장
              </v-chip>
              <div>
                {{ groupDetail['leader_info']['nickname'] }}
              </div>
            </v-list-item-title>
            <v-list-item-title class="heading6 mb-1 d-flex align-baseline">
              <v-chip
                class="mx-2"
                label
                small
              >
                회원수
              </v-chip>
              <div>
                {{ groupDetail['members_info'].length }} 명
              </div>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-textarea
          class="px-7"
          filled
          disabled
          name="input-7-3"
          :value="groupDetail['group_info']['description']"
        ></v-textarea>

        <v-chip
          class="ml-7 mb-2"
          label
          small
        >
          회원목록
        </v-chip>
        <v-card class="overflow-y-auto mx-7" flat>
          <v-card-text style="max-height: 200px;" class="pt-0">
            <v-list>
              <template v-for="(member, index) in groupDetail['members_info']">
                <v-list-item :key="`member-${index}`">
                  <v-list-item-avatar>
                    <v-img v-if="member['profile_img'] != ''" :src="member['profile_img']"></v-img>
                    <i v-else class="fas fa-user-circle fa-3x"></i>
                  </v-list-item-avatar>
                  {{ member['nickname'] }}
                </v-list-item>
                <v-divider
                  v-if="index + 1 < groupDetail['members_info'].length"
                  :key="`member-divider-${index}`"
                ></v-divider>
              </template>
            </v-list>
          </v-card-text>
        </v-card>

        <v-card-actions class="mx-3 py-5 d-flex justify-space-between">
          <v-btn
            v-if="user_pk == groupDetail['leader_info']['id']"
            color="white"
            depressed
            x-small
            dense
            class="ma-1 red--text"
            @click="deleteGroup"
          >
            그룹 해산
          </v-btn>
          <v-btn color="#3C474D" class="white--text ml-auto" @click="closeModal" depressed>
            닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import axios from '@/http-common';

export default {
  props: ['openGroupDetailModal', 'groupDetail'],
  data() {
    return {};
  },
  computed: {
    user_pk() {
      return this.$store.getters.user_pk;
    },
  },
  methods: {
    deleteGroup() {
      this.$emit('closeModal');
      axios.delete(`/users/group/${this.groupDetail['group_info']['id']}/`).then(() => {
        this.$emit('reload');
      });
    },
    closeModal() {
      this.$emit('closeModal');
    },
  },
};
</script>
<style scoped>

</style>
