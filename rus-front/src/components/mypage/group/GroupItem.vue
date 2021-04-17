<template>
  <v-container>
    <v-row>
      <v-col cols="1">
        <v-btn id="groupCreateBtn" dark @click="openCreateGroupModal = true" color="#3C474D" depressed>
          그룹 생성
        </v-btn>
      </v-col>
      <v-col cols="7"></v-col>
      <v-col cols="4" class="d-flex">
        <v-text-field
          v-model="search"
          label="검색"
          solo
          dense
          background-color="white"
          @keypress.enter="searchGroup"
          
        ></v-text-field>
        <v-btn class="mx-3 white--text" color="#3C474D" @click="searchGroup" depressed>
          검색
        </v-btn>
      </v-col>
      <CreateGroupModal
        :openCreateGroupModal="openCreateGroupModal"
        v-on:close="openCreateGroupModal = false"
        v-on:reload="(reloadMyGroup = true), (reloadAllGroup = true)"
      />
    </v-row>
    <v-card class="pb-4" flat rounded="lg">
      <v-tabs v-model="tab" dark background-color="#3C474D">
        <v-tab>내 그룹</v-tab>
        <v-tab>그룹 찾기</v-tab>

        <v-tab-item class="mt-3 px-4 pr-6">
          <v-list two-line>
            <template v-for="(myGroup, index) in calMyGroupData">
              <v-list-item :key="`my-${index}`">
                <v-list-item-avatar color="grey darken-1">
                  <v-img
                    v-if="myGroup['group_img'] == ''"
                    class="elevation-6"
                    alt=""
                    src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
                  ></v-img>
                  <v-img v-else :src="myGroup['group_img']"></v-img>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title>{{ myGroup['name'] }}</v-list-item-title>

                  <v-list-item-subtitle class="d-flex align-center justify-space-between">
                    {{ myGroup['description'] }}
                    <div class="d-flex">
                      <v-btn
                        v-if="myGroup['leader_pk'] == user_pk"
                        color="white"
                        class="ma-1"
                        @click="goUpdateGroupModal(myGroup['id'])"
                        depressed
                      >
                        수정
                      </v-btn>
                      <v-btn
                        v-if="myGroup['leader_pk'] != user_pk"
                        color="white"
                        class="ma-1 red--text"
                        @click="leaveGroup(myGroup['id'], myGroup['leader_pk'])"
                        depressed
                      >
                        탈퇴
                      </v-btn>
                      <v-btn
                        class="ma-1"
                        color="#3C474D"
                        dark
                        @click="goGroupDetailModal(myGroup['id'])"
                        depressed
                      >
                        조회
                      </v-btn>
                    </div>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>

              <v-divider :key="`my-divider-${index}`" inset></v-divider>
            </template>

            <v-snackbar v-model="snackbar" :timeout="timeout">
              탈퇴되었습니다.

              <template v-slot:action="{ attrs }">
                <v-btn color="#A3A19D" text v-bind="attrs" @click="snackbar = false">
                  확인
                </v-btn>
              </template>
            </v-snackbar>
          </v-list>
          <v-pagination v-model="curMyGroupPageNum" color="#3C474D" :length="numOfMyGroupPages">
          </v-pagination>
        </v-tab-item>

        <v-tab-item class="mt-3 px-4 pr-6">
          <v-list two-line>
            <template v-for="(allGroup, index) in calAllGroupData">
              <v-list-item :key="`all-${index}`">
                <v-list-item-avatar color="grey darken-1">
                  <v-img
                    v-if="allGroup['group_img'] == ''"
                    class="elevation-6"
                    alt=""
                    src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
                  ></v-img>
                  <v-img v-else :src="allGroup['group_img']"></v-img>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title>{{ allGroup['name'] }}</v-list-item-title>

                  <v-list-item-subtitle class="d-flex align-center justify-space-between">
                    {{ allGroup['description'] }}
                    <div class="d-flex">
                      <v-btn
                        v-if="allGroup['participate'] == 'false'"
                        class="ma-1"
                        color="white"
                        @click="joinGroup(allGroup['id'])"
                        depressed
                      >
                        가입
                      </v-btn>
                      <v-btn
                        class="ma-1"
                        color="#3C474D"
                        dark
                        @click="goGroupDetailModal(allGroup['id'])"
                        depressed
                      >
                        조회
                      </v-btn>
                    </div>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>

              <v-divider :key="`all-divider-${index}`" inset></v-divider>
            </template>

            <v-snackbar v-model="snackbar" :timeout="timeout">
              가입되었습니다.

              <template v-slot:action="{ attrs }">
                <v-btn color="#A3A19D" text v-bind="attrs" @click="snackbar = false">
                  확인
                </v-btn>
              </template>
            </v-snackbar>
          </v-list>
          <v-pagination v-model="curAllGroupPageNum" color="#3C474D" :length="numOfAllGroupPages">
          </v-pagination>
        </v-tab-item>
      </v-tabs>
    </v-card>

    <UpdateGroupModal
      v-if="openUpdateGroupModal == true"
      :groupDetail="groupDetail"
      :openUpdateGroupModal="openUpdateGroupModal"
      v-on:closeModal="openUpdateGroupModal = false"
      v-on:reload="(reloadMyGroup = true), (reloadAllGroup = true)"
    ></UpdateGroupModal>

    <GroupDetailModal
      v-if="openGroupDetailModal == true"
      :groupDetail="groupDetail"
      :openGroupDetailModal="openGroupDetailModal"
      v-on:closeModal="openGroupDetailModal = false"
      v-on:reload="(reloadMyGroup = true), (reloadAllGroup = true)"
    >
    </GroupDetailModal>
  </v-container>
</template>

<script>
import GroupDetailModal from '@/components/mypage/group/GroupDetailModal.vue';
import CreateGroupModal from '@/components/mypage/group/CreateGroupModal';
import UpdateGroupModal from '@/components/mypage/group/UpdateGroupModal';
import axios from '@/http-common';

export default {
  components: {
    GroupDetailModal,
    CreateGroupModal,
    UpdateGroupModal,
  },
  data: () => ({
    tab: '',
    cards: ['Today'],
    search: '',
    openCreateGroupModal: false,
    openGroupDetailModal: false,
    openUpdateGroupModal: false,
    snackbar: false,
    timeout: 2000,
    groupListAll: [],
    myGroup: [],
    groupDetail: [],
    dataPerPage: 5,
    curMyGroupPageNum: 1,
    curAllGroupPageNum: 1,
    reloadMyGroup: false,
    reloadAllGroup: false,
  }),
  computed: {
    user_pk() {
      return this.$store.getters.user_pk;
    },
    myStartOffset() {
      return (this.curMyGroupPageNum - 1) * this.dataPerPage;
    },
    allStartOffset() {
      return (this.curAllGroupPageNum - 1) * this.dataPerPage;
    },
    myEndOffset() {
      return this.myStartOffset + this.dataPerPage;
    },
    allEndOffset() {
      return this.allStartOffset + this.dataPerPage;
    },
    numOfMyGroupPages() {
      return Math.ceil(this.myGroup.length / this.dataPerPage);
    },
    numOfAllGroupPages() {
      return Math.ceil(this.groupListAll.length / this.dataPerPage);
    },
    calMyGroupData: {
      get() {
        return this.myGroup.slice(this.myStartOffset, this.myEndOffset);
      },
      set() {},
    },
    calAllGroupData: {
      get() {
        return this.groupListAll.slice(this.allStartOffset, this.allEndOffset);
      },
      set() {},
    },
  },
  methods: {
    async goUpdateGroupModal(group_pk) {
      await this.getData(group_pk);
      this.openUpdateGroupModal = true;
    },
    async getData(group_pk) {
      const res = await axios.get(`/users/group/${group_pk}/`);
      this.groupDetail = res.data;
    },
    async searchGroup() {
      if (this.tab == 0) {
        await axios
          .get(`/users/group/my/${this.user_pk}/`)
          .then((response) => {
            const result = response.data.filter((group) => {
              return group['name'].toLowerCase().includes(this.search.toLowerCase());
            });
            this.myGroup = result;
            this.search = '';
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        await axios
          .get(`/users/group/list/${this.user_pk}/`)
          .then((response) => {
            const result = response.data.filter((group) => {
              return group['name'].toLowerCase().includes(this.search.toLowerCase());
            });
            this.groupListAll = result;
            this.search = '';
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    leaveGroup(group_pk, leader_pk) {
      if (this.user_pk != leader_pk) {
        axios
          .delete(`/users/group/member/${this.user_pk}/${group_pk}/`)
          .then(() => {
            this.snackbar = true;
            this.reloadAllGroup = true;
            this.reloadMyGroup = true;
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    joinGroup(group_pk) {
      axios
        .put(`/users/group/member/${this.user_pk}/${group_pk}/`)
        .then(() => {
          this.reloadAllGroup = true;
          this.reloadMyGroup = true;
          this.snackbar = true;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    goGroupDetailModal(group_pk) {
      axios.get(`/users/group/${group_pk}/`).then((response) => {
        this.groupDetail = response.data;
        this.openGroupDetailModal = true;
      });
    },
  },
  created() {
    axios
      .get(`/users/group/list/${this.user_pk}/`)
      .then((response) => {
        this.groupListAll = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
    axios.get(`/users/group/my/${this.user_pk}/`).then((response) => {
      this.myGroup = response.data;
    });
  },
  watch: {
    myGroup() {
      this.calMyGroupData
    },
    groupListAll() {
      this.calAllGroupData
    },
    reloadMyGroup() {
      this.reloadMyGroup = false;
      axios.get(`/users/group/my/${this.user_pk}/`).then((response) => {
        this.myGroup = response.data;
      });
    },
    reloadAllGroup() {
      this.reloadAllGroup = false;
      axios.get(`/users/group/list/${this.user_pk}/`).then((response) => {
        this.groupListAll = response.data;
      });
    },
  },
};
</script>
<style scoped>
#groupCreateBtn {
  background-color: #797979;
}
#groupCreateBtn:hover {
  background-color: #a3a19d;
  color: #4a4a48;
}
</style>
